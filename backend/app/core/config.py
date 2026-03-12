# Конфигурация приложения
# Загружает переменные окружения из .env файла

import os
from pathlib import Path
from pydantic import Field
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

    # Обязательная переменная! Секретный ключ для JWT токенов
    SECRET_KEY: str = Field(..., description="Секретный ключ для JWT. Должен быть установлен в .env файле.")

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

    model_config = SettingsConfigDict(
        case_sensitive=False,
        extra='ignore'  # Игнорировать лишние поля
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Валидация SECRET_KEY при инициализации
        if not self.SECRET_KEY or self.SECRET_KEY == "your-secret-key-change-in-production":
            raise ValueError(
                "SECRET_KEY не установлен! "
                "Установите переменную окружения SECRET_KEY в .env файле. "
                "Пример: SECRET_KEY=$(openssl rand -hex 32)"
            )


# Глобальный экземпляр настроек
settings = Settings()
