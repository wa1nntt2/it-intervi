# Конфигурация приложения
# Загружает переменные окружения из .env файла

import os
import secrets
from pathlib import Path
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Настройки приложения.
    Переменные окружения загружаются из .env файла.
    Все значения по умолчанию могут быть переопределены через переменные окружения.
    """

    PROJECT_NAME: str = "IT Interview Trainer"
    VERSION: str = "0.1.0"

    # URL подключения к базе данных SQLite
    DATABASE_URL: str = "sqlite:///./interview_trainer.db"

    # Секретный ключ для JWT токенов
    # В production обязательно установите через переменную окружения!
    SECRET_KEY: str = Field(
        default_factory=lambda: os.environ.get("SECRET_KEY", ""),
        description="Секретный ключ для JWT. Должен быть установлен в .env файле."
    )

    # Настройки JWT
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # Время жизни access токена (минуты)
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7  # Время жизни refresh токена (дни)

    DEBUG: bool = True  # Режим отладки

    # CORS settings - разрешенные origin для frontend
    CORS_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:3000"
    CORS_ALLOW_CREDENTIALS: bool = True

    # Rate limiting - ограничение количества запросов в минуту
    RATE_LIMIT_PER_MINUTE: int = 10

    # Пагинация
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100

    # Сессии
    QUESTIONS_PER_SESSION: int = 20
    MIN_QUESTIONS_IN_SESSION: int = 5

    # Кэширование
    CACHE_CAPACITY: int = 100

    model_config = SettingsConfigDict(
        case_sensitive=False,
        extra='ignore'  # Игнорировать лишние поля
    )

    @field_validator('SECRET_KEY', mode='after')
    @classmethod
    def validate_secret_key(cls, v: str) -> str:
        """
        Валидация SECRET_KEY.
        В DEBUG режиме генерируем временный ключ с предупреждением.
        В production требуем установленный ключ.
        """
        # Если ключ пустой или дефолтный
        if not v or v == "your-secret-key-change-in-production":
            # В DEBUG режиме генерируем временный ключ
            if os.environ.get("DEBUG", "false").lower() == "true":
                import warnings
                temp_key = secrets.token_urlsafe(32)
                warnings.warn(
                    f"⚠️  SECRET_KEY не установлен! Сгенерирован временный ключ. "
                    f"В production обязательно установите SECRET_KEY через переменную окружения.\n"
                    f"Добавьте в .env: SECRET_KEY={temp_key}",
                    UserWarning,
                    stacklevel=2
                )
                return temp_key
            else:
                # В production режиме - ошибка
                raise ValueError(
                    "SECRET_KEY не установлен! "
                    "Установите переменную окружения SECRET_KEY в .env файле. "
                    "Пример: SECRET_KEY=$(openssl rand -hex 32) "
                    "Или используйте: python -c \"import secrets; print(secrets.token_urlsafe(32))\""
                )
        
        # Проверка минимальной длины ключа в production
        if os.environ.get("DEBUG", "false").lower() != "true" and len(v) < 32:
            raise ValueError(
                f"SECRET_KEY слишком короткий! Минимальная длина 32 символа. "
                f"Текущая длина: {len(v)}. "
                "Сгенерируйте надежный ключ: openssl rand -hex 32"
            )
        
        return v


# Глобальный экземпляр настроек
settings = Settings()
