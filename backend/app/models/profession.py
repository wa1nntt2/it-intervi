# Модель профессии
# Представляет направления IT (Frontend, Backend, etc.)

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database.engine import Base


class Profession(Base):
    """
    Модель профессии/направления в IT.
    Используется для категоризации вопросов и сессий.
    """
    __tablename__ = "professions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # Название профессии (например, "Frontend Developer")
    description = Column(Text, nullable=True)  # Краткое описание

    # Связи с другими таблицами
    questions = relationship("Question", back_populates="profession")  # Вопросы по профессии
    sessions = relationship("Session", back_populates="profession")  # Сессии тестирования
