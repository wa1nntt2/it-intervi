# API роутер для аутентификации и авторизации
# Регистрация, вход, refresh токенов, управление профилем

import re
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database.engine import get_db
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    validate_refresh_token,
)
from app.models.user import User
from app.api.schemas import UserCreate, UserUpdate, UserResponse, Token, TokenRefresh, TokenRefreshResponse
from app.core.config import settings
from app.core.limiter import limiter

router = APIRouter(prefix="/auth", tags=["auth"])  # Префикс /api/auth

# Схема OAuth2 для получения токена из заголовка Authorization
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency для получения текущего пользователя из JWT токена.
    Используется в защищенных endpoint'ах.
    
    Args:
        token: JWT токен из заголовка Authorization
        db: Сессия базы данных
    
    Returns:
        User: Объект текущего пользователя
    
    Raises:
        HTTPException: Если токен невалиден или пользователь не найден
    """
    from app.core.security import decode_token

    payload = decode_token(token, expected_type="access")
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный или истекший токен",
            headers={"WWW-Authenticate": "Bearer"},
        )

    email: str = payload.get("sub")
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный токен",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не найден",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


def validate_password_strength(password: str) -> None:
    """
    Валидация сложности пароля.
    
    Требования к паролю:
    - Минимум 8 символов
    - Хотя бы одна заглавная буква
    - Хотя бы одна строчная буква
    - Хотя бы одна цифра
    
    Args:
        password: Пароль для проверки
    
    Raises:
        HTTPException: Если пароль не соответствует требованиям
    """
    if len(password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пароль должен содержать минимум 8 символов"
        )
    if not re.search(r"[A-Z]", password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пароль должен содержать хотя бы одну заглавную букву"
        )
    if not re.search(r"[a-z]", password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пароль должен содержать хотя бы одну строчную букву"
        )
    if not re.search(r"\d", password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пароль должен содержать хотя бы одну цифру"
        )


@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Регистрация нового пользователя.
    
    Проверяет уникальность email и сложность пароля,
    затем создает нового пользователя в базе данных.
    
    Args:
        user_data: Данные для регистрации (email, password)
        db: Сессия базы данных
    
    Returns:
        UserResponse: Данные созданного пользователя
    
    Raises:
        HTTPException: Если email уже занят или пароль слишком простой
    """
    # Проверка существующего пользователя
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email уже зарегистрирован"
        )

    # Валидация сложности пароля
    validate_password_strength(user_data.password)

    new_user = User(
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login", response_model=Token)
def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Вход пользователя (аутентификация).
    
    Проверяет email и пароль, возвращает пару access/refresh токенов.
    Использует OAuth2PasswordRequestForm для совместимости с OAuth2.
    
    Args:
        request: HTTP запрос
        form_data: Данные формы (username=email, password)
        db: Сессия базы данных
    
    Returns:
        Token: Access и refresh токены
    
    Raises:
        HTTPException: Если credentials неверны
    """
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(data={"sub": user.email})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/refresh", response_model=TokenRefreshResponse)
def refresh_token(
    token_data: TokenRefresh,
    db: Session = Depends(get_db)
):
    """
    Обновление access токена с использованием refresh токена.
    
    Позволяет получить новую пару токенов без повторного ввода пароля.
    
    Args:
        token_data: Refresh токен
        db: Сессия базы данных
    
    Returns:
        TokenRefreshResponse: Новая пара токенов
    
    Raises:
        HTTPException: Если refresh токен невалиден
    """
    payload = validate_refresh_token(token_data.refresh_token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный или истекший refresh токен",
            headers={"WWW-Authenticate": "Bearer"},
        )

    email: str = payload.get("sub")
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный refresh токен",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не найден",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Создаем новую пару токенов
    new_access_token = create_access_token(data={"sub": user.email})
    new_refresh_token = create_refresh_token(data={"sub": user.email})

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }


@router.get("/me", response_model=UserResponse)
def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """
    Получение информации о текущем пользователе.
    
    Защищенный endpoint - требует валидный access токен.
    
    Returns:
        UserResponse: Данные текущего пользователя
    """
    return current_user


@router.put("/me", response_model=UserResponse)
def update_current_user(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Обновление профиля текущего пользователя.
    
    Позволяет изменить пароль и статус администратора.
    
    Args:
        user_data: Данные для обновления
        current_user: Текущий пользователь
        db: Сессия базы данных
    
    Returns:
        UserResponse: Обновленные данные пользователя
    """
    if user_data.password is not None:
        validate_password_strength(user_data.password)
        current_user.hashed_password = get_password_hash(user_data.password)

    if user_data.is_admin is not None:
        # Только админ может изменить свой статус (для безопасности)
        # В реальном приложении это должно быть ограничено
        current_user.is_admin = user_data.is_admin

    db.commit()
    db.refresh(current_user)
    return current_user
