# 🐘 PostgreSQL для IT Interview Trainer

## Быстрый старт с PostgreSQL

### 1. Запуск с PostgreSQL (Docker Compose)

```bash
# Копируем .env.example в .env
cp .env.example .env

# Генерируем SECRET_KEY
openssl rand -hex 32

# Устанавливаем POSTGRES_PASSWORD в .env
echo "POSTGRES_PASSWORD=$(openssl rand -base64 32)" >> .env
echo "SECRET_KEY=$(openssl rand -hex 32)" >> .env

# Запускаем все сервисы с PostgreSQL
docker-compose -f docker-compose.postgres.yml up -d

# Проверка статуса
docker-compose -f docker-compose.postgres.yml ps
```

### 2. Доступные сервисы

| Сервис | URL | Описание |
|--------|-----|----------|
| **Frontend** | http://localhost:3000 | React приложение |
| **Backend** | http://localhost:8000 | FastAPI API |
| **PostgreSQL** | localhost:5433 | База данных (порт 5433) |
| **Swagger UI** | http://localhost:8000/docs | API документация |

### 3. Применение миграций

```bash
# Миграции применяются автоматически при старте backend
# Проверка в логах:
docker-compose -f docker-compose.postgres.yml logs backend | grep migration
```

### 4. Бэкап данных

```bash
# Бэкап PostgreSQL
docker-compose -f docker-compose.postgres.yml exec postgres \
  pg_dump -U interview_admin interview_trainer > backup_$(date +%Y%m%d).sql

# Восстановление из бэкапа
docker-compose -f docker-compose.postgres.yml exec -T postgres \
  psql -U interview_admin interview_trainer < backup_20260319.sql
```

---

## Миграция с SQLite на PostgreSQL

### Шаг 1: Экспорт данных из SQLite

```bash
cd backend
source venv/bin/activate

# Экспорт в JSON
python3 ../scripts/export_to_postgres.py
```

### Шаг 2: Запуск PostgreSQL

```bash
docker-compose -f docker-compose.postgres.yml up -d postgres
```

### Шаг 3: Применение миграций

```bash
# Применяем миграции Alembic
cd backend
alembic upgrade head
```

### Шаг 4: Импорт данных

```bash
python3 ../scripts/import_from_json.py backup_data.json
```

---

## Настройки для production

### Переменные окружения

```bash
# .env.production
DATABASE_URL=postgresql://interview_admin:secure_password@postgres:5432/interview_trainer
SECRET_KEY=<64-random-characters>
DEBUG=false
CORS_ORIGINS=https://yourdomain.com
```

### Docker Compose production

```bash
# Используйте docker-compose.postgres.yml как основу
# Измените пароли и настройки в .env файле
```

### Рекомендации по безопасности

1. **Смените пароли по умолчанию**
   ```bash
   POSTGRES_PASSWORD=$(openssl rand -base64 48)
   ```

2. **Настройте firewall**
   ```bash
   # Закройте порт 5433 для внешнего доступа
   ufw deny 5433
   ```

3. **Используйте secrets для Docker**
   ```yaml
   # docker-compose.prod.yml
   secrets:
     db_password:
       file: ./secrets/db_password.txt
   ```

4. **Включите SSL для PostgreSQL**
   ```bash
   # postgresql.conf
   ssl = on
   ssl_cert_file = /path/to/server.crt
   ssl_key_file = /path/to/server.key
   ```

---

## Мониторинг PostgreSQL

### Проверка статуса

```bash
# Подключение к БД
docker-compose -f docker-compose.postgres.yml exec postgres \
  psql -U interview_admin -d interview_trainer

# Проверка таблиц
\dt

# Проверка размера БД
SELECT pg_size_pretty(pg_database_size('interview_trainer'));

# Активные соединения
SELECT * FROM pg_stat_activity;
```

### Логи PostgreSQL

```bash
docker-compose -f docker-compose.postgres.yml logs postgres
```

### Prometheus метрики

Backend предоставляет метрики через endpoint `/metrics`:

```bash
curl http://localhost:8000/metrics
```

---

## Troubleshooting

### Ошибка: "database does not exist"

```bash
# Создайте базу данных вручную
docker-compose -f docker-compose.postgres.yml exec postgres \
  psql -U interview_admin -c "CREATE DATABASE interview_trainer;"
```

### Ошибка: "relation does not exist"

```bash
# Примените миграции
cd backend
alembic upgrade head
```

### Ошибка: "password authentication failed"

```bash
# Проверьте POSTGRES_PASSWORD в .env
# Пересоздайте контейнер
docker-compose -f docker-compose.postgres.yml down
docker-compose -f docker-compose.postgres.yml up -d
```

### Бэкап не восстанавливается

```bash
# Проверьте версию PostgreSQL
docker-compose -f docker-compose.postgres.yml exec postgres \
  psql -U interview_admin -c "SELECT version();"

# Убедитесь что бэкап совместим
head -20 backup.sql
```

---

## Производительность

### Индексы

Для ускорения работы с JSON полями применяются GIN индексы:

```sql
-- Проверка индексов
\di

-- Создание дополнительного индекса (если нужно)
CREATE INDEX CONCURRENTLY idx_questions_difficulty 
ON questions USING btree (difficulty);
```

### Кэширование запросов

PostgreSQL автоматически кэширует часто используемые данные в `shared_buffers`.

### Connection Pooling

Для production с >100 одновременных соединений используйте **PgBouncer**:

```yaml
# docker-compose.pgbouncer.yml
services:
  pgbouncer:
    image: bitnami/pgbouncer:latest
    environment:
      - POSTGRESQL_HOST=postgres
      - POSTGRESQL_PORT=5432
      - POSTGRESQL_USERNAME=interview_admin
      - POSTGRESQL_PASSWORD=${POSTGRES_PASSWORD}
      - PGBOUNCER_POOL_MODE=transaction
      - PGBOUNCER_MAX_CLIENT_CONN=200
      - PGBOUNCER_DEFAULT_POOL_SIZE=20
```

---

## Дополнительные ресурсы

- [Документация PostgreSQL](https://www.postgresql.org/docs/)
- [Alembic миграции](https://alembic.sqlalchemy.org/)
- [SQLAlchemy Core](https://docs.sqlalchemy.org/)
- [PgBouncer](https://www.pgbouncer.org/)

---

**✅ Готово!** Ваше приложение полностью готово к работе с PostgreSQL.
