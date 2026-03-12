# Модуль безопасности
# Содержит функции для хеширования паролей и работы с JWT токенами

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt, JWTError as JoseJWTError
from passlib.context import CryptContext

from app.core.config import settings

# Контекст для хеширования паролей алгоритмом bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверка соответствия пароля хешу.
    
    Args:
        plain_password: Пароль в открытом виде
        hashed_password: Хешированный пароль из базы данных
    
    Returns:
        True если пароль верный, False иначе
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Хеширование пароля.
    
    Args:
        password: Пароль в открытом виде
    
    Returns:
        Хешированный пароль
    """
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Создание access токена для аутентификации пользователя.
    
    Args:
        data: Данные для кодирования (обычно email пользователя)
        expires_delta: Время действия токена (по умолчанию из настроек)
    
    Returns:
        JWT токен в виде строки
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire, "type": "access"})  # Добавляем метку типа токена
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Создание refresh токена для обновления access токена.
    
    Args:
        data: Данные для кодирования
        expires_delta: Время действия токена (по умолчанию из настроек)
    
    Returns:
        JWT токен для обновления сессии
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    to_encode.update({"exp": expire, "type": "refresh"})  # Метка типа refresh
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_token(token: str, expected_type: str = "access") -> Optional[dict]:
    """
    Декодирование JWT токена с проверкой типа.
    
    Args:
        token: JWT токен для декодирования
        expected_type: Ожидаемый тип токена ('access' или 'refresh')
    
    Returns:
        Расшифрованные данные токена или None если токен невалиден
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        token_type = payload.get("type")
        if token_type != expected_type:
            return None  # Тип токена не совпадает
        return payload
    except (JWTError, JoseJWTError):
        return None


def validate_refresh_token(token: str) -> Optional[dict]:
    """
    Валидация refresh токена.
    
    Args:
        token: Refresh токен для проверки
    
    Returns:
        Расшифрованные данные или None
    """
    return decode_token(token, expected_type="refresh")
