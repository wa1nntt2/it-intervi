# Pydantic схемы для валидации данных API
# Определяют структуру запросов и ответов

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


# === Схемы пользователя ===

class UserBase(BaseModel):
    """Базовая схема пользователя с email"""
    email: EmailStr


class UserCreate(UserBase):
    """Схема для регистрации пользователя"""
    password: str


class UserUpdate(BaseModel):
    """Схема для обновления данных пользователя"""
    password: Optional[str] = None  # Новый пароль (опционально)
    is_admin: Optional[bool] = None  # Статус администратора


class UserResponse(UserBase):
    """Схема ответа с данными пользователя"""
    id: int
    created_at: datetime
    is_admin: bool = False

    class Config:
        from_attributes = True  # Разрешить загрузку из SQLAlchemy моделей


# === Схемы для JWT токенов ===

class Token(BaseModel):
    """Схема ответа с access и refresh токенами"""
    access_token: str  # JWT токен для доступа к API
    refresh_token: str  # JWT токен для обновления access токена
    token_type: str = "bearer"  # Тип токена


class TokenRefresh(BaseModel):
    """Схема запроса на refresh токена"""
    refresh_token: str


class TokenRefreshResponse(BaseModel):
    """Схема ответа с новой парой токенов"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


# === Схемы профессии ===

class ProfessionBase(BaseModel):
    """Базовая схема профессии"""
    name: str  # Название профессии
    description: Optional[str] = None  # Описание


class ProfessionCreate(ProfessionBase):
    """Схема для создания профессии"""
    pass


class ProfessionResponse(ProfessionBase):
    """Схема ответа с данными профессии"""
    id: int

    class Config:
        from_attributes = True


# === Схемы вопроса ===

class QuestionBase(BaseModel):
    """Базовая схема вопроса"""
    text: str  # Текст вопроса
    question_type: str  # "mcq" (Multiple Choice) или "ordering" (упорядочивание)
    profession_id: int  # ID профессии
    difficulty: str = "junior"  # "intern", "junior", "middle"
    explanation: Optional[str] = None  # Пояснение к правильному ответу


class QuestionCreate(QuestionBase):
    """Схема для создания вопроса"""
    options: list[str]  # Варианты ответов
    correct_option: Optional[int] = None  # Индекс правильного ответа (для MCQ)
    correct_order: Optional[list[int]] = None  # Правильный порядок (для Ordering)


class QuestionUpdate(BaseModel):
    """Схема для обновления вопроса (все поля опциональны)"""
    text: Optional[str] = None
    question_type: Optional[str] = None
    profession_id: Optional[int] = None
    difficulty: Optional[str] = None
    options: Optional[list[str]] = None
    correct_option: Optional[int] = None
    correct_order: Optional[list[int]] = None
    explanation: Optional[str] = None


class QuestionResponse(QuestionBase):
    """Схема ответа с данными вопроса"""
    id: int
    options: list[str]  # Варианты ответов
    correct_option: Optional[int] = None  # Индекс правильного ответа

    class Config:
        from_attributes = True


# === Схемы ответа ===

class AnswerCreate(BaseModel):
    """Схема для создания ответа на вопрос"""
    selected_option: int  # Индекс выбранного варианта


class AnswerResponse(BaseModel):
    """Схема ответа с данными о ответе пользователя"""
    id: int
    question_id: int
    selected_option: int
    is_correct: bool  # Флаг правильности ответа

    class Config:
        from_attributes = True


# === Схемы сессии ===

class SessionBase(BaseModel):
    """Базовая схема сессии"""
    profession_id: int  # ID профессии для тестирования


class SessionCreate(SessionBase):
    """Схема для создания новой сессии"""
    pass


class SessionResponse(SessionBase):
    """Схема ответа с данными сессии"""
    id: int
    question_ids: list[int]  # Список ID вопросов в сессии
    status: str  # "active", "completed", "failed"
    created_at: datetime  # Время создания

    class Config:
        from_attributes = True
