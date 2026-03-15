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
    profession_id = Column(Integer, ForeignKey("professions.id"), nullable=False, index=True)  # Профессия для тестирования
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)  # Пользователь (может быть NULL для анонимных)
    question_ids = Column(JSON, nullable=False)  # Список ID вопросов в сессии
    status = Column(String, default="active", index=True)  # "active", "completed", "failed"
    score = Column(Integer, default=0)  # Количество правильных ответов
    mode = Column(String, default="practice")  # "practice", "learning", "timed", "exam"
    time_limit = Column(Integer, nullable=True)  # Лимит времени в секундах (для timed mode)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)  # Время создания сессии
    completed_at = Column(DateTime, nullable=True, index=True)  # Время завершения

    # Связи с другими таблицами
    profession = relationship("Profession", back_populates="sessions")
    user = relationship("User", back_populates="sessions")
