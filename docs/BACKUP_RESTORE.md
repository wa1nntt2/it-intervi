# 💾 Руководство по бэкапам и восстановлению

## 📋 Оглавление

1. [Стратегия бэкапирования](#стратегия-бэкапирования)
2. [Настройка](#настройка)
3. [Создание бэкапа](#создание-бэкапа)
4. [Восстановление](#восстановление)
5. [Проверка](#проверка)
6. [Troubleshooting](#troubleshooting)

---

## 📊 Стратегия бэкапирования

### Правило 3-2-1

```
✅ 3 копии данных (оригинал + 2 бэкапа)
✅ 2 разных типа носителей (локально + облако)
✅ 1 копия вне площадки (offsite)
```

### Расписание

| Тип | Частота | Время | Хранение |
|-----|---------|-------|----------|
| **Ежедневный** | Каждый день | 02:00 UTC | 30 дней |
| **Недельный** | Пятница | 03:00 UTC | 8 недель |
| **Месячный** | 1-е число | 04:00 UTC | 12 месяцев |

### Что бэкапим

| Компонент | Метод | Размер | Критичность |
|-----------|-------|--------|-------------|
| **PostgreSQL** | pg_dump | ~100MB | 🔴 Critical |
| **Конфигурация** | Копия файлов | ~10MB | 🟡 High |
| **Логи** | Архив | ~500MB | 🟢 Medium |
| **Медиа** | Копия файлов | ~1GB | 🟢 Medium |

---

## ⚙️ Настройка

### 1. Скрипт бэкапа

```bash
#!/bin/bash
# scripts/backup_postgres.sh

set -e

# Переменные
PROJECT_DIR="/app/it-interview-trainer"
BACKUP_DIR="$PROJECT_DIR/backups/postgresql"
DATE=$(date +%Y%m%d_%H%M%S)
PG_HOST="postgres"
PG_PORT="5432"
PG_USER="interview_admin"
PG_DB="interview_trainer"
PG_PASSWORD="${POSTGRES_PASSWORD}"

# Создать директорию
mkdir -p "$BACKUP_DIR/daily"
mkdir -p "$BACKUP_DIR/weekly"
mkdir -p "$BACKUP_DIR/monthly"

# Бэкап
export PGPASSWORD="$PG_PASSWORD"
pg_dump -h "$PG_HOST" -p "$PG_PORT" -U "$PG_USER" -d "$PG_DB" | \
  gzip > "$BACKUP_DIR/daily/interview_trainer_$DATE.sql.gz"

# Symlink на последний
ln -sf "daily/interview_trainer_$DATE.sql.gz" "$BACKUP_DIR/latest.sql.gz"

# Очистка старых (30 дней)
find "$BACKUP_DIR/daily" -name "*.sql.gz" -mtime +30 -delete

echo "✅ Бэкап создан: $BACKUP_DIR/daily/interview_trainer_$DATE.sql.gz"
```

### 2. Cron задача

```bash
# Отредактировать crontab
crontab -e

# Ежедневный бэкап в 02:00
0 2 * * * /app/it-interview-trainer/scripts/backup_postgres.sh >> /var/log/backup.log 2>&1

# Недельный бэкап в пятницу в 03:00
0 3 * * 5 /app/it-interview-trainer/scripts/backup_postgres.sh --weekly >> /var/log/backup.log 2>&1

# Месячный бэкап 1-го числа в 04:00
0 4 1 * * /app/it-interview-trainer/scripts/backup_postgres.sh --monthly >> /var/log/backup.log 2>&1
```

### 3. Docker Compose для бэкапов

```yaml
# docker-compose.backup.yml
version: '3.8'

services:
  backup:
    image: postgres:15-alpine
    volumes:
      - ./backups:/backups
      - ./scripts:/scripts
    environment:
      - PGPASSWORD=${POSTGRES_PASSWORD}
    command: >
      sh -c "
      pg_dump -h postgres -U interview_admin interview_trainer | \
      gzip > /backups/interview_trainer_\$(date +%Y%m%d_%H%M%S).sql.gz &&
      find /backups -name '*.sql.gz' -mtime +30 -delete
      "
    depends_on:
      - postgres
```

---

## 📦 Создание бэкапа

### Автоматический бэкап

```bash
# Запустить через cron (автоматически)
# Ежедневно в 02:00
```

### Ручной бэкап

```bash
# 1. Перейти в директорию проекта
cd /app/it-interview-trainer

# 2. Запустить скрипт бэкапа
./scripts/backup_postgres.sh

# 3. Или через Docker
docker-compose -f docker-compose.backup.yml up
```

### Бэкап через pg_dump напрямую

```bash
# Подключиться к БД
docker-compose -f docker-compose.prod.yml exec postgres \
  pg_dump -U interview_admin interview_trainer | \
  gzip > backups/interview_trainer_manual.sql.gz

# Проверить размер
ls -lh backups/interview_trainer_manual.sql.gz
```

### Полный бэкап (включая конфигурацию)

```bash
#!/bin/bash
# scripts/full_backup.sh

set -e

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/app/backups/full_$DATE"

mkdir -p "$BACKUP_DIR"

# Бэкап БД
docker-compose -f docker-compose.prod.yml exec postgres \
  pg_dump -U interview_admin interview_trainer | \
  gzip > "$BACKUP_DIR/database.sql.gz"

# Бэкап конфигурации
cp -r /app/it-interview-trainer/.env.production "$BACKUP_DIR/"
cp -r /app/it-interview-trainer/docker-compose.prod.yml "$BACKUP_DIR/"
cp -r /app/it-interview-trainer/nginx/ "$BACKUP_DIR/"

# Бэкап логов (опционально)
tar -czf "$BACKUP_DIR/logs.tar.gz" /app/it-interview-trainer/backend/logs/

# Архивировать всё
cd /app/backups
tar -czf "full_backup_$DATE.tar.gz" "full_$DATE"
rm -rf "full_$DATE"

echo "✅ Полный бэкап создан: /app/backups/full_backup_$DATE.tar.gz"
```

---

## 🔄 Восстановление

### Восстановление из последнего бэкапа

```bash
# 1. Найти последний бэкап
ls -lh /app/backups/postgresql/latest.sql.gz

# 2. Проверить целостность
gzip -t /app/backups/postgresql/latest.sql.gz

# 3. Восстановить БД
docker-compose -f docker-compose.prod.yml exec -T postgres \
  psql -U interview_admin -d interview_trainer < \
  /app/backups/postgresql/latest.sql.gz

# 4. Проверить
docker-compose -f docker-compose.prod.yml exec postgres \
  psql -U interview_admin -d interview_trainer -c \
  "SELECT COUNT(*) FROM users;"
```

### Восстановление из конкретного файла

```bash
# 1. Найти нужный бэкап
ls -lh /app/backups/postgresql/daily/

# 2. Проверить целостность
gzip -t /app/backups/postgresql/daily/interview_trainer_20260319_020000.sql.gz

# 3. Восстановить
docker-compose -f docker-compose.prod.yml exec -T postgres \
  psql -U interview_admin -d interview_trainer < \
  /app/backups/postgresql/daily/interview_trainer_20260319_020000.sql.gz
```

### Восстановление с полной остановкой сервиса

```bash
# 1. Остановить приложение
docker-compose -f docker-compose.prod.yml down

# 2. Восстановить БД
docker-compose -f docker-compose.prod.yml up -d postgres
sleep 10

docker-compose -f docker-compose.prod.yml exec -T postgres \
  psql -U interview_admin -d interview_trainer < \
  /app/backups/postgresql/latest.sql.gz

# 3. Запустить приложение
docker-compose -f docker-compose.prod.yml up -d

# 4. Проверить
curl https://yourdomain.com/health
```

### Восстановление из полного бэкапа

```bash
# 1. Распаковать архив
cd /app/backups
tar -xzf full_backup_20260319.tar.gz

# 2. Восстановить БД
gunzip -c full_20260319/database.sql.gz | \
  docker-compose -f docker-compose.prod.yml exec -T postgres \
  psql -U interview_admin -d interview_trainer

# 3. Восстановить конфигурацию
cp full_20260319/.env.production /app/it-interview-trainer/
cp full_20260319/docker-compose.prod.yml /app/it-interview-trainer/

# 4. Перезапустить сервисы
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d
```

---

## ✅ Проверка

### Ежедневная проверка

```bash
# 1. Проверить последний бэкап
ls -lh /app/backups/postgresql/latest.sql.gz

# 2. Проверить размер (должен быть > 1MB)
du -h /app/backups/postgresql/latest.sql.gz

# 3. Проверить целостность
gzip -t /app/backups/postgresql/latest.sql.gz

# 4. Проверить дату создания
stat /app/backups/postgresql/latest.sql.gz | grep Modify
```

### Еженедельная проверка

```bash
# 1. Проверить все бэкапы за неделю
ls -lh /app/backups/postgresql/daily/

# 2. Проверить логи бэкапа
cat /var/log/backup.log | tail -50

# 3. Проверить место на диске
df -h /app/backups
```

### Ежемесячная проверка (тестовое восстановление)

```bash
# 1. Создать тестовую БД
docker-compose -f docker-compose.prod.yml exec postgres \
  createdb -U interview_admin test_restore

# 2. Восстановить в тестовую БД
gunzip -c /app/backups/postgresql/latest.sql.gz | \
  docker-compose -f docker-compose.prod.yml exec -T postgres \
  psql -U interview_admin -d test_restore

# 3. Проверить данные
docker-compose -f docker-compose.prod.yml exec postgres \
  psql -U interview_admin -d test_restore -c \
  "SELECT COUNT(*) FROM users;"

# 4. Удалить тестовую БД
docker-compose -f docker-compose.prod.yml exec postgres \
  dropdb -U interview_admin test_restore

echo "✅ Тестовое восстановление успешно"
```

---

## 🔧 Troubleshooting

### Бэкап не создается

```bash
# 1. Проверить права на скрипт
ls -l /app/it-interview-trainer/scripts/backup_postgres.sh
chmod +x /app/it-interview-trainer/scripts/backup_postgres.sh

# 2. Проверить логи
cat /var/log/backup.log | tail -50

# 3. Проверить подключение к БД
docker-compose -f docker-compose.prod.yml exec postgres \
  pg_isready -U interview_admin

# 4. Запустить вручную
./scripts/backup_postgres.sh
```

### Бэкап слишком маленький

```bash
# 1. Проверить размер
du -h /app/backups/postgresql/latest.sql.gz

# 2. Проверить количество записей в БД
docker-compose -f docker-compose.prod.yml exec postgres \
  psql -U interview_admin -d interview_trainer -c \
  "SELECT 
    (SELECT count(*) FROM users) as users,
    (SELECT count(*) FROM questions) as questions,
    (SELECT count(*) FROM sessions) as sessions;"

# 3. Если мало данных - проверить скрипт
cat /app/it-interview-trainer/scripts/backup_postgres.sh
```

### Бэкап поврежден

```bash
# 1. Проверить целостность
gzip -t /app/backups/postgresql/latest.sql.gz

# 2. Если ошибка - попробовать восстановить
gzip -d /app/backups/postgresql/latest.sql.gz

# 3. Если не помогло - использовать предыдущий бэкап
ls -lt /app/backups/postgresql/daily/ | head -5
```

### Нет места для бэкапов

```bash
# 1. Проверить место
df -h

# 2. Очистить старые бэкапы
find /app/backups -name "*.sql.gz" -mtime +30 -delete

# 3. Настроить ротацию в скрипте
# find "$BACKUP_DIR/daily" -name "*.sql.gz" -mtime +30 -delete
```

### Cron не работает

```bash
# 1. Проверить статус cron
systemctl status cron

# 2. Проверить crontab
crontab -l

# 3. Проверить логи cron
grep CRON /var/log/syslog | tail -20

# 4. Перезапустить cron
systemctl restart cron
```

---

## 📊 Мониторинг бэкапов

### Алерт: Бэкап не создан

```yaml
# prometheus/alerts.yml
groups:
  - name: backup
    rules:
      - alert: BackupNotCreated
        expr: time() - backup_last_success_timestamp > 86400
        for: 1h
        labels:
          severity: warning
        annotations:
          summary: "Бэкап не создан за последние 24 часа"
```

### Алерт: Бэкап слишком маленький

```yaml
      - alert: BackupTooSmall
        expr: backup_size_bytes < 1048576
        for: 1h
        labels:
          severity: warning
        annotations:
          summary: "Бэкап подозрительно маленький (< 1MB)"
```

### Dashboard в Grafana

```logql
// Последний бэкап
{filename="/var/log/backup.log"} | line_format "{{.line}}"

// Успешные бэкапы
{filename="/var/log/backup.log"} |= "✅ Бэкап создан"

// Ошибки бэкапа
{filename="/var/log/backup.log"} |= "❌"
```

---

## 📋 Чек-листы

### Daily

- [ ] Проверить последний бэкап
- [ ] Проверить размер (> 1MB)
- [ ] Проверить целостность (gzip -t)

### Weekly

- [ ] Проверить все бэкапы за неделю
- [ ] Проверить логи бэкапа
- [ ] Проверить место на диске

### Monthly

- [ ] Тестовое восстановление
- [ ] Проверка процедуры восстановления
- [ ] Аудит стратегии бэкапирования

---

## 📞 Контакты

| Роль | Контакты |
|------|----------|
| **DevOps** | devops@yourdomain.com |
| **On-call** | oncall@yourdomain.com |

---

**Последнее обновление:** 2026-03-19  
**Версия:** 1.0
