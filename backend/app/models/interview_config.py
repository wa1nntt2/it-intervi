# Модель конфигурации собеседования
# Хранит сохранённые пользователем настройки собеседования (темы, количество вопросов)

from sqlalchemy import Column, Integer, String, ForeignKey, JSON, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database.engine import Base


class InterviewConfig(Base):
    """
    Модель конфигурации собеседования.
    Позволяет пользователю сохранить настройки собеседования:
    - Название (например, "Junior DevOps Interview")
    - Профессия
    - Выбранные категории и количество вопросов для каждой
    - Уровень сложности
    """
    __tablename__ = "interview_configs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # Название конфигурации (даёт пользователь)
    description = Column(String, nullable=True)  # Описание (опционально)
    
    # Основные настройки
    profession_id = Column(Integer, ForeignKey("professions.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)  # Если null - публичный шаблон
    difficulty = Column(String, default="junior")  # "intern", "junior", "middle"
    
    # Категории и количество вопросов: [{"category_id": 1, "question_count": 5}, ...]
    category_configs = Column(JSON, nullable=False, default=list)
    
    # Метаданные
    is_public = Column(Boolean, default=False)  # Публичный шаблон (доступен всем)
    is_default = Column(Boolean, default=False)  # Шаблон по умолчанию для профессии
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Связи
    profession = relationship("Profession", back_populates="interview_configs")
    user = relationship("User", back_populates="interview_configs")
