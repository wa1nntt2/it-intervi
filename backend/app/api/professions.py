# API роутер для управления профессиями
# CRUD операции для профессий (Frontend, Backend, etc.)

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.engine import get_db
from app.models.profession import Profession
from app.api.schemas import ProfessionCreate, ProfessionResponse

router = APIRouter(prefix="/professions", tags=["professions"])  # Префикс /api/professions


@router.get("/", response_model=list[ProfessionResponse])
def get_professions(db: Session = Depends(get_db)):
    """
    Получить список всех профессий.
    
    Returns:
        list[ProfessionResponse]: Список всех профессий
    """
    return db.query(Profession).all()


@router.post("/", response_model=ProfessionResponse)
def create_profession(profession: ProfessionCreate, db: Session = Depends(get_db)):
    """
    Создать новую профессию.
    
    Args:
        profession: Данные профессии (name, description)
        db: Сессия базы данных
    
    Returns:
        ProfessionResponse: Созданная профессия
    """
    new_profession = Profession(**profession.model_dump())
    db.add(new_profession)
    db.commit()
    db.refresh(new_profession)
    return new_profession


@router.get("/{profession_id}", response_model=ProfessionResponse)
def get_profession(profession_id: int, db: Session = Depends(get_db)):
    """
    Получить профессию по ID.
    
    Args:
        profession_id: ID профессии
        db: Сессия базы данных
    
    Returns:
        ProfessionResponse: Данные профессии
    
    Raises:
        HTTPException: Если профессия не найдена (404)
    """
    profession = db.query(Profession).filter(Profession.id == profession_id).first()
    if not profession:
        raise HTTPException(status_code=404, detail="Профессия не найдена")
    return profession
