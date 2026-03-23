# 📝 Руководство по логированию

## 📋 Оглавление

1. [Быстрый старт](#быстрый-старт)
2. [Настройка логирования](#настройка-логирования)
3. [Использование в коде](#использование-в-коде)
4. [Форматы логов](#форматы-логов)
5. [Интеграция с Prometheus/Grafana](#интеграция-с-prometheusgrafana)
6. [Best Practices](#best-practices)

---

## 🚀 Быстрый старт

### Использование в коде

```python
from app.core.logging_config import get_logger

logger = get_logger(__name__)

logger.debug("Отладочное сообщение")
logger.info("Информационное сообщение")
logger.warning("Предупреждение")
logger.error("Ошибка")
logger.critical("Критическая ошибка")
```

### Настройка при запуске

```python
from app.core.logging_config import setup_logging

# Development режим (цветной вывод)
setup_logging(
    log_level="DEBUG",
    json_format=False,
    log_sql=True
)

# Production режим (JSON формат)
setup_logging(
    log_level="INFO",
    log_file="logs/app.log",
    json_format=True,
    log_sql=False
)
```

---

## ⚙️ Настройка логирования

### Параметры setup_logging

| Параметр | Тип | По умолчанию | Описание |
|----------|-----|--------------|----------|
| `log_level` | str | "INFO" | Уровень логирования |
| `log_file` | str | None | Путь к файлу логов |
| `json_format` | bool | False | Использовать JSON формат |
| `log_sql` | bool | False | Логировать SQL запросы |

### Уровни логирования

| Уровень | Когда использовать |
|---------|-------------------|
| **DEBUG** | Детальная отладочная информация |
| **INFO** | Важные события (вход пользователя, создание записи) |
| **WARNING** | Предупреждения (некритичные ошибки) |
| **ERROR** | Ошибки (критичные события) |
| **CRITICAL** | Критические ошибки (требуют немедленного внимания) |

### Примеры настройки

#### Development

```python
setup_logging(
    log_level="DEBUG",      # Подробные логи
    json_format=False,      # Цветной вывод
    log_sql=True,           # Логировать SQL
    log_file=None           # Только консоль
)
```

#### Production

```python
setup_logging(
    log_level="INFO",       # Только важные события
    json_format=True,       # JSON для Grafana
    log_sql=False,          # Не логировать SQL
    log_file="logs/app.log" # Сохранять в файл
)
```

#### Staging

```python
setup_logging(
    log_level="DEBUG",      # Подробные логи для отладки
    json_format=True,       # JSON формат
    log_sql=True,           # Логировать SQL
    log_file="logs/app.log"
)
```

---

## 💻 Использование в коде

### Базовое использование

```python
from app.core.logging_config import get_logger

logger = get_logger(__name__)

# Простые сообщения
logger.info("Пользователь зарегистрирован")
logger.error("Ошибка базы данных")

# С контекстом
logger.info(
    "Сессия создана",
    extra={
        "user_id": user.id,
        "session_id": session.id,
        "profession": profession_name
    }
)

# С исключением
try:
    result = db.query(User).filter(User.id == user_id).one()
except Exception as e:
    logger.error(f"Ошибка при получении пользователя: {e}", exc_info=True)
```

### Логирование в API endpoints

```python
from app.core.logging_config import get_logger

logger = get_logger(__name__)

@router.post("/login")
def login(...):
    user = db.query(User).filter(User.email == email).first()
    
    if not user:
        logger.warning(f"⚠️  Попытка входа с несуществующим email: {email}")
        raise HTTPException(404, "Пользователь не найден")
    
    if not verify_password(password, user.hashed_password):
        logger.warning(f"⚠️  Неверный пароль для: {email}")
        raise HTTPException(401, "Неверный пароль")
    
    logger.info(f"✅ Пользователь вошел: {user.email} (ID: {user.id})")
    return create_tokens(user)
```

### Логирование с контекстом

```python
# Логирование с дополнительными полями
logger.info(
    "Запрос выполнен",
    extra={
        "method": request.method,
        "path": request.url.path,
        "duration_ms": duration * 1000,
        "status_code": response.status_code,
        "user_agent": request.headers.get("user-agent"),
    }
)
```

### Логирование исключений

```python
# С выводом traceback
try:
    risky_operation()
except Exception as e:
    logger.error(f"Ошибка операции: {e}", exc_info=True)

# С указанием уровня
logger.exception("Критическая ошибка в обработчике")  # То же что error + exc_info=True
```

---

## 📊 Форматы логов

### Development (цветной)

```
18:45:32 INFO     app.main: 🚀 Запуск IT Interview Trainer v0.1.0
18:45:32 DEBUG    app.main: ✅ Rate limiter добавлен
18:45:32 DEBUG    app.main: ✅ CORS настроен для: ['http://localhost:3000']
18:45:33 INFO     app.main: 🌱 Сидирование базы данных...
18:45:33 INFO     app.main: ✅ База данных засидирована
18:45:33 INFO     app.main: ✅ API роутеры зарегистрированы
```

### Production (JSON)

```json
{
  "timestamp": "2026-03-19T18:45:32.123456",
  "level": "INFO",
  "logger": "app.main",
  "module": "main",
  "function": "create_app",
  "message": "Запуск IT Interview Trainer v0.1.0",
  "app_name": "IT Interview Trainer",
  "app_version": "0.1.0",
  "process_id": 12345,
  "thread_id": 140234567890
}
```

---

## 📈 Интеграция с Prometheus/Grafana

### Структура JSON логов

Каждый лог в JSON формате содержит:

```json
{
  "timestamp": "2026-03-19T18:45:32.123456",  # ISO 8601
  "level": "INFO",                             # Уровень
  "logger": "app.main",                        # Имя logger
  "module": "main",                            # Модуль
  "function": "create_app",                    # Функция
  "message": "Сообщение",                      # Текст
  "app_name": "IT Interview Trainer",          # Приложение
  "app_version": "0.1.0",                      # Версия
  "process_id": 12345,                         # PID
  "thread_id": 140234567890                    # TID
}
```

### Настройка Loki для сбора логов

```yaml
# docker-compose.monitoring.yml
services:
  loki:
    image: grafana/loki:2.9.0
    volumes:
      - ./loki:/etc/loki
      - ./logs:/var/log/app
    command: -config.file=/etc/loki/loki.yml

  promtail:
    image: grafana/promtail:2.9.0
    volumes:
      - ./logs:/var/log/app
      - ./promtail:/etc/promtail
    command: -config.file=/etc/promtail/config.yml
```

### Promtail конфигурация

```yaml
# promtail/config.yml
server:
  http_listen_port: 9080
  grpc_listen_port: 0

positions:
  filename: /tmp/positions.yaml

clients:
  - url: http://loki:3100/loki/api/v1/push

scrape_configs:
  - job_name: app_logs
    static_configs:
      - targets:
          - localhost
        labels:
          job: it-interview-trainer
          __path__: /var/log/app/*.log
```

### Grafana Loki запросы

```logql
# Все ошибки за последний час
{job="it-interview-trainer"} |= "ERROR"

# Логи конкретного пользователя
{job="it-interview-trainer"} | json | user_id="12345"

# Медленные запросы (>1s)
{job="it-interview-trainer"} |= "Медленный запрос"

# Количество ошибок по уровням
sum by (level) (count_over_time({job="it-interview-trainer"} |= "ERROR" [1h]))
```

---

## ✅ Best Practices

### 1. Используйте правильные уровни

```python
# ✅ Правильно
logger.debug("Получены данные из кэша")
logger.info("Пользователь создан")
logger.warning("Попытка входа с неверным паролем")
logger.error("Ошибка подключения к БД", exc_info=True)
logger.critical("Сервер не отвечает")

# ❌ Неправильно
logger.info("Получены данные из кэша")  # Слишком подробно для INFO
logger.error("Пользователь не найден")  # Это не ошибка, а ожидаемое поведение
```

### 2. Добавляйте контекст

```python
# ✅ Правильно
logger.info(
    "Сессия завершена",
    extra={
        "session_id": session.id,
        "user_id": user.id,
        "score": score,
        "total": total
    }
)

# ❌ Неправильно
logger.info("Сессия завершена")  # Нет контекста
```

### 3. Логируйте важные события

```python
# Что логировать:
# - Аутентификация (вход, выход, регистрация)
# - CRUD операции (создание, обновление, удаление)
# - Ошибки валидации
# - Медленные запросы
# - Изменения важных настроек

# Что НЕ логировать:
# - Чтение данных (если не отладка)
# - Успешные валидации (если не отладка)
# - Внутренние детали реализации
```

### 4. Не логируйте чувствительные данные

```python
# ❌ НИКОГДА не логируйте:
logger.info(f"Пароль пользователя: {password}")
logger.debug(f"Токен: {token}")
logger.info(f"Email: {email}, Пароль: {password}")

# ✅ Правильно:
logger.info(f"Пользователь вошел: {email}")  # Только email
```

### 5. Используйте structured logging

```python
# ✅ Правильно (JSON формат в production)
logger.info("Запрос выполнен", extra={
    "method": "POST",
    "path": "/api/login",
    "duration_ms": 45.2,
    "status": 200
})

# ❌ Неправильно
logger.info("POST /api/login 200 45.2ms")  # Парсинг сложен
```

---

## 🔧 Troubleshooting

### Логи не записываются в файл

```python
# Проверьте путь
setup_logging(log_file="/absolute/path/logs/app.log")

# Проверьте права
chmod 755 logs/
chmod 644 logs/app.log
```

### JSON логи не читаются

```python
# Установите python-json-logger
pip install python-json-logger

# Проверьте доступность
python -c "from pythonjsonlogger import jsonlogger; print('OK')"
```

### Дублирование логов

```python
# Очищайте handlers перед настройкой
logger.handlers.clear()

# Или используйте setup_logging которая делает это автоматически
```

---

## 📚 Дополнительные ресурсы

- [Python logging documentation](https://docs.python.org/3/library/logging.html)
- [python-json-logger](https://github.com/madzak/python-json-logger)
- [Grafana Loki](https://grafana.com/oss/loki/)
- [LogQL documentation](https://grafana.com/docs/loki/latest/logql/)

---

**✅ Готово!** Теперь ваше приложение имеет полноценное логирование!
