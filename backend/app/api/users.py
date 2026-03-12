# API роутер для управления пользователями
# Административные операции: список, просмотр, удаление

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from app.database.engine import get_db
from app.models.user import User
from app.models.session import Session as SessionModel
from app.api.schemas import UserResponse

router = APIRouter(prefix="/users", tags=["users"])  # Префикс /api/users


@router.get("/", response_model=list[UserResponse])
def get_users(
    skip: int = 0,  # Пропуск первых N записей (для пагинации)
    limit: int = 100,  # Максимальное количество записей
    db: Session = Depends(get_db)
):
    """
    Получить список всех пользователей с пагинацией.
    
    Args:
        skip: Количество записей для пропуска
        limit: Максимальное количество записей
        db: Сессия базы данных
    
    Returns:
        list[UserResponse]: Список пользователей
    """
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Получить пользователя по ID.
    
    Args:
        user_id: ID пользователя
        db: Сессия базы данных
    
    Returns:
        UserResponse: Данные пользователя
    
    Raises:
        HTTPException: Если пользователь не найден (404)
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Удалить пользователя и все его сессии.
    
    Args:
        user_id: ID пользователя
        db: Сессия базы данных
    
    Returns:
        dict: Сообщение об успешном удалении
    
    Raises:
        HTTPException: Если пользователь не найден (404)
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    # Удаляем сессии пользователя (каскадное удаление)
    db.query(SessionModel).filter(SessionModel.user_id == user_id).delete()

    # Удаляем пользователя
    db.delete(user)
    db.commit()

    return {"message": "Пользователь удалён"}
