# Движок базы данных SQLAlchemy
# Настраивает подключение к SQLite/PostgreSQL и сессию для работы с БД

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings

# URL базы данных для Alembic
DATABASE_URL = settings.DATABASE_URL

# Проверка типа БД
is_sqlite = DATABASE_URL.startswith("sqlite")

# Создание движка SQLAlchemy для подключения к базе данных
# check_same_thread=False требуется только для SQLite при использовании в многопоточном режиме
connect_args = {"check_same_thread": False} if is_sqlite else {}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args
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
