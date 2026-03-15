# Общие зависимости (dependencies) для API endpoints
# Содержит функции для получения текущего пользователя и другие общие зависимости

from fastapi import Depends, HTTPException, status, Header, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Optional

from app.database.engine import get_db
from app.models.user import User
from app.core.security import decode_token

# OAuth2 схема для получения токена из заголовка Authorization
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login", auto_error=False)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency для получения текущего пользователя из JWT токена.
    Поддерживает получение токена из заголовка Authorization или из cookies.
    Используется в защищенных endpoint'ах.

    Args:
        token: JWT токен из заголовка Authorization
        db: Сессия базы данных

    Returns:
        User: Объект текущего пользователя

    Raises:
        HTTPException: Если токен невалиден или пользователь не найден
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Токен не предоставлен",
            headers={"WWW-Authenticate": "Bearer"},
        )

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


async def get_current_user_optional(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Dependency для получения текущего пользователя (опционально).
    Возвращает None если токен невалиден или не предоставлен.
    Используется в endpoint'ах где аутентификация не обязательна.

    Args:
        authorization: Заголовок Authorization с JWT токеном
        db: Сессия базы данных

    Returns:
        User или None если токен невалиден
    """
    if not authorization or not authorization.startswith("Bearer "):
        return None
    
    token = authorization.split(" ")[1]
    try:
        payload = decode_token(token, expected_type="access")
        if payload is None:
            return None

        email: str = payload.get("sub")
        if email is None:
            return None

        user = db.query(User).filter(User.email == email).first()
        return user
    except Exception:
        return None


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Dependency для получения активного пользователя.
    Дополнительно проверяет что пользователь активен.

    Args:
        current_user: Текущий пользователь

    Returns:
        User: Активный пользователь

    Raises:
        HTTPException: Если пользователь не активен
    """
    # В будущей реализации можно добавить поле is_active
    return current_user


async def get_current_admin_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Dependency для получения пользователя с правами администратора.
    Используется в админских endpoint'ах.

    Args:
        current_user: Текущий пользователь

    Returns:
        User: Пользователь с правами администратора

    Raises:
        HTTPException: Если пользователь не администратор
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Требуется права администратора"
        )
    return current_user
