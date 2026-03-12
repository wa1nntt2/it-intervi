from collections import OrderedDict
from typing import Any, Optional
import threading

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


# Глобальный экземпляр кэша
cache = LRUCache()
