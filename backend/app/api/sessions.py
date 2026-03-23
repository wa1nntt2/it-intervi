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
from app.api.deps import get_current_user_optional
from app.core.config import settings
from app.core.logging_config import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/sessions", tags=["sessions"])  # Префикс /api/sessions


class SessionCreate(BaseModel):
    """Схема для создания новой сессии"""
    profession_id: int  # ID профессии для тестирования
    difficulty: Optional[str] = "junior"  # "intern", "junior", "middle"
    mode: Optional[str] = "practice"  # "practice", "learning", "timed", "exam"
    time_limit: Optional[int] = None  # Лимит времени в секундах (для timed mode)
    category_ids: Optional[list[int]] = None  # ID категорий для фильтрации вопросов
    total_questions: Optional[int] = None  # Общее количество вопросов в сессии


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
    """
    logger.debug("📊 Запрос статистики сессий")
    
    from sqlalchemy import case

    total = db.query(func.count(Session.id)).scalar() or 0
    active = db.query(func.count(Session.id)).filter(Session.status == "active").scalar() or 0
    completed = db.query(func.count(Session.id)).filter(Session.status == "completed").scalar() or 0
    failed = db.query(func.count(Session.id)).filter(Session.status == "failed").scalar() or 0

    # Средняя оценка в процентах
    average_score_query = db.query(
        func.avg(
            case(
                (
                    Session.status == "completed",
                    case(
                        (func.json_array_length(Session.question_ids) > 0,
                         (Session.score * 100.0) / func.json_array_length(Session.question_ids)),
                        else_=0
                    )
                ),
                else_=None
            )
        ).filter(Session.status == "completed")
    ).scalar()

    average_score = round(average_score_query, 1) if average_score_query is not None else 0

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

    logger.debug(f"✅ Статистика: total={total}, active={active}, completed={completed}")
    
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
    """
    logger.debug(f"📖 Запрос сессий: status={status_filter}, page={page}, page_size={page_size}")
    
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

    logger.debug(f"✅ Получено {len(sessions)} сессий из {total} всего")
    
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
            mode=s.mode,
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
def create_session(
    session_data: SessionCreate,
    db: Session = Depends(get_db),
    user: Optional[User] = Depends(get_current_user_optional)
):
    """
    Создать новую сессию тестирования.
    """
    logger.info(
        f"🎯 Создание сессии для профессии ID={session_data.profession_id}",
        extra={
            "user_id": user.id if user else None,
            "difficulty": session_data.difficulty,
            "mode": session_data.mode,
            "total_questions": session_data.total_questions
        }
    )
    
    import random

    # Фильтрация вопросов по профессии и сложности
    query = db.query(Question).filter(
        Question.profession_id == session_data.profession_id
    )

    # Фильтр по сложности
    if session_data.difficulty:
        query = query.filter(Question.difficulty == session_data.difficulty)

    # Фильтр по категориям (если указаны)
    if session_data.category_ids and len(session_data.category_ids) > 0:
        from app.models.category import question_categories
        query = query.join(question_categories).filter(
            question_categories.c.category_id.in_(session_data.category_ids)
        )

    questions = query.all()
    logger.debug(f"📊 Найдено {len(questions)} вопросов для профессии")

    # Если нет вопросов выбранной сложности, берем все вопросы профессии
    if not questions:
        logger.warning(f"⚠️  Нет вопросов выбранной сложности {session_data.difficulty}, берем все")
        questions = db.query(Question).filter(
            Question.profession_id == session_data.profession_id
        ).all()

    # Перемешиваем вопросы и берём первые N
    num_questions = session_data.total_questions if session_data.total_questions else settings.QUESTIONS_PER_SESSION
    random.shuffle(questions)
    selected_questions = questions[:num_questions]

    new_session = Session(
        profession_id=session_data.profession_id,
        user_id=user.id if user else None,
        question_ids=[q.id for q in selected_questions],
        status="active",
        mode=session_data.mode or "practice",
        time_limit=session_data.time_limit
    )
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    
    logger.info(f"✅ Сессия создана: ID={new_session.id}, вопросов={len(selected_questions)}")
    return new_session


@router.get("/{session_id}", response_model=SessionResponse)
def get_session(session_id: int, db: Session = Depends(get_db)):
    """
    Получить сессию по ID.
    """
    logger.debug(f"📖 Запрос сессии ID={session_id}")
    
    session = db.query(Session).filter(Session.id == session_id).first()
    if not session:
        logger.warning(f"⚠️  Сессия не найдена: ID={session_id}")
        raise HTTPException(status_code=404, detail="Сессия не найдена")
    
    logger.debug(f"✅ Сессия получена: ID={session.id}")
    return session


class CompleteSessionRequest(BaseModel):
    """Схема запроса для завершения сессии"""
    score: int = 0  # Количество правильных ответов


@router.post("/{session_id}/complete")
def complete_session(session_id: int, request: CompleteSessionRequest, db: Session = Depends(get_db)):
    """
    Завершить сессию с указанием результата.
    """
    logger.info(f"🏁 Завершение сессии ID={session_id}, score={request.score}")
    
    session = db.query(Session).filter(Session.id == session_id).first()
    if not session:
        logger.warning(f"⚠️  Сессия не найдена для завершения: ID={session_id}")
        raise HTTPException(status_code=404, detail="Сессия не найдена")
    
    session.status = "completed"
    session.score = request.score
    session.completed_at = datetime.utcnow()
    db.commit()
    
    logger.info(f"✅ Сессия завершена: ID={session_id}, score={request.score}/{len(session.question_ids)}")
    return {"message": "Сессия завершена"}


@router.delete("/{session_id}")
def delete_session(session_id: int, db: Session = Depends(get_db)):
    """
    Удалить сессию.
    """
    logger.info(f"🗑️  Удаление сессии ID={session_id}")
    
    session = db.query(Session).filter(Session.id == session_id).first()
    if not session:
        logger.warning(f"⚠️  Сессия не найдена для удаления: ID={session_id}")
        raise HTTPException(status_code=404, detail="Сессия не найдена")
    
    db.delete(session)
    db.commit()
    
    logger.info(f"✅ Сессия удалена: ID={session_id}")
    return {"message": "Сессия удалена"}
