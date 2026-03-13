import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine

# Устанавливаем переменные окружения ДО импорта app модулей
import os
os.environ["SECRET_KEY"] = "test-secret-key-for-testing-min-32-chars-12345"
os.environ["DEBUG"] = "true"
os.environ["SKIP_SEED"] = "true"  # Отключаем seed данные для тестов

from app.database.engine import Base, get_db, engine, SessionLocal

# Используем in-memory SQLite для тестов
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


# Включаем foreign keys для SQLite
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


@pytest.fixture(scope="function")
def db_session():
    # Создаем все таблицы в in-memory БД
    Base.metadata.create_all(bind=test_engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Очищаем все таблицы после теста
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    # Переопределяем engine в main.py чтобы использовать тестовый engine
    from app import main
    main.engine = test_engine
    main.SessionLocal = TestingSessionLocal

    # Пересоздаем приложение с тестовым engine
    test_app = main.create_app()

    # Отключаем rate limiting для тестов
    test_app.state.limiter.enabled = False

    with TestClient(test_app) as test_client:
        yield test_client


@pytest.fixture(scope="function", autouse=True)
def setup_test_data(db_session):
    """Автоматически создает тестовую профессию для всех тестов"""
    from app.models.profession import Profession
    
    profession = Profession(
        name="TestProfession",
        description="Test profession for unit tests"
    )
    db_session.add(profession)
    db_session.commit()
    db_session.refresh(profession)
    return profession


@pytest.fixture
def test_user():
    """Фикстура с тестовым пользователем"""
    return {
        "email": "testuser@example.com",
        "password": "TestPass123"
    }


@pytest.fixture
def test_profession(setup_test_data):
    """Фикстура с тестовой профессией (для явного использования)"""
    # Возвращаем профессию созданную в setup_test_data
    return setup_test_data


@pytest.fixture
def authenticated_client(client: TestClient, test_user: dict):
    """Фикстура с аутентифицированным клиентом"""
    # Регистрируем пользователя
    client.post("/api/auth/register", json=test_user)

    # Логинимся и получаем токен
    response = client.post("/api/auth/login", data={
        "username": test_user["email"],
        "password": test_user["password"]
    })

    token = response.json()["access_token"]
    client.headers["Authorization"] = f"Bearer {token}"

    yield client

    # Очищаем заголовок после теста
    client.headers.pop("Authorization", None)
