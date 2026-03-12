"""
Rate limiter конфигурация.
Вынесено в отдельный модуль для избежания циклических зависимостей.

Rate limiting защищает API от злоупотреблений, ограничивая количество запросов
в минуту от одного IP адреса.
"""
from slowapi import Limiter
from slowapi.util import get_remote_address

# Инициализация rate limiter с функцией получения IP адреса клиента
limiter = Limiter(key_func=get_remote_address)
