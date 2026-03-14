# Модель категории вопросов
# Представляет тему/категорию вопросов (Linux, Docker, Сети и т.д.)

from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table
from sqlalchemy.orm import relationship

from app.database.engine import Base


# Таблица связи многие-ко-многим между вопросами и категориями
question_categories = Table(
    'question_categories',
    Base.metadata,
    Column('question_id', Integer, ForeignKey('questions.id'), primary_key=True),
    Column('category_id', Integer, ForeignKey('categories.id'), primary_key=True)
)


class Category(Base):
    """
    Модель категории вопросов.
    Категории группируют вопросы по темам (Linux, Docker, Сети, Kubernetes и т.д.)
    """
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # Название категории (например, "Linux")
    description = Column(Text, nullable=True)  # Описание категории
    profession_id = Column(Integer, ForeignKey("professions.id"), nullable=False, index=True)  # Связь с профессией

    # Связи
    profession = relationship("Profession", back_populates="categories")
    questions = relationship("Question", secondary=question_categories, back_populates="categories")
