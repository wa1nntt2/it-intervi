from fastapi import APIRouter, Depends, HTTPException, status, Header, Body
from sqlalchemy.orm import Session, joinedload
from datetime import datetime, timedelta

from app.database.engine import get_db
from app.models.user import User
from app.models.user_progress import UserProgress, Achievement, UserAchievement
from app.models.question import Question
from app.models.answer import Answer
from app.models.session import Session as SessionModel
from app.api.schemas import UserResponse
from app.api.auth import get_current_user
from app.core.security import decode_token

router = APIRouter(prefix="/progress", tags=["progress"])

# Система уровней
LEVELS = {
    1: ("Intern", 0),
    2: ("Junior", 500),
    3: ("Middle", 1500),
    4: ("Senior", 3500),
    5: ("Lead", 6500),
    6: ("Architect", 10500),
}

def get_level_info(level: int):
    if level > 6:
        return ("Legend", 10500, float('inf'))
    current_name, current_xp = LEVELS[level]
    next_xp = LEVELS[min(level + 1, 6)][1] if level < 6 else float('inf')
    return (current_name, current_xp, next_xp)

def calculate_level(xp: int):
    level = 1
    for lvl, (name, req_xp) in sorted(LEVELS.items(), key=lambda x: x[0]):
        if xp >= req_xp:
            level = lvl
        else:
            break
    return level

def get_or_create_progress(db: Session, user_id: int) -> UserProgress:
    progress = db.query(UserProgress).filter(UserProgress.user_id == user_id).first()
    if not progress:
        progress = UserProgress(user_id=user_id)
        db.add(progress)
        db.commit()
        db.refresh(progress)
    return progress

def check_achievements(db: Session, user: User, progress: UserProgress):
    """Проверка и разблокировка достижений"""
    achievements = db.query(Achievement).all()
    unlocked = []
    
    for achievement in achievements:
        # Проверяем уже разблокировано ли
        exists = db.query(UserAchievement).filter(
            UserAchievement.user_id == user.id,
            UserAchievement.achievement_id == achievement.id
        ).first()
        if exists:
            continue
        
        # Проверяем условие
        value = 0
        if achievement.requirement_type == "sessions_completed":
            value = progress.completed_sessions
        elif achievement.requirement_type == "correct_answers":
            value = progress.total_correct_answers
        elif achievement.requirement_type == "streak":
            value = progress.best_streak
        elif achievement.requirement_type == "perfect_score":
            value = progress.completed_sessions  # Упрощённо
        
        if value >= achievement.requirement_value:
            # Разблокируем достижение
            user_achievement = UserAchievement(
                user_id=user.id,
                achievement_id=achievement.id
            )
            db.add(user_achievement)
            
            # Начисляем XP
            progress.xp += achievement.xp_reward
            new_level = calculate_level(progress.xp)
            if new_level > progress.level:
                progress.level = new_level
                progress.title = get_level_info(new_level)[0]
            
            unlocked.append({
                "name": achievement.name,
                "icon": achievement.icon,
                "xp_reward": achievement.xp_reward
            })
    
    if unlocked:
        db.commit()
    
    return unlocked

@router.get("/me")
async def get_my_progress(
    authorization: str = Header(None, alias="Authorization"),
    db: Session = Depends(get_db)
):
    """Получить прогресс текущего пользователя"""
    from app.api.auth import get_current_user
    
    # Извлекаем токен из "Bearer <token>"
    token = None
    if authorization and authorization.startswith("Bearer "):
        token = authorization[7:]
    
    if not token:
        raise HTTPException(status_code=401, detail="Требуется авторизация")
    
    try:
        user = await get_current_user(token, db)
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Ошибка авторизации: {str(e)}")
    
    progress = get_or_create_progress(db, user.id)
    
    level_name, level_start, level_end = get_level_info(progress.level)
    progress_in_level = progress.xp - level_start
    progress_to_next = level_end - level_start if level_end != float('inf') else 0
    progress_percent = (progress_in_level / progress_to_next * 100) if progress_to_next > 0 else 100
    
    # Полученные достижения
    user_achievements = db.query(UserAchievement).filter(UserAchievement.user_id == user.id).all()
    achievement_ids = [ua.achievement_id for ua in user_achievements]
    all_achievements = db.query(Achievement).all()
    
    achievements_list = []
    for ach in all_achievements:
        achievements_list.append({
            "id": ach.id,
            "name": ach.name,
            "description": ach.description,
            "icon": ach.icon,
            "xp_reward": ach.xp_reward,
            "unlocked": ach.id in achievement_ids
        })
    
    return {
        "user_id": user.id,
        "xp": progress.xp,
        "level": progress.level,
        "level_name": level_name,
        "level_progress": round(progress_percent, 1),
        "title": progress.title,
        "stats": {
            "total_sessions": progress.total_sessions,
            "completed_sessions": progress.completed_sessions,
            "total_correct": progress.total_correct_answers,
            "total_answered": progress.total_questions_answered,
            "best_streak": progress.best_streak
        },
        "achievements": achievements_list,
        "badges": progress.badges
    }

@router.post("/add-xp")
async def add_xp(
    xp_amount: int = Body(..., embed=True),
    correct_answers: int = Body(..., embed=True),
    total_questions: int = Body(..., embed=True),
    authorization: str = Header(None, alias="Authorization"),
    db: Session = Depends(get_db)
):
    """Добавить XP за сессию"""
    from app.api.auth import get_current_user
    
    # Извлекаем токен из "Bearer <token>"
    token = None
    if authorization and authorization.startswith("Bearer "):
        token = authorization[7:]
    
    if not token:
        raise HTTPException(status_code=401, detail="Требуется авторизация")
    
    try:
        user = await get_current_user(token, db)
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Ошибка авторизации: {str(e)}")
    
    progress = get_or_create_progress(db, user.id)
    
    # Начисляем XP
    progress.xp += xp_amount
    
    # Обновляем статистику
    progress.total_sessions += 1
    progress.completed_sessions += 1
    progress.total_correct_answers += correct_answers
    progress.total_questions_answered += total_questions
    progress.last_session_at = datetime.utcnow()
    
    # Проверяем стрик (упрощённо)
    if correct_answers == total_questions:
        progress.current_streak += 1
        if progress.current_streak > progress.best_streak:
            progress.best_streak = progress.current_streak
    else:
        progress.current_streak = 0
    
    # Обновляем уровень
    new_level = calculate_level(progress.xp)
    if new_level > progress.level:
        progress.level = new_level
        progress.title = get_level_info(new_level)[0]
    
    # Проверяем достижения
    unlocked_achievements = check_achievements(db, user, progress)
    
    db.commit()
    
    return {
        "xp_added": xp_amount,
        "new_xp": progress.xp,
        "new_level": progress.level,
        "level_up": new_level > progress.level - 1,
        "unlocked_achievements": unlocked_achievements
    }

@router.get("/achievements")
def get_all_achievements(db: Session = Depends(get_db)):
    """Получить все достижения"""
    achievements = db.query(Achievement).all()
    return [
        {
            "id": a.id,
            "name": a.name,
            "description": a.description,
            "icon": a.icon,
            "xp_reward": a.xp_reward,
            "category": a.category,
            "requirement": f"{a.requirement_type}: {a.requirement_value}"
        }
        for a in achievements
    ]


@router.get("/wrong-answers")
def get_wrong_answers(
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Получить неправильные ответы пользователя"""
    # Получаем ответы пользователя где is_correct = False
    wrong_answers = db.query(Answer).options(
        joinedload(Answer.question)
    ).filter(
        Answer.user_id == current_user.id,
        Answer.is_correct == False
    ).order_by(Answer.created_at.desc()).limit(limit).all()
    
    result = []
    for answer in wrong_answers:
        question = answer.question
        if not question:
            continue
            
        # Получаем категории вопроса
        categories = [c.name for c in question.categories]
        
        result.append({
            "question_id": question.id,
            "question_text": question.text,
            "your_answer": question.options[answer.selected_option] if answer.selected_option is not None else None,
            "correct_answer": question.options[question.correct_option] if question.correct_option is not None else None,
            "explanation": question.explanation,
            "category": categories[0] if categories else None,
            "answered_at": answer.created_at.isoformat() if answer.created_at else None
        })
    
    return result
