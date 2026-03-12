# Модель ответа пользователя
# Хранит историю ответов на вопросы

from sqlalchemy import Column, Integer, Boolean, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database.engine import Base


class Answer(Base):
    """
    Модель ответа пользователя на вопрос.
    Сохраняет историю прохождения тестирования.
    """
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)  # Связь с вопросом
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Связь с пользователем (может быть NULL для анонимных сессий)
    selected_option = Column(Integer, nullable=True)  # Выбранный вариант ответа (индекс)
    selected_order = Column(JSON, nullable=True)  # Выбранный порядок (для Ordering вопросов)
    is_correct = Column(Boolean, default=False)  # Флаг правильного ответа
    created_at = Column(DateTime, default=datetime.utcnow)  # Время ответа

    # Связь с вопросом
    question = relationship("Question")
