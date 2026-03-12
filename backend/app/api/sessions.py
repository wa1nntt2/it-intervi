# API роутер для управления сессиями тестирования
# Создание сессий, получение статистики, завершение тестов

from fastapi import APIRouter, Depends, HTTPException, status, Header, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, extract
from typing import Optional
from datetime import datetime, date
from pydantic import BaseModel
from math import ceil

from app.database.engine import get_db
from app.models.session import Session
from app.models.question import Question
from app.models.user import User
from app.models.profession import Profession
from app.api.schemas import SessionResponse, PaginatedSessions, SessionListItem
from app.core.security import decode_token
from app.api.auth import get_current_user as auth_get_current_user
from app.core.config import settings

router = APIRouter(prefix="/sessions", tags=["sessions"])  # Префикс /api/sessions


class SessionCreate(BaseModel):
    """Схема для создания новой сессии"""
    profession_id: int  # ID профессии для тестирования
    difficulty: Optional[str] = "junior"  # "intern", "junior", "middle"


async def get_current_user(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)) -> Optional[User]:
    """
    Получение текущего пользователя из JWT токена.
    Использует функцию из auth модуля.

    Args:
        authorization: Заголовок Authorization с JWT токеном
        db: Сессия базы данных

    Returns:
        User или None если токен невалиден
    """
    if not authorization or not authorization.startswith("Bearer "):
        return None
    token = authorization.split(" ")[1]
    try:
        user = await auth_get_current_user(token, db)
        return user
    except Exception:
        return None


class SessionStatsResponse(BaseModel):
    """Схема ответа со статистикой по сессиям"""
    total: int  # Всего сессий
    active: int  # Активных сессий
    completed: int  # Завершенных сессий
    failed: int  # Проваленных сессий
    average_score: float  # Средний балл в процентах
    today_sessions: int  # Сессий сегодня
    this_week_sessions: int  # Сессий за неделю
    this_month_sessions: int  # Сессий за месяц


@router.get("/stats", response_model=SessionStatsResponse)
def get_session_stats(
    db: Session = Depends(get_db),
    authorization: Optional[str] = Header(None)
):
    """
    Получить статистику по сессиям.
    
    Вычисляет:
    - Общее количество сессий по статусам
    - Средний балл в процентах
    - Количество сессий за сегодня/неделю/месяц
    
    Args:
        db: Сессия базы данных
        authorization: JWT токен (опционально)
    
    Returns:
        SessionStatsResponse: Статистика по сессиям
    """
    total = db.query(func.count(Session.id)).scalar() or 0
    active = db.query(func.count(Session.id)).filter(Session.status == "active").scalar() or 0
    completed = db.query(func.count(Session.id)).filter(Session.status == "completed").scalar() or 0
    failed = db.query(func.count(Session.id)).filter(Session.status == "failed").scalar() or 0

    # Средняя оценка в процентах
    # Для каждой завершённой сессии считаем процент: (score / len(question_ids)) * 100
    completed_sessions = db.query(Session).filter(Session.status == "completed").all()
    if completed_sessions:
        percentages = []
        for session in completed_sessions:
            total_questions = len(session.question_ids)
            if total_questions > 0:
                percentage = (session.score / total_questions) * 100
                percentages.append(percentage)
        average_score = round(sum(percentages) / len(percentages), 1) if percentages else 0
    else:
        average_score = 0

    # Сегодня
    today = datetime.now().date()
    today_sessions = db.query(func.count(Session.id)).filter(
        func.date(Session.created_at) == today
    ).scalar() or 0

    # Эта неделя
    from datetime import timedelta
    week_ago = today - timedelta(days=7)
    this_week_sessions = db.query(func.count(Session.id)).filter(
        Session.created_at >= week_ago
    ).scalar() or 0

    # Этот месяц
    month_ago = today - timedelta(days=30)
    this_month_sessions = db.query(func.count(Session.id)).filter(
        Session.created_at >= month_ago
    ).scalar() or 0

    return SessionStatsResponse(
        total=total,
        active=active,
        completed=completed,
        failed=failed,
        average_score=average_score,
        today_sessions=today_sessions,
        this_week_sessions=this_week_sessions,
        this_month_sessions=this_month_sessions
    )


@router.get("/", response_model=PaginatedSessions)
def get_sessions(
    status_filter: Optional[str] = Query(None, alias="status"),  # Фильтр по статусу
    profession_id: Optional[int] = Query(None),  # Фильтр по профессии
    user_id: Optional[int] = Query(None),  # Фильтр по пользователю
    date_from: Optional[date] = Query(None),  # Фильтр по дате (от)
    date_to: Optional[date] = Query(None),  # Фильтр по дате (до)
    page: int = Query(1, ge=1),  # Номер страницы
    page_size: int = Query(20, ge=1, le=100),  # Размер страницы
    db: Session = Depends(get_db)
):
    """
    Получить список сессий с фильтрами и пагинацией.

    Доступные фильтры:
    - status: "active", "completed", "failed"
    - profession_id: ID профессии
    - user_id: ID пользователя
    - date_from/date_to: Диапазон дат

    Args:
        status_filter: Фильтр по статусу
        profession_id: Фильтр по профессии
        user_id: Фильтр по пользователю
        date_from: Дата начала диапазона
        date_to: Дата конца диапазона
        page: Номер страницы
        page_size: Размер страницы (1-100)
        db: Сессия базы данных

    Returns:
        PaginatedSessions: Пагинированный список сессий
    """
    query = db.query(Session).options(
        joinedload(Session.profession),
        joinedload(Session.user)
    ).join(Profession, Session.profession_id == Profession.id).outerjoin(User, Session.user_id == User.id)

    if status_filter:
        query = query.filter(Session.status == status_filter)
    if profession_id:
        query = query.filter(Session.profession_id == profession_id)
    if user_id:
        query = query.filter(Session.user_id == user_id)
    if date_from:
        query = query.filter(func.date(Session.created_at) >= date_from)
    if date_to:
        query = query.filter(func.date(Session.created_at) <= date_to)

    # Получаем общее количество
    total = query.count()
    total_pages = ceil(total / page_size) if total > 0 else 1
    
    # Применяем пагинацию
    offset = (page - 1) * page_size
    sessions = query.order_by(Session.created_at.desc()).offset(offset).limit(page_size).all()

    result = []
    for s in sessions:
        result.append(SessionListItem(
            id=s.id,
            profession_id=s.profession_id,
            profession_name=s.profession.name,
            user_id=s.user_id,
            user_email=s.user.email if s.user else None,
            question_ids=s.question_ids,
            status=s.status,
            score=s.score,
            created_at=s.created_at,
            completed_at=s.completed_at
        ))

    return PaginatedSessions(
        items=result,
        meta={
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages
        }
    )


@router.post("/", response_model=SessionResponse)
def create_session(session_data: SessionCreate, db: Session = Depends(get_db), authorization: Optional[str] = Header(None)):
    """
    Создать новую сессию тестирования.
    
    Выбирает 20 случайных вопросов по профессии и сложности.
    Если вопросов выбранной сложности нет, берутся все вопросы профессии.
    
    Args:
        session_data: Данные сессии (profession_id, difficulty)
        db: Сессия базы данных
        authorization: JWT токен (опционально)
    
    Returns:
        SessionResponse: Созданная сессия с ID вопросов
    """
    import random

    # Получаем пользователя (функция async, но вызываем в sync контексте)
    # Поэтому используем простой вариант с извлечением токена из заголовка
    user = None
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]
        try:
            from app.core.security import decode_token
            payload = decode_token(token, expected_type="access")
            if payload:
                email = payload.get("sub")
                if email:
                    user = db.query(User).filter(User.email == email).first()
        except Exception:
            pass  # Если токен невалиден, user останется None

    # Фильтрация вопросов по профессии и сложности
    query = db.query(Question).filter(
        Question.profession_id == session_data.profession_id
    )

    # Фильтр по сложности
    if session_data.difficulty:
        query = query.filter(Question.difficulty == session_data.difficulty)

    questions = query.all()

    # Если нет вопросов выбранной сложности, берем все вопросы профессии
    if not questions:
        questions = db.query(Question).filter(
            Question.profession_id == session_data.profession_id
        ).all()

    # Перемешиваем вопросы и берём первые N (из настроек)
    random.shuffle(questions)
    selected_questions = questions[:settings.QUESTIONS_PER_SESSION]

    new_session = Session(
        profession_id=session_data.profession_id,
        user_id=user.id if user else None,
        question_ids=[q.id for q in selected_questions],
        status="active"
    )
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session


@router.get("/{session_id}", response_model=SessionResponse)
def get_session(session_id: int, db: Session = Depends(get_db)):
    """
    Получить сессию по ID.
    
    Args:
        session_id: ID сессии
        db: Сессия базы данных
    
    Returns:
        SessionResponse: Данные сессии
    
    Raises:
        HTTPException: Если сессия не найдена (404)
    """
    session = db.query(Session).filter(Session.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Сессия не найдена")
    return session


class CompleteSessionRequest(BaseModel):
    """Схема запроса для завершения сессии"""
    score: int = 0  # Количество правильных ответов


@router.post("/{session_id}/complete")
def complete_session(session_id: int, request: CompleteSessionRequest, db: Session = Depends(get_db)):
    """
    Завершить сессию с указанием результата.
    
    Args:
        session_id: ID сессии
        request: Данные о результате (score)
        db: Сессия базы данных
    
    Returns:
        dict: Сообщение об успешном завершении
    
    Raises:
        HTTPException: Если сессия не найдена (404)
    """
    session = db.query(Session).filter(Session.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Сессия не найдена")
    session.status = "completed"
    session.score = request.score
    session.completed_at = datetime.utcnow()
    db.commit()
    return {"message": "Сессия завершена"}


@router.delete("/{session_id}")
def delete_session(session_id: int, db: Session = Depends(get_db)):
    """
    Удалить сессию.
    
    Args:
        session_id: ID сессии
        db: Сессия базы данных
    
    Returns:
        dict: Сообщение об успешном удалении
    
    Raises:
        HTTPException: Если сессия не найдена (404)
    """
    session = db.query(Session).filter(Session.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Сессия не найдена")
    db.delete(session)
    db.commit()
    return {"message": "Сессия удалена"}
