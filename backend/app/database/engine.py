# Движок базы данных SQLAlchemy
# Настраивает подключение к SQLite/PostgreSQL и сессию для работы с БД
# Полная совместимость с обоими типами баз данных

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings

# URL базы данных для Alembic
DATABASE_URL = settings.DATABASE_URL

# Проверка типа БД
is_sqlite = DATABASE_URL.startswith("sqlite")
is_postgresql = DATABASE_URL.startswith("postgresql")

# Настройки подключения
connect_args = {}
if is_sqlite:
    # check_same_thread=False требуется только для SQLite при использовании в многопоточном режиме
    connect_args["check_same_thread"] = False
elif is_postgresql:
    # Для PostgreSQL настройки через psycopg2
    # server_side_cursors включаем через execution_options (не через connect_args)
    pass

# Создание движка SQLAlchemy
# pool_pre_ping=True - проверка соединения перед использованием (важно для PostgreSQL)
# pool_size и max_overflow - только для PostgreSQL (SQLite игнорирует)
engine_kwargs = {
    "connect_args": connect_args,
}

if is_postgresql:
    engine_kwargs["pool_pre_ping"] = True  # Проверка соединения перед использованием
    engine_kwargs["pool_size"] = 20  # Размер пула соединений
    engine_kwargs["max_overflow"] = 40  # Максимум соединений сверх pool_size

engine = create_engine(DATABASE_URL, **engine_kwargs)

# SQLite PRAGMA настройки для включения foreign keys
if is_sqlite:
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        """
        Включение поддержки foreign keys для SQLite.
        По умолчанию SQLite не проверяет внешние ключи.
        """
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

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
