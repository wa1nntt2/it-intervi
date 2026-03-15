from collections import OrderedDict
from typing import Any, Optional, Callable
from datetime import datetime, timedelta
import threading
import hashlib
import json
from functools import wraps

from app.core.config import settings


class LRUCache:
    """LRU кэш для кэширования вопросов и других данных"""

    def __init__(self, capacity: Optional[int] = None):
        self.capacity = capacity if capacity is not None else settings.CACHE_CAPACITY
        self.cache: OrderedDict = OrderedDict()
        self.lock = threading.Lock()

    def get(self, key: str) -> Optional[Any]:
        with self.lock:
            if key not in self.cache:
                return None
            self.cache.move_to_end(key)
            return self.cache[key]

    def put(self, key: str, value: Any) -> None:
        with self.lock:
            if key in self.cache:
                self.cache.move_to_end(key)
            self.cache[key] = value
            if len(self.cache) > self.capacity:
                self.cache.popitem(last=False)

    def delete(self, key: str) -> bool:
        with self.lock:
            if key in self.cache:
                del self.cache[key]
                return True
            return False

    def clear(self) -> None:
        with self.lock:
            self.cache.clear()


class CachedValue:
    """Значение с временем жизни"""
    
    def __init__(self, value: Any, ttl_seconds: int):
        self.value = value
        self.expires_at = datetime.now() + timedelta(seconds=ttl_seconds)
    
    def is_expired(self) -> bool:
        return datetime.now() > self.expires_at


class TTLCache:
    """LRU кэш с TTL (time-to-live) для каждого значения"""
    
    def __init__(self, capacity: int = 100):
        self.capacity = capacity
        self.cache: OrderedDict = OrderedDict()
        self.lock = threading.Lock()
    
    def get(self, key: str) -> Optional[Any]:
        with self.lock:
            if key not in self.cache:
                return None
            
            cached = self.cache[key]
            if cached.is_expired():
                del self.cache[key]
                return None
            
            self.cache.move_to_end(key)
            return cached.value
    
    def put(self, key: str, value: Any, ttl_seconds: int = 300) -> None:
        """
        Сохранить значение в кэш.
        
        Args:
            key: Кэш ключ
            value: Значение
            ttl_seconds: Время жизни в секундах (по умолчанию 5 минут)
        """
        with self.lock:
            if key in self.cache:
                self.cache.move_to_end(key)
            
            self.cache[key] = CachedValue(value, ttl_seconds)
            
            # Удаляем старые элементы
            while len(self.cache) > self.capacity:
                self.cache.popitem(last=False)
    
    def delete(self, key: str) -> bool:
        with self.lock:
            if key in self.cache:
                del self.cache[key]
                return True
            return False
    
    def clear(self) -> None:
        with self.lock:
            self.cache.clear()


# Глобальные экземпляры кэшей
cache = LRUCache()  # Для обратной совместимости
ttl_cache = TTLCache(capacity=settings.CACHE_CAPACITY)


def cached(ttl_seconds: int = 300, key_prefix: str = ""):
    """
    Декоратор для кэширования результатов функции.
    
    Args:
        ttl_seconds: Время жизни кэша в секундах
        key_prefix: Префикс для ключа кэша
        
    Пример:
        @cached(ttl_seconds=600, key_prefix="questions")
        def get_questions(profession_id: int):
            ...
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Генерируем ключ из аргументов
            key_data = {
                "func": func.__qualname__,
                "args": args,
                "kwargs": kwargs
            }
            key_hash = hashlib.md5(
                json.dumps(key_data, default=str).encode()
            ).hexdigest()
            cache_key = f"{key_prefix}:{func.__name__}:{key_hash}" if key_prefix else f"{func.__name__}:{key_hash}"
            
            # Проверяем кэш
            cached_result = ttl_cache.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # Вызываем функцию и кэшируем результат
            result = func(*args, **kwargs)
            ttl_cache.put(cache_key, result, ttl_seconds)
            
            return result
        
        return wrapper
    return decorator
