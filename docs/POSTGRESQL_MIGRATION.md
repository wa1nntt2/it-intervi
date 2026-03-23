# 🐘 Руководство по миграции на PostgreSQL

## Проблема

В текущей конфигурации используются JSON поля в SQLite, которые работают иначе чем в PostgreSQL:

| Особенность | SQLite | PostgreSQL |
|-------------|--------|------------|
| **JSON тип** | TEXT (хранится как строка) | JSONB (бинарный формат) |
| **Валидация** | Нет валидации JSON | Автоматическая валидация |
| **Индексы** | Нельзя создать индекс на JSON | GIN/GiST индексы для JSON |
| **Производительность** | Медленная работа с JSON | Оптимизировано |

## Решение

### 1. Обновленная модель данных для PostgreSQL

Модели уже совместимы с PostgreSQL благодаря SQLAlchemy. JSON поля автоматически маппятся:

```python
# Работает и для SQLite, и для PostgreSQL
from sqlalchemy import Column, JSON

class Question(Base):
    options = Column(JSON, nullable=False)  # SQLite: TEXT, PostgreSQL: JSONB
    correct_order = Column(JSON, nullable=True)
```

### 2. Конфигурация подключения

#### Для разработки (SQLite)
```bash
# .env
DATABASE_URL=sqlite:///./data/interview_trainer.db
```

#### Для production (PostgreSQL)
```bash
# .env.production
DATABASE_URL=postgresql://user:password@localhost:5432/interview_trainer
```

#### Для Docker Compose
```yaml
# docker-compose.yml
services:
  backend:
    environment:
      - DATABASE_URL=postgresql://postgres:postgres123@postgres:5432/interview_trainer
```

### 3. Миграция данных с SQLite на PostgreSQL

#### Шаг 1: Экспорт данных из SQLite

```bash
cd backend
source venv/bin/activate

# Экспорт всех таблиц в JSON
python3 ../scripts/export_to_postgres.py
```

#### Шаг 2: Настройка PostgreSQL

```bash
# Создаем базу данных
docker-compose up -d postgres
docker-compose exec postgres psql -U postgres -c "CREATE DATABASE interview_trainer;"
```

#### Шаг 3: Применение миграций

```bash
cd backend
export DATABASE_URL=postgresql://postgres:postgres123@localhost:5432/interview_trainer

# Применить миграции Alembic
python migrate.py upgrade
```

#### Шаг 4: Импорт данных

```bash
python3 ../scripts/import_from_sqlite.py backup_data.json
```

---

## Проверка совместимости

### ✅ Уже совместимы

| Компонент | Статус | Примечания |
|-----------|--------|------------|
| **Модели** | ✅ Совместимы | SQLAlchemy абстрагирует различия |
| **Миграции** | ✅ Совместимы | Alembic поддерживает обе БД |
| **JSON поля** | ✅ Совместимы | `JSON` тип работает везде |
| **Индексы** | ✅ Совместимы | Стандартные индексы работают |

### ⚠️ Требуют внимания

| Компонент | Проблема | Решение |
|-----------|----------|---------|
| **SQLite специфичные функции** | `CURRENT_TIMESTAMP` | Использовать `datetime.utcnow` |
| **JSON индексы** | SQLite не поддерживает | Добавить GIN индексы для PostgreSQL |
| **Коннекты** | `check_same_thread` | Только для SQLite |

---

## Обновленная конфигурация engine.py

```python
# backend/app/database/engine.py
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

DATABASE_URL = settings.DATABASE_URL

# Определяем тип БД
is_sqlite = DATABASE_URL.startswith("sqlite")
is_postgresql = DATABASE_URL.startswith("postgresql")

# Настройки подключения
connect_args = {}
if is_sqlite:
    connect_args["check_same_thread"] = False
elif is_postgresql:
    connect_args["server_side_cursors"] = True  # Для больших выборок

# Создание движка
engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,  # Проверка соединения перед использованием
    pool_size=20 if is_postgresql else None,  # Только для PostgreSQL
    max_overflow=40 if is_postgresql else None,
)

# SQLite PRAGMA настройки
if is_sqlite:
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
```

---

## Оптимизации для PostgreSQL

### 1. GIN индексы для JSON полей

Создайте миграцию для ускорения поиска по JSON:

```python
# alembic/versions/xxx_add_json_indexes.py
from alembic import op
from sqlalchemy import text

def upgrade():
    # GIN индекс для options (быстрый поиск по значениям)
    op.execute(text(
        "CREATE INDEX IF NOT EXISTS ix_questions_options_gin "
        "ON questions USING GIN (options)"
    ))
    
    # GIN индекс для correct_order
    op.execute(text(
        "CREATE INDEX IF NOT EXISTS ix_questions_correct_order_gin "
        "ON questions USING GIN (correct_order)"
    ))
    
    # GIN индекс для question_ids в сессиях
    op.execute(text(
        "CREATE INDEX IF NOT EXISTS ix_sessions_question_ids_gin "
        "ON sessions USING GIN (question_ids)"
    ))

def downgrade():
    op.execute(text("DROP INDEX IF EXISTS ix_questions_options_gin"))
    op.execute(text("DROP INDEX IF EXISTS ix_questions_correct_order_gin"))
    op.execute(text("DROP INDEX IF EXISTS ix_sessions_question_ids_gin"))
```

### 2. Full-text search для вопросов

```python
# alembic/versions/xxx_add_fulltext_search.py
from alembic import op
from sqlalchemy import text

def upgrade():
    # Создаем tsvector колонку
    op.execute(text(
        "ALTER TABLE questions ADD COLUMN search_vector tsvector"
    ))
    
    # Заполняем существующие записи
    op.execute(text(
        """
        UPDATE questions 
        SET search_vector = to_tsvector('russian', COALESCE(text, ''))
        """
    ))
    
    # Создаем GIN индекс
    op.execute(text(
        "CREATE INDEX ix_questions_search_vector ON questions USING GIN (search_vector)"
    ))
    
    # Триггер для авто-обновления
    op.execute(text(
        """
        CREATE TRIGGER questions_search_vector_update
        BEFORE INSERT OR UPDATE ON questions
        FOR EACH ROW EXECUTE FUNCTION
        tsvector_update_trigger(search_vector, 'pg_catalog.russian', text)
        """
    ))

def downgrade():
    op.execute(text("DROP TRIGGER IF EXISTS questions_search_vector_update ON questions"))
    op.execute(text("ALTER TABLE questions DROP COLUMN search_vector"))
```

### 3. Использование search_vector в API

```python
# backend/app/api/questions.py
@router.get("/search")
def search_questions(q: str, db: Session = Depends(get_db)):
    """Полнотекстовый поиск вопросов"""
    from sqlalchemy import text
    
    query = db.query(Question).filter(
        text("search_vector @@ plainto_tsquery('russian', :query)"),
        {"query": q}
    )
    
    return query.all()
```

---

## Docker Compose для production

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    container_name: it-interview-postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./scripts/init.sql:/docker-entrypoint-initdb.d/init.sql
    environment:
      - POSTGRES_DB=interview_trainer
      - POSTGRES_USER=${POSTGRES_USER:-interview_admin}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD:?Required}
      - PGDATA=/var/lib/postgresql/data/pgdata
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-interview_admin}"]
      interval: 5s
      timeout: 5s
      retries: 5
    restart: unless-stopped
    networks:
      - it-interview-network

  backend:
    build: ./backend
    environment:
      - DATABASE_URL=postgresql://${POSTGRES_USER:-interview_admin}:${POSTGRES_PASSWORD}@postgres:5432/interview_trainer
      - SECRET_KEY=${SECRET_KEY:?Required}
    depends_on:
      postgres:
        condition: service_healthy
    networks:
      - it-interview-network

volumes:
  postgres_data:
    driver: local

networks:
  it-interview-network:
    driver: bridge
```

---

## Проверка после миграции

```bash
# Проверка подключения
psql postgresql://user:pass@localhost/interview_trainer -c "\dt"

# Проверка данных
psql postgresql://user:pass@localhost/interview_trainer -c "SELECT COUNT(*) FROM questions;"

# Проверка индексов
psql postgresql://user:pass@localhost/interview_trainer -c "\di"

# Проверка JSON полей
psql postgresql://user:pass@localhost/interview_trainer -c "SELECT id, jsonb_typeof(options) FROM questions LIMIT 5;"
```

---

## Troubleshooting

### Ошибка: "relation does not exist"

```bash
# Примените миграции
cd backend
alembic upgrade head
```

### Ошибка: "permission denied"

```sql
-- Предоставьте права
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO interview_admin;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO interview_admin;
```

### Ошибка: "invalid byte sequence for encoding"

```python
# В engine.py добавьте
engine = create_engine(
    DATABASE_URL,
    connect_args={"options": "-c client_encoding=UTF8"}
)
```

---

## Рекомендации для production

1. **Регулярные бэкапы**
   ```bash
   pg_dump -U interview_admin interview_trainer > backup_$(date +%Y%m%d).sql
   ```

2. **Мониторинг**
   ```sql
   SELECT * FROM pg_stat_activity;  -- Активные соединения
   SELECT * FROM pg_stat_user_tables;  -- Статистика таблиц
   ```

3. **VACUUM**
   ```sql
   VACUUM ANALYZE questions;  -- Оптимизация и обновление статистики
   ```

4. **Connection pooling**
   - Используйте PgBouncer для production с >100 коннектов

---

**✅ Готово!** Приложение полностью совместимо с PostgreSQL.
