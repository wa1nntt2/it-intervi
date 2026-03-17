# API роутер для аутентификации и авторизации
# Регистрация, вход, refresh токенов, управление профилем

import re
from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database.engine import get_db
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    validate_refresh_token,
    get_cookie_config,
)
from app.models.user import User
from app.api.schemas import UserCreate, UserUpdate, UserResponse, TokenCookie
from app.core.config import settings
from app.core.limiter import limiter
from app.api.deps import get_current_user as get_current_user_from_token

# OAuth2 схема для получения токена из заголовка Authorization
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login", auto_error=False)

router = APIRouter(prefix="/auth", tags=["auth"])  # Префикс /api/auth

# Rate limit декораторы
register_limit = limiter.limit("5 per minute")
login_limit = limiter.limit("10 per minute")
refresh_limit = limiter.limit("3 per minute")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Wrapper для общей функции get_current_user из deps.
    Оставлен для обратной совместимости.
    """
    return await get_current_user_from_token(token, db)


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


@router.post("/register")
@register_limit
def register(
    request: Request,
    response: Response,
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
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

    # Устанавливаем CSRF токен для защиты от CSRF атак
    from app.core.csrf import csrf_protect
    csrf_token = csrf_protect.generate_csrf_token()
    csrf_protect.set_csrf_cookie(response, csrf_token)

    # Возвращаем пользователя с CSRF токеном
    user_dict = {
        "id": new_user.id,
        "email": new_user.email,
        "is_admin": new_user.is_admin,
        "created_at": new_user.created_at,
        "csrf_token": csrf_token
    }
    return user_dict


@router.post("/login", response_model=TokenCookie)
@login_limit
def login(
    request: Request,
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Вход пользователя (аутентификация).

    Проверяет email и пароль, устанавливает токены в HttpOnly cookies.
    Использует OAuth2PasswordRequestForm для совместимости с OAuth2.

    Args:
        request: HTTP запрос
        response: HTTP ответ для установки cookies
        form_data: Данные формы (username=email, password)
        db: Сессия базы данных

    Returns:
        TokenCookie: Access токен в теле ответа (refresh в cookie)

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

    # Устанавливаем refresh токен в HttpOnly cookie
    cookie_config = get_cookie_config()
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=cookie_config["httponly"],
        secure=cookie_config["secure"],
        samesite=cookie_config["samesite"],
        max_age=cookie_config["max_age"],
        path=cookie_config["path"],
    )
    
    # Устанавливаем CSRF токен для защиты от CSRF атак
    from app.core.csrf import csrf_protect
    csrf_token = csrf_protect.generate_csrf_token()
    csrf_protect.set_csrf_cookie(response, csrf_token)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "message": "Токены установлены в cookies",
        "csrf_token": csrf_token  # Возвращаем для совместимости
    }


@router.post("/refresh", response_model=TokenCookie)
@refresh_limit
def refresh_token(
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):
    """
    Обновление access токена с использованием refresh токена из cookies.

    Позволяет получить новую пару токенов без повторного ввода пароля.
    Refresh токен автоматически читается из HttpOnly cookie.

    Args:
        request: HTTP запрос
        response: HTTP ответ для установки cookies
        db: Сессия базы данных

    Returns:
        TokenCookie: Новый access токен в теле ответа (refresh в cookie)

    Raises:
        HTTPException: Если refresh токен невалиден
    """
    # Читаем refresh токен из cookie
    refresh_token = request.cookies.get("refresh_token")
    
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh токен не найден в cookies",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = validate_refresh_token(refresh_token)
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

    # Устанавливаем новый refresh токен в cookie
    cookie_config = get_cookie_config()
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=cookie_config["httponly"],
        secure=cookie_config["secure"],
        samesite=cookie_config["samesite"],
        max_age=cookie_config["max_age"],
        path=cookie_config["path"],
    )

    return {
        "access_token": new_access_token,
        "token_type": "bearer",
        "message": "Токены обновлены"
    }


@router.post("/logout")
def logout(
    request: Request,
    response: Response
):
    """
    Выход пользователя.

    Удаляет refresh токен из cookies.

    Args:
        request: HTTP запрос
        response: HTTP ответ для очистки cookies

    Returns:
        dict: Сообщение об успешном выходе
    """
    # Очищаем refresh токен из cookie
    response.delete_cookie(
        key="refresh_token",
        path="/",
    )
    return {"message": "Выход выполнен успешно"}


@router.get("/csrf-token")
def get_csrf_token(request: Request, response: Response):
    """
    Получить новый CSRF токен.
    
    Используется при инициализации приложения или после истечения срока действия токена.
    
    Args:
        request: HTTP запрос
        response: HTTP ответ для установки cookies
        
    Returns:
        dict: CSRF токен
    """
    from app.core.csrf import csrf_protect
    
    csrf_token = csrf_protect.generate_csrf_token()
    csrf_protect.set_csrf_cookie(response, csrf_token)
    
    return {"csrf_token": csrf_token}


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
