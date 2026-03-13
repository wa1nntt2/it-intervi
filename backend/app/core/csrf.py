"""
CSRF Protection модуль.
Защищает state-changing операции от CSRF атак.
Использует double submit cookie pattern.
"""

import secrets
from typing import Optional
from fastapi import Request, Response, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.config import settings


class CSRFProtect:
    """
    CSRF защита для FastAPI.
    
    Реализует double submit cookie pattern:
    1. Сервер устанавливает CSRF токен в cookie (httponly, samesite=strict)
    2. Клиент должен отправить этот токен в заголовке X-CSRF-Token
    3. Сервер сравнивает токены из cookie и заголовка
    """
    
    CSRF_COOKIE_NAME = "csrf_token"
    CSRF_HEADER_NAME = "x-csrf-token"
    
    def __init__(self):
        self.security = HTTPBearer(auto_error=False)
    
    def generate_csrf_token(self) -> str:
        """Генерация нового CSRF токена"""
        return secrets.token_urlsafe(32)
    
    def set_csrf_cookie(self, response: Response, token: str) -> None:
        """
        Установка CSRF токена в cookie.
        
        Args:
            response: HTTP ответ
            token: CSRF токен
        """
        response.set_cookie(
            key=self.CSRF_COOKIE_NAME,
            value=token,
            httponly=True,
            secure=not settings.DEBUG,
            samesite="strict",
            max_age=3600,  # 1 час
            path="/",
        )
    
    def get_csrf_token_from_cookie(self, request: Request) -> Optional[str]:
        """Получение CSRF токена из cookie"""
        return request.cookies.get(self.CSRF_COOKIE_NAME)
    
    def get_csrf_token_from_header(self, request: Request) -> Optional[str]:
        """Получение CSRF токена из заголовка"""
        return request.headers.get(self.CSRF_HEADER_NAME)
    
    async def validate_csrf(self, request: Request) -> bool:
        """
        Валидация CSRF токена.
        
        Args:
            request: HTTP запрос
            
        Returns:
            True если токен валиден
            
        Raises:
            HTTPException: Если токен невалиден
        """
        cookie_token = self.get_csrf_token_from_cookie(request)
        header_token = self.get_csrf_token_from_header(request)
        
        if not cookie_token:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="CSRF токен не найден в cookies"
            )
        
        if not header_token:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"CSRF токен не найден в заголовке {self.CSRF_HEADER_NAME}"
            )
        
        if not secrets.compare_digest(cookie_token, header_token):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="CSRF токены не совпадают"
            )
        
        return True


# Глобальный экземпляр
csrf_protect = CSRFProtect()


# Dependency для защиты endpoints
async def csrf_required(request: Request) -> bool:
    """
    Dependency для защиты endpoints от CSRF.
    Используется в FastAPI endpoints через Depends().
    
    Usage:
        @router.post("/protected")
        async def protected_endpoint(_: bool = Depends(csrf_required)):
            ...
    """
    return await csrf_protect.validate_csrf(request)
