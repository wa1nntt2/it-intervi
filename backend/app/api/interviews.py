# API для категорий и конфигураций собеседований

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from app.database.engine import get_db
from app.models.category import Category
from app.models.interview_config import InterviewConfig
from app.models.profession import Profession
from app.models.question import Question
from app.models.session import Session
from app.api.auth import get_current_user
from app.models.user import User

router = APIRouter(tags=["Categories & Interviews"])


# === Категории ===

class CategoryResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    profession_id: int

    class Config:
        from_attributes = True


class CategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None
    profession_id: int


@router.get("/professions/{profession_id}/categories", response_model=List[CategoryResponse])
def get_categories_by_profession(profession_id: int, db: Session = Depends(get_db)):
    """Получить все категории для профессии"""
    categories = db.query(Category).filter(Category.profession_id == profession_id).all()
    return categories


@router.get("/categories/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    """Получить категорию по ID"""
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    return category


@router.post("/categories", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    category_data: CategoryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Создать новую категорию (только для админов)"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Только администраторы могут создавать категории")
    
    # Проверка существования профессии
    profession = db.query(Profession).filter(Profession.id == category_data.profession_id).first()
    if not profession:
        raise HTTPException(status_code=404, detail="Профессия не найдена")
    
    # Проверка уникальности названия в рамках профессии
    existing = db.query(Category).filter(
        Category.name == category_data.name,
        Category.profession_id == category_data.profession_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Категория с таким названием уже существует")
    
    category = Category(**category_data.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@router.put("/categories/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    category_data: CategoryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Обновить категорию (только для админов)"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Только администраторы могут редактировать категории")
    
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    
    category.name = category_data.name
    category.description = category_data.description
    category.profession_id = category_data.profession_id
    
    db.commit()
    db.refresh(category)
    return category


@router.delete("/categories/{category_id}")
def delete_category(
    category_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Удалить категорию (только для админов)"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Только администраторы могут удалять категории")
    
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    
    db.delete(category)
    db.commit()
    return {"message": "Категория удалена"}


# === Конфигурации собеседований ===

class CategoryConfigItem(BaseModel):
    category_id: int
    question_count: int


class InterviewConfigCreate(BaseModel):
    name: str
    description: Optional[str] = None
    profession_id: int
    difficulty: str = "junior"
    category_configs: List[CategoryConfigItem] = []
    is_public: bool = False


class InterviewConfigResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    profession_id: int
    profession_name: str
    user_id: Optional[int] = None
    difficulty: str
    category_configs: List[CategoryConfigItem]
    is_public: bool
    is_default: bool

    class Config:
        from_attributes = True


@router.get("/professions/{profession_id}/interview-configs", response_model=List[InterviewConfigResponse])
def get_interview_configs_by_profession(
    profession_id: int,
    include_public: bool = True,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Получить все конфигурации для профессии (свои и публичные)"""
    configs = db.query(InterviewConfig).filter(
        InterviewConfig.profession_id == profession_id,
        (InterviewConfig.user_id == current_user.id) | (InterviewConfig.is_public == True)
    ).all()
    
    result = []
    for config in configs:
        profession = db.query(Profession).filter(Profession.id == config.profession_id).first()
        result.append({
            "id": config.id,
            "name": config.name,
            "description": config.description,
            "profession_id": config.profession_id,
            "profession_name": profession.name if profession else "",
            "user_id": config.user_id,
            "difficulty": config.difficulty,
            "category_configs": config.category_configs,
            "is_public": config.is_public,
            "is_default": config.is_default
        })
    
    return result


@router.get("/interview-configs/{config_id}", response_model=InterviewConfigResponse)
def get_interview_config(
    config_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Получить конфигурацию по ID"""
    config = db.query(InterviewConfig).filter(InterviewConfig.id == config_id).first()
    if not config:
        raise HTTPException(status_code=404, detail="Конфигурация не найдена")
    
    # Проверка доступа
    if config.user_id and config.user_id != current_user.id and not config.is_public and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Нет доступа к этой конфигурации")
    
    profession = db.query(Profession).filter(Profession.id == config.profession_id).first()
    return {
        "id": config.id,
        "name": config.name,
        "description": config.description,
        "profession_id": config.profession_id,
        "profession_name": profession.name if profession else "",
        "user_id": config.user_id,
        "difficulty": config.difficulty,
        "category_configs": config.category_configs,
        "is_public": config.is_public,
        "is_default": config.is_default
    }


@router.post("/interview-configs", response_model=InterviewConfigResponse, status_code=status.HTTP_201_CREATED)
def create_interview_config(
    config_data: InterviewConfigCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Создать новую конфигурацию собеседования"""
    # Проверка существования профессии
    profession = db.query(Profession).filter(Profession.id == config_data.profession_id).first()
    if not profession:
        raise HTTPException(status_code=404, detail="Профессия не найдена")
    
    # Создание конфигурации
    config = InterviewConfig(
        name=config_data.name,
        description=config_data.description,
        profession_id=config_data.profession_id,
        user_id=current_user.id,
        difficulty=config_data.difficulty,
        category_configs=[{"category_id": c.category_id, "question_count": c.question_count} for c in config_data.category_configs],
        is_public=config_data.is_public,
        is_default=False
    )
    
    db.add(config)
    db.commit()
    db.refresh(config)
    
    return {
        "id": config.id,
        "name": config.name,
        "description": config.description,
        "profession_id": config.profession_id,
        "profession_name": profession.name,
        "user_id": config.user_id,
        "difficulty": config.difficulty,
        "category_configs": config.category_configs,
        "is_public": config.is_public,
        "is_default": config.is_default
    }


@router.delete("/interview-configs/{config_id}")
def delete_interview_config(
    config_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Удалить конфигурацию собеседования"""
    config = db.query(InterviewConfig).filter(InterviewConfig.id == config_id).first()
    if not config:
        raise HTTPException(status_code=404, detail="Конфигурация не найдена")
    
    # Проверка прав
    if config.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Нет прав на удаление этой конфигурации")
    
    db.delete(config)
    db.commit()
    return {"message": "Конфигурация удалена"}


@router.put("/interview-configs/{config_id}", response_model=InterviewConfigResponse)
def update_interview_config(
    config_id: int,
    config_data: InterviewConfigCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Обновить конфигурацию собеседования"""
    config = db.query(InterviewConfig).filter(InterviewConfig.id == config_id).first()
    if not config:
        raise HTTPException(status_code=404, detail="Конфигурация не найдена")
    
    # Проверка прав
    if config.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Нет прав на редактирование этой конфигурации")
    
    # Обновление
    config.name = config_data.name
    config.description = config_data.description
    config.profession_id = config_data.profession_id
    config.difficulty = config_data.difficulty
    config.category_configs = [{"category_id": c.category_id, "question_count": c.question_count} for c in config_data.category_configs]
    config.is_public = config_data.is_public
    
    db.commit()
    db.refresh(config)
    
    profession = db.query(Profession).filter(Profession.id == config.profession_id).first()
    return {
        "id": config.id,
        "name": config.name,
        "description": config.description,
        "profession_id": config.profession_id,
        "profession_name": profession.name if profession else "",
        "user_id": config.user_id,
        "difficulty": config.difficulty,
        "category_configs": config.category_configs,
        "is_public": config.is_public,
        "is_default": config.is_default
    }


# === Создание сессии из конфигурации ===

class SessionCreateFromConfig(BaseModel):
    config_id: int


class SessionCreateResponse(BaseModel):
    session_id: int
    question_ids: List[int]
    total_questions: int


@router.post("/sessions/from-config", response_model=SessionCreateResponse)
def create_session_from_config(
    session_data: SessionCreateFromConfig,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Создать сессию из конфигурации собеседования"""
    from app.models.session import Session
    import random
    
    config = db.query(InterviewConfig).filter(InterviewConfig.id == session_data.config_id).first()
    if not config:
        raise HTTPException(status_code=404, detail="Конфигурация не найдена")
    
    # Проверка доступа
    if config.user_id and config.user_id != current_user.id and not config.is_public and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Нет доступа к этой конфигурации")
    
    # Сбор вопросов по категориям
    all_question_ids = []
    
    for cat_config in config.category_configs:
        category_id = cat_config["category_id"]
        question_count = cat_config["question_count"]
        
        # Получаем вопросы категории с фильтром по сложности
        category = db.query(Category).filter(Category.id == category_id).first()
        if not category:
            continue
        
        questions_query = db.query(Question).filter(
            Question.categories.any(id=category_id),
            Question.profession_id == config.profession_id
        )
        
        # Фильтр по сложности если указан
        if config.difficulty:
            questions_query = questions_query.filter(Question.difficulty == config.difficulty)
        
        questions = questions_query.all()
        
        # Выбираем случайные вопросы
        selected = random.sample(questions, min(question_count, len(questions)))
        all_question_ids.extend([q.id for q in selected])
    
    if not all_question_ids:
        raise HTTPException(status_code=400, detail="Не найдено вопросов для выбранной конфигурации")
    
    # Перемешиваем вопросы
    random.shuffle(all_question_ids)
    
    # Создаем сессию
    session = Session(
        profession_id=config.profession_id,
        user_id=current_user.id,
        question_ids=all_question_ids,
        status="active"
    )
    
    db.add(session)
    db.commit()
    db.refresh(session)
    
    return {
        "session_id": session.id,
        "question_ids": session.question_ids,
        "total_questions": len(session.question_ids)
    }
