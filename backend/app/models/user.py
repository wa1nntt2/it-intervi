# Модель пользователя
# Представляет таблицу users в базе данных

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database.engine import Base


class User(Base):
    """
    Модель пользователя системы.
    Содержит данные для аутентификации и авторизации.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)  # Уникальный email для входа
    hashed_password = Column(String, nullable=False)  # Хешированный пароль (bcrypt)
    is_admin = Column(Boolean, default=False)  # Флаг администратора
    created_at = Column(DateTime, default=datetime.utcnow)  # Дата регистрации

    # Связи с другими таблицами
    sessions = relationship("Session", back_populates="user")  # Сессии тестирования
    achievements = relationship("UserAchievement", back_populates="user", cascade="all, delete-orphan")  # Достижения
    interview_configs = relationship("InterviewConfig", back_populates="user")  # Сохранённые конфигурации собеседований
