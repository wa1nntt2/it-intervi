# Модель прогресса пользователя
# Хранит XP, уровни, статистику и достижения

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database.engine import Base


class UserProgress(Base):
    """
    Модель прогресса пользователя.
    Отслеживает опыт (XP), уровень, статистику прохождения и достижения.
    """
    __tablename__ = "user_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)  # Связь 1:1 с пользователем

    # Уровень и опыт
    xp = Column(Integer, default=0)  # Накопленный опыт
    level = Column(Integer, default=1)  # Текущий уровень

    # Статистика прохождения
    total_sessions = Column(Integer, default=0)  # Всего сессий пройдено
    completed_sessions = Column(Integer, default=0)  # Завершенных сессий
    total_correct_answers = Column(Integer, default=0)  # Всего правильных ответов
    total_questions_answered = Column(Integer, default=0)  # Всего вопросов отвечено
    best_streak = Column(Integer, default=0)  # Лучшая серия побед
    current_streak = Column(Integer, default=0)  # Текущая серия

    # Даты
    created_at = Column(DateTime, default=datetime.utcnow)  # Дата создания прогресса
    last_session_at = Column(DateTime, nullable=True)  # Дата последней сессии

    # Мета-информация
    title = Column(String, default="Новичок")  # Звание пользователя
    badges = Column(JSON, default=list)  # Список значков/наград

    # Связь с пользователем
    user = relationship("User", backref="progress", uselist=False)


class Achievement(Base):
    """
    Модель достижения.
    Определяет условия разблокировки и награды.
    """
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # Название достижения
    description = Column(String, nullable=False)  # Описание условия
    icon = Column(String, nullable=False)  # Emoji иконка
    xp_reward = Column(Integer, default=0)  # Награда в XP

    # Условия разблокировки
    requirement_type = Column(String, nullable=False)  # "sessions_completed", "correct_answers", "streak", "perfect_score"
    requirement_value = Column(Integer, nullable=False)  # Требуемое значение

    # Категория достижения
    category = Column(String, default="general")  # "general", "profession", "streak"

    # Связь с разблокированными достижениями пользователей
    user_achievements = relationship("UserAchievement", back_populates="achievement")


class UserAchievement(Base):
    """
    Модель разблокированного достижения пользователя.
    Связывает пользователя с полученными достижениями.
    """
    __tablename__ = "user_achievements"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Владелец достижения
    achievement_id = Column(Integer, ForeignKey("achievements.id"), nullable=False)  # Тип достижения

    unlocked_at = Column(DateTime, default=datetime.utcnow)  # Дата разблокировки

    # Связи
    user = relationship("User", back_populates="achievements")
    achievement = relationship("Achievement", back_populates="user_achievements")
