"""
Unit тесты для моделей SQLAlchemy.
"""

import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.engine import Base
from app.models.user import User
from app.models.profession import Profession
from app.models.question import Question
from app.models.session import Session


# Создаем тестовую БД в памяти
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Фикстура для сессии БД"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


class TestUserModel:
    """Тесты модели User"""

    def test_create_user(self, db_session):
        """Тест создания пользователя"""
        user = User(
            email="test@example.com",
            hashed_password="hashed_password_123",
            is_admin=False
        )
        
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        
        assert user.id is not None
        assert user.email == "test@example.com"
        assert user.is_admin is False
        assert isinstance(user.created_at, datetime)

    def test_user_unique_email(self, db_session):
        """Тест уникальности email"""
        user1 = User(email="unique@example.com", hashed_password="hash1")
        user2 = User(email="unique@example.com", hashed_password="hash2")
        
        db_session.add(user1)
        db_session.commit()
        
        # Попытка добавить пользователя с таким же email должна вызвать ошибку
        db_session.add(user2)
        with pytest.raises(Exception):
            db_session.commit()

    def test_user_relationships(self, db_session):
        """Тест связей пользователя"""
        user = User(email="relations@example.com", hashed_password="hash")
        db_session.add(user)
        db_session.commit()
        
        # Проверяем, что связи инициализированы
        assert user.sessions is not None
        assert user.achievements is not None


class TestProfessionModel:
    """Тесты модели Profession"""

    def test_create_profession(self, db_session):
        """Тест создания профессии"""
        profession = Profession(
            name="Frontend Developer",
            description="React, Vue, Angular"
        )
        
        db_session.add(profession)
        db_session.commit()
        db_session.refresh(profession)
        
        assert profession.id is not None
        assert profession.name == "Frontend Developer"
        assert profession.description == "React, Vue, Angular"

    def test_profession_without_description(self, db_session):
        """Тест профессии без описания"""
        profession = Profession(name="Backend Developer")
        
        db_session.add(profession)
        db_session.commit()
        
        assert profession.id is not None
        assert profession.name == "Backend Developer"
        assert profession.description is None


class TestQuestionModel:
    """Тесты модели Question"""

    def test_create_mcq_question(self, db_session):
        """Тест создания MCQ вопроса"""
        profession = Profession(name="Test Profession")
        db_session.add(profession)
        db_session.commit()
        
        question = Question(
            text="What is Python?",
            question_type="mcq",
            profession_id=profession.id,
            difficulty="junior",
            options=["Snake", "Programming Language", "Java", "C++"],
            correct_option=1
        )
        
        db_session.add(question)
        db_session.commit()
        db_session.refresh(question)
        
        assert question.id is not None
        assert question.question_type == "mcq"
        assert question.correct_option == 1
        assert len(question.options) == 4

    def test_create_ordering_question(self, db_session):
        """Тест создания вопроса на упорядочивание"""
        profession = Profession(name="Test Profession")
        db_session.add(profession)
        db_session.commit()
        
        question = Question(
            text="Order the SDLC phases",
            question_type="ordering",
            profession_id=profession.id,
            difficulty="middle",
            options=["Planning", "Development", "Testing", "Deployment"],
            correct_order=[0, 1, 2, 3]
        )
        
        db_session.add(question)
        db_session.commit()
        db_session.refresh(question)
        
        assert question.question_type == "ordering"
        assert question.correct_order == [0, 1, 2, 3]

    def test_question_with_explanation(self, db_session):
        """Тест вопроса с пояснением"""
        profession = Profession(name="Test Profession")
        db_session.add(profession)
        db_session.commit()
        
        question = Question(
            text="What is HTML?",
            question_type="mcq",
            profession_id=profession.id,
            difficulty="intern",
            options=["Language", "Protocol", "Database", "OS"],
            correct_option=0,
            explanation="HTML is HyperText Markup Language"
        )
        
        db_session.add(question)
        db_session.commit()
        
        assert question.explanation == "HTML is HyperText Markup Language"


class TestSessionModel:
    """Тесты модели Session"""

    def test_create_session(self, db_session):
        """Тест создания сессии"""
        profession = Profession(name="Test Profession")
        db_session.add(profession)
        db_session.commit()
        
        session = Session(
            profession_id=profession.id,
            question_ids=[1, 2, 3, 4, 5],
            status="active"
        )
        
        db_session.add(session)
        db_session.commit()
        db_session.refresh(session)
        
        assert session.id is not None
        assert session.status == "active"
        assert session.score == 0
        assert session.question_ids == [1, 2, 3, 4, 5]

    def test_session_with_user(self, db_session):
        """Тест сессии с пользователем"""
        user = User(email="session@example.com", hashed_password="hash")
        profession = Profession(name="Test Profession")
        db_session.add_all([user, profession])
        db_session.commit()
        
        session = Session(
            profession_id=profession.id,
            user_id=user.id,
            question_ids=[1, 2, 3]
        )
        
        db_session.add(session)
        db_session.commit()
        db_session.refresh(session)
        
        assert session.user_id == user.id

    def test_complete_session(self, db_session):
        """Тест завершения сессии"""
        profession = Profession(name="Test Profession")
        db_session.add(profession)
        db_session.commit()
        
        session = Session(
            profession_id=profession.id,
            question_ids=[1, 2, 3, 4, 5],
            status="active"
        )
        
        db_session.add(session)
        db_session.commit()
        
        # Завершаем сессию
        session.status = "completed"
        session.score = 4
        session.completed_at = datetime.utcnow()
        db_session.commit()
        
        assert session.status == "completed"
        assert session.score == 4
        assert session.completed_at is not None
