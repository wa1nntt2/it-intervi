# Импорт всех моделей для корректной работы SQLAlchemy
from app.models.user import User
from app.models.profession import Profession
from app.models.question import Question
from app.models.answer import Answer
from app.models.ordering_item import OrderingItem
from app.models.session import Session
from app.models.user_progress import UserProgress, Achievement, UserAchievement
from app.models.category import Category
from app.models.interview_config import InterviewConfig

__all__ = ["User", "Profession", "Question", "Answer", "OrderingItem", "Session", "UserProgress", "Achievement", "UserAchievement", "Category", "InterviewConfig"]
