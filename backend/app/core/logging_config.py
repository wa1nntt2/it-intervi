"""
Конфигурация логирования для IT Interview Trainer.

Поддерживает:
- Консольный вывод (development)
- JSON формат для production (совместимость с Prometheus/Grafana)
- Файловое логирование
- Разные уровни логирования для разных модулей
- Структурированные логи с контекстом
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

try:
    from pythonjsonlogger import jsonlogger
    JSON_LOGGER_AVAILABLE = True
except ImportError:
    JSON_LOGGER_AVAILABLE = False

from app.core.config import settings


class CustomJsonFormatter(jsonlogger.JsonFormatter if JSON_LOGGER_AVAILABLE else logging.Formatter):
    """
    Кастомный JSON форматтер для структурированных логов.
    Добавляет дополнительные поля в каждый лог.
    """
    
    def add_fields(self, log_record: dict, record: logging.LogRecord, message_dict: dict) -> None:
        """Добавляет дополнительные поля в лог запись"""
        super().add_fields(log_record, record, message_dict)
        
        # Добавляем timestamp в ISO формате
        log_record['timestamp'] = datetime.utcnow().isoformat()
        
        # Добавляем уровень лога
        log_record['level'] = record.levelname
        
        # Добавляем имя логгера
        log_record['logger'] = record.name
        
        # Добавляем имя модуля и функцию
        log_record['module'] = record.module
        log_record['function'] = record.funcName
        
        # Добавляем номер строки
        log_record['line'] = record.lineno
        
        # Добавляем process info
        log_record['process_id'] = record.process
        log_record['thread_id'] = record.thread
        
        # Добавляем app информацию
        log_record['app_name'] = settings.PROJECT_NAME
        log_record['app_version'] = settings.VERSION


class ColoredFormatter(logging.Formatter):
    """
    Цветной форматтер для консольного вывода в development режиме.
    """
    
    # ANSI escape codes для цветов
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
    }
    RESET = '\033[0m'
    
    def format(self, record: logging.LogRecord) -> str:
        """Форматирование с цветами"""
        log_color = self.COLORS.get(record.levelname, self.RESET)
        log_time = datetime.fromtimestamp(record.created).strftime('%H:%M:%S')
        
        # Формируем сообщение
        message = super().format(record)
        
        return f"{log_color}[{log_time}] {record.levelname:8}{self.RESET} {message}"


def setup_logging(
    log_level: str = "INFO",
    log_file: Optional[str] = None,
    json_format: bool = False,
    log_sql: bool = False,
) -> logging.Logger:
    """
    Настройка логирования для приложения.
    
    Args:
        log_level: Уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Путь к файлу для логирования (опционально)
        json_format: Использовать JSON формат (True для production)
        log_sql: Логировать SQL запросы (только для development)
    
    Returns:
        Настроенный logger
    
    Пример использования:
        logger = setup_logging(log_level="DEBUG", json_format=False)
        logger.info("Приложение запущено")
    """
    
    # Создаем root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))
    
    # Очищаем существующие handlers
    root_logger.handlers.clear()
    
    # === Консольный handler ===
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, log_level.upper()))
    
    if json_format and JSON_LOGGER_AVAILABLE:
        # JSON формат для production
        console_formatter = CustomJsonFormatter(
            '%(timestamp)s %(level)s %(logger)s %(module)s %(function)s %(message)s'
        )
    else:
        # Цветной формат для development
        console_formatter = ColoredFormatter(
            f'%(asctime)s %(levelname)-8s %(name)s: %(message)s',
            datefmt='%H:%M:%S'
        )
    
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)
    
    # === Файловый handler (опционально) ===
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_path, encoding='utf-8')
        file_handler.setLevel(getattr(logging, log_level.upper()))
        
        # Для файла всегда используем JSON формат
        if JSON_LOGGER_AVAILABLE:
            file_formatter = CustomJsonFormatter(
                '%(timestamp)s %(level)s %(logger)s %(module)s %(function)s %(message)s'
            )
        else:
            file_formatter = logging.Formatter(
                '%(asctime)s %(levelname)-8s %(name)s: %(message)s'
            )
        
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)
    
    # === Логирование SQLAlchemy (опционально) ===
    if log_sql:
        sql_logger = logging.getLogger('sqlalchemy.engine')
        sql_logger.setLevel(logging.INFO)  # INFO для SQL, DEBUG для параметров
        
        # Добавляем SQL logger в console
        sql_logger.addHandler(console_handler)
    
    # === Логирование uvicorn ===
    uvicorn_logger = logging.getLogger('uvicorn')
    uvicorn_logger.handlers.clear()
    uvicorn_logger.addHandler(console_handler)
    uvicorn_logger.setLevel(getattr(logging, log_level.upper()))
    
    # === Логирование alembic ===
    alembic_logger = logging.getLogger('alembic')
    alembic_logger.handlers.clear()
    alembic_logger.addHandler(console_handler)
    alembic_logger.setLevel(logging.WARNING)  # Только warnings и ошибки
    
    # Создаем и возвращаем logger для приложения
    app_logger = logging.getLogger('app')
    app_logger.setLevel(getattr(logging, log_level.upper()))
    
    return app_logger


def get_logger(name: str) -> logging.Logger:
    """
    Получить logger по имени.
    
    Args:
        name: Имя logger (обычно __name__ модуля)
    
    Returns:
        Logger instance
    
    Пример:
        logger = get_logger(__name__)
        logger.info("Сообщение")
    """
    return logging.getLogger(name)


# Глобальный logger для приложения
logger = get_logger('app')
