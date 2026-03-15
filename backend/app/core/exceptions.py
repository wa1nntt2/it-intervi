# Кастомные исключения для API
# Унифицированный формат ошибок для всего приложения

from fastapi import HTTPException, status
from typing import Any, Optional, Dict, List


class APIException(HTTPException):
    """
    Базовое исключение для API с унифицированным форматом ошибок.
    
    Пример ответа:
    {
        "error": {
            "code": "VALIDATION_ERROR",
            "message": "Ошибка валидации данных",
            "details": {...}
        }
    }
    """
    
    def __init__(
        self,
        message: str,
        code: str = "API_ERROR",
        status_code: int = 400,
        details: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ):
        self.code = code
        self.details = details
        
        super().__init__(
            status_code=status_code,
            detail={
                "error": {
                    "code": code,
                    "message": message,
                    "details": details or {}
                }
            },
            headers=headers
        )


class ValidationException(APIException):
    """Исключение для ошибок валидации данных"""
    
    def __init__(
        self,
        message: str = "Ошибка валидации данных",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            code="VALIDATION_ERROR",
            status_code=status.HTTP_400_BAD_REQUEST,
            details=details
        )


class NotFoundException(APIException):
    """Исключение для ресурса не найден"""
    
    def __init__(
        self,
        resource: str = "Ресурс",
        resource_id: Optional[Any] = None
    ):
        message = f"{resource} не найден"
        if resource_id:
            message += f" (ID: {resource_id})"
            
        super().__init__(
            message=message,
            code="NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND,
            details={"resource": resource, "resource_id": resource_id}
        )


class UnauthorizedException(APIException):
    """Исключение для ошибок аутентификации"""
    
    def __init__(
        self,
        message: str = "Необходима аутентификация",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            code="UNAUTHORIZED",
            status_code=status.HTTP_401_UNAUTHORIZED,
            details=details,
            headers={"WWW-Authenticate": "Bearer"}
        )


class ForbiddenException(APIException):
    """Исключение для ошибок авторизации (недостаточно прав)"""
    
    def __init__(
        self,
        message: str = "Недостаточно прав для выполнения действия",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            code="FORBIDDEN",
            status_code=status.HTTP_403_FORBIDDEN,
            details=details
        )


class ConflictException(APIException):
    """Исключение для конфликтов (например, дубликат ресурса)"""
    
    def __init__(
        self,
        message: str = "Конфликт данных",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            code="CONFLICT",
            status_code=status.HTTP_409_CONFLICT,
            details=details
        )


class TooManyRequestsException(APIException):
    """Исключение для превышения лимита запросов"""
    
    def __init__(
        self,
        message: str = "Слишком много запросов",
        retry_after: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        headers = {}
        if retry_after:
            headers["Retry-After"] = str(retry_after)
            
        super().__init__(
            message=message,
            code="TOO_MANY_REQUESTS",
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            details=details,
            headers=headers if headers else None
        )


class InternalServerException(APIException):
    """Исключение для внутренних ошибок сервера"""
    
    def __init__(
        self,
        message: str = "Внутренняя ошибка сервера",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            code="INTERNAL_ERROR",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details=details
        )


class ImportException(APIException):
    """Исключение для ошибок импорта данных"""
    
    def __init__(
        self,
        message: str = "Ошибка импорта данных",
        errors: Optional[List[Dict[str, Any]]] = None
    ):
        super().__init__(
            message=message,
            code="IMPORT_ERROR",
            status_code=status.HTTP_400_BAD_REQUEST,
            details={"errors": errors or []}
        )
