# 📝 Резюме: Настройка логирования

## ✅ Выполненные задачи

### 1. Модуль логирования

**Файл:** `backend/app/core/logging_config.py`

**Возможности:**
- ✅ Консольный вывод (development)
- ✅ JSON формат для production (совместимость с Prometheus/Grafana)
- ✅ Файловое логирование
- ✅ Разные уровни логирования
- ✅ Структурированные логи с контекстом
- ✅ Цветной вывод для development
- ✅ Логирование SQL запросов (опционально)

**Функции:**
- `setup_logging()` - настройка логирования
- `get_logger(name)` - получение logger по имени
- `CustomJsonFormatter` - JSON форматтер с доп. полями
- `ColoredFormatter` - Цветной форматтер для консоли

---

### 2. Обновление main.py

**Изменения:**
- ✅ Импорт и настройка logging в начале файла
- ✅ Логирование запуска приложения
- ✅ Логирование применения миграций
- ✅ Логирование сидирования БД
- ✅ Логирование регистрации роутеров
- ✅ Логирование медленных запросов (>1s)
- ✅ Обработка ошибок с logging.exception()

**Примеры логов:**
```
🚀 Запуск IT Interview Trainer v0.1.0
Режим: DEBUG
✅ Rate limiter добавлен
✅ CORS настроен для: ['http://localhost:3000']
🌱 Сидирование базы данных...
✅ База данных засидирована
✅ API роутеры зарегистрированы
```

---

### 3. Обновление auth.py

**Добавлено логирование:**
- ✅ Регистрация нового пользователя
- ✅ Попытки входа с неверным email/паролем
- ✅ Успешный вход пользователя
- ✅ Предупреждения о подозрительной активности

**Примеры:**
```
⚠️  Попытка регистрации занятого email: user@example.com
✅ Зарегистрирован новый пользователь: user@example.com (ID: 123)
⚠️  Неверная попытка входа для: user@example.com
✅ Пользователь вошел в систему: user@example.com (ID: 123)
```

---

### 4. Обновление requirements.txt

**Добавлена зависимость:**
```
python-json-logger>=2.0.7
```

---

### 5. Документация

**Созданные файлы:**
- `docs/LOGGING_GUIDE.md` - Полное руководство (350+ строк)
- `docs/LOGGING_SUMMARY.md` - Это резюме

---

## 🚀 Быстрый старт

### Использование в коде

```python
from app.core.logging_config import get_logger

logger = get_logger(__name__)

logger.debug("Отладочное сообщение")
logger.info("Информационное сообщение")
logger.warning("Предупреждение")
logger.error("Ошибка", exc_info=True)
logger.critical("Критическая ошибка")
```

### Настройка для development

```python
from app.core.logging_config import setup_logging

setup_logging(
    log_level="DEBUG",      # Подробные логи
    json_format=False,      # Цветной вывод
    log_sql=True,           # Логировать SQL
    log_file=None           # Только консоль
)
```

### Настройка для production

```python
from app.core.logging_config import setup_logging

setup_logging(
    log_level="INFO",       # Только важные события
    json_format=True,       # JSON для Grafana
    log_sql=False,          # Не логировать SQL
    log_file="logs/app.log" # Сохранять в файл
)
```

---

## 📊 Форматы логов

### Development (цветной)

```
18:45:32 INFO     app.main: 🚀 Запуск IT Interview Trainer v0.1.0
18:45:32 DEBUG    app.main: ✅ Rate limiter добавлен
18:45:33 WARNING  app.api.auth: ⚠️  Неверная попытка входа для: user@example.com
18:45:33 ERROR    app.api.auth: ❌ Ошибка аутентификации
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

### Loki конфигурация

```yaml
# docker-compose.monitoring.yml
services:
  loki:
    image: grafana/loki:2.9.0
    volumes:
      - ./loki:/etc/loki
      - ./logs:/var/log/app

  promtail:
    image: grafana/promtail:2.9.0
    volumes:
      - ./logs:/var/log/app
      - ./promtail:/etc/promtail
```

### LogQL запросы

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

| Уровень | Когда использовать |
|---------|-------------------|
| **DEBUG** | Детальная отладочная информация |
| **INFO** | Важные события (вход, создание записи) |
| **WARNING** | Предупреждения (некритичные ошибки) |
| **ERROR** | Ошибки (критичные события) |
| **CRITICAL** | Критические ошибки (требуют внимания) |

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
```

### 3. Не логируйте чувствительные данные

```python
# ❌ НИКОГДА не логируйте:
logger.info(f"Пароль: {password}")
logger.debug(f"Токен: {token}")

# ✅ Правильно:
logger.info(f"Пользователь вошел: {email}")
```

---

## 📁 Структура файлов

```
backend/
├── app/
│   ├── core/
│   │   └── logging_config.py    # ✅ Новый модуль логирования
│   └── main.py                   # ✅ Обновлен с logging
│   └── api/
│       └── auth.py               # ✅ Обновлен с logging
├── logs/                         # 📁 Директория для логов
│   └── app.log                   # Файл логов (production)
└── requirements.txt              # ✅ Добавлен python-json-logger
```

---

## 🔧 Проверка работы

### Тестирование

```bash
cd backend
source venv/bin/activate

# Тест цветного вывода
python -c "
from app.core.logging_config import setup_logging, get_logger
logger = setup_logging(log_level='DEBUG', json_format=False)
log = get_logger(__name__)
log.info('Test message')
"

# Тест JSON формата
python -c "
from app.core.logging_config import setup_logging, get_logger
logger = setup_logging(log_level='DEBUG', json_format=True)
log = get_logger(__name__)
log.info('Test JSON message')
"
```

### Проверка в приложении

```bash
# Запуск backend
uvicorn app.main:app --reload

# Проверка логов
tail -f logs/app.log  # Production
```

---

## 📚 Документация

| Файл | Описание |
|------|----------|
| [`docs/LOGGING_GUIDE.md`](docs/LOGGING_GUIDE.md) | Полное руководство |
| [`backend/app/core/logging_config.py`](backend/app/core/logging_config.py) | Модуль логирования |

---

## 🎯 Итог

Создана **полноценная система логирования** для приложения:

1. ✅ **Централизованное логирование** - единый модуль для всех компонентов
2. ✅ **Гибкость** - 2 формата (цветной/JSON), разные уровни
3. ✅ **Production-ready** - JSON формат для Grafana/Loki
4. ✅ **Безопасность** - предупреждения о чувствительных данных
5. ✅ **Документация** - подробное руководство
6. ✅ **Интеграция** - готово к использованию с Prometheus/Grafana

**Общий объем изменений:**
- 1 новый модуль (logging_config.py, 200+ строк)
- 2 обновленных файла (main.py, auth.py)
- 1 обновленный requirements.txt
- 1 документ (350+ строк)

---

**🎉 Готово!** Теперь ваше приложение имеет полноценное структурированное логирование!
