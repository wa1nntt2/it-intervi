# Модель вопроса
# Хранит вопросы для тестирования с вариантами ответов

from sqlalchemy import Column, Integer, String, Text, ForeignKey, JSON, Table
from sqlalchemy.orm import relationship

from app.database.engine import Base
from app.models.category import question_categories


class Question(Base):
    """
    Модель вопроса для тестирования.
    Поддерживает два типа вопросов:
    - MCQ (Multiple Choice): выбор одного правильного ответа
    - Ordering: упорядочивание элементов в правильном порядке
    """
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)  # Текст вопроса
    question_type = Column(String, nullable=False, index=True)  # "mcq" или "ordering"
    profession_id = Column(Integer, ForeignKey("professions.id"), nullable=False, index=True)  # Связь с профессией
    difficulty = Column(String, default="junior", index=True)  # "intern", "junior", "middle"
    options = Column(JSON, nullable=False)  # Список вариантов ответа (JSON массив)
    correct_option = Column(Integer, nullable=True)  # Индекс правильного ответа (для MCQ)
    correct_order = Column(JSON, nullable=True)  # Правильный порядок элементов (для Ordering)
    explanation = Column(Text, nullable=True)  # Пояснение к правильному ответу

    # Связь с профессией
    profession = relationship("Profession", back_populates="questions")
    
    # Связь с категориями (многие-ко-многим)
    categories = relationship("Category", secondary=question_categories, back_populates="questions")
