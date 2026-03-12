# Модель элемента упорядочивания
# Используется для вопросов типа Ordering

from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.orm import relationship

from app.database.engine import Base


class OrderingItem(Base):
    """
    Модель элемента для вопросов на упорядочивание.
    Хранит элементы и их правильные позиции.
    """
    __tablename__ = "ordering_items"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, nullable=False)  # Связь с вопросом
    item_text = Column(String, nullable=False)  # Текст элемента
    correct_position = Column(Integer, nullable=False)  # Правильная позиция в порядке
