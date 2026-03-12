# Движок базы данных SQLAlchemy
# Настраивает подключение к SQLite и сессию для работы с БД

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings

# Создание движка SQLAlchemy для подключения к базе данных
# check_same_thread=False требуется для SQLite при использовании в многопоточном режиме
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Фабрика сессий для взаимодействия с базой данных
# autocommit=False - транзакции нужно подтверждать вручную
# autoflush=False - автоматическая отправка изменений перед запросами отключена
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для ORM моделей
Base = declarative_base()


def get_db():
    """
    Dependency для получения сессии базы данных.
    Используется в FastAPI endpoints через Depends().
    
    Yields:
        Session: Сессия SQLAlchemy для работы с БД
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  # Гарантированное закрытие сессии
