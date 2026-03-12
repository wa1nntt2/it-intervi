# Модель сессии тестирования
# Хранит информацию о прохождении тестов пользователем

from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database.engine import Base


class Session(Base):
    """
    Модель сессии тестирования.
    Представляет одну попытку прохождения теста по определенной профессии.
    """
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    profession_id = Column(Integer, ForeignKey("professions.id"), nullable=False)  # Профессия для тестирования
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Пользователь (может быть NULL для анонимных)
    question_ids = Column(JSON, nullable=False)  # Список ID вопросов в сессии
    status = Column(String, default="active")  # "active", "completed", "failed"
    score = Column(Integer, default=0)  # Количество правильных ответов
    created_at = Column(DateTime, default=datetime.utcnow)  # Время создания сессии
    completed_at = Column(DateTime, nullable=True)  # Время завершения

    # Связи с другими таблицами
    profession = relationship("Profession", back_populates="sessions")
    user = relationship("User", back_populates="sessions")
