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

# Импортируем модели чтобы SQLAlchemy знал о них перед созданием таблиц
from app.models import user, profession, question, answer, session, ordering_item, user_progress

# Используем in-memory SQLite для тестов
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# Включаем foreign keys для SQLite ДО создания engine
# Это критично для работы FOREIGN KEY constraints
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

test_engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="function")
def db_session():
    # Включаем foreign keys перед созданием таблиц
    with test_engine.connect() as conn:
        conn.execute(text("PRAGMA foreign_keys=ON"))
        conn.commit()
    
    # Создаем все таблицы в in-memory БД
    Base.metadata.create_all(bind=test_engine)
    
    # Создаем сессию и тестовую профессию
    db = TestingSessionLocal()
    try:
        # Создаем тестовую профессию с ID=1 для всех тестов
        from app.models.profession import Profession
        profession = Profession(
            id=1,
            name="TestProfession",
            description="Test profession for unit tests"
        )
        db.add(profession)
        db.commit()
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


@pytest.fixture(scope="function")
def setup_test_data(db_session):
    """Возвращает тестовую профессию (создается в db_session)"""
    from app.models.profession import Profession
    profession = db_session.query(Profession).filter(Profession.id == 1).first()
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
