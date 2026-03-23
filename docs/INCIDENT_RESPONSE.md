# 🚨 Incident Response Guide

## 📋 Оглавление

1. [Классификация инцидентов](#классификация-инцидентов)
2. [Процесс реагирования](#процесс-реагирования)
3. [Playbooks](#playbooks)
4. [Post-mortem](#post-mortem)
5. [Communication](#communication)

---

## 🎯 Классификация инцидентов

### Уровни серьезности

| Уровень | Название | Описание | Время реакции | Примеры |
|---------|----------|----------|---------------|---------|
| **P0** | Critical | Полный простой системы | 5 минут | Backend down, БД недоступна |
| **P1** | High | Критические функции не работают | 15 минут | Аутентификация не работает, сессии не создаются |
| **P2** | Medium | Частичная деградация | 1 час | Медленные ответы, ошибки импорта |
| **P3** | Low | Минорные проблемы | 4 часа | Ошибки в логах, предупреждения |

### Матрица эскалации

```
P0 (Critical):
  0-15 мин  → On-call инженер
  15-30 мин → DevOps Lead
  30-60 мин → Tech Lead
  60+ мин   → CTO

P1 (High):
  0-30 мин  → On-call инженер
  30-60 мин → DevOps Lead
  60+ мин   → Tech Lead

P2 (Medium):
  0-2 часа  → On-call инженер
  2+ часа   → DevOps Lead

P3 (Low):
  0-8 часов → On-call инженер
  8+ часов  → Создать ticket в Jira
```

---

## 🔄 Процесс реагирования

### 1. Обнаружение

**Источники:**
- Алерты от Prometheus/Grafana
- Алерты от Loki (логи)
- Уведомления от пользователей
- Мониторинг uptime (UptimeRobot, Pingdom)

**Первые действия:**
```
1. Подтвердить инцидент
2. Определить уровень (P0-P3)
3. Начать логировать действия в #incidents
4. Назначить Incident Commander (IC)
```

### 2. Диагностика

**Собрать информацию:**
```bash
# Проверить статус сервисов
docker-compose -f docker-compose.prod.yml ps

# Проверить алерты
curl http://localhost:9090/api/v1/alerts

# Проверить логи
docker-compose -f docker-compose.prod.yml logs --tail=100 backend

# Проверить метрики
curl http://localhost:9090/api/v1/query?query=up
```

**Определить scope:**
- Какие сервисы затронуты?
- Какие пользователи затронуты?
- Когда началось?
- Есть ли паттерн?

### 3. Содерживание

**Цель:** Предотвратить дальнейшее распространение

**Действия:**
- Отключить проблемный функционал
- Переключить трафик на backup
- Увеличить ресурсы (scale up)
- Включить rate limiting

### 4. Восстановление

**Цель:** Восстановить работу сервиса

**Стратегии:**
1. **Restart** - Перезапустить сервис
2. **Rollback** - Откатить последние изменения
3. **Failover** - Переключиться на backup
4. **Hotfix** - Применить быстрое исправление

### 5. Пост-мортем

**Цель:** Извлечь уроки и предотвратить повторение

**В течение 24 часов:**
- Созвать post-mortem встречу
- Заполнить post-mortem документ
- Создать action items
- Назначить ответственных

---

## 📚 Playbooks

### PB-001: Backend не отвечает

**Симптомы:**
- 🔴 502 Bad Gateway
- 🔴 Health check fails
- 🔴 Алерт BackendDown

**Действия:**

```bash
# 1. Подтвердить инцидент
curl https://yourdomain.com/health

# 2. Проверить статус контейнеров
docker-compose -f docker-compose.prod.yml ps

# 3. Проверить логи
docker-compose -f docker-compose.prod.yml logs --tail=100 backend

# 4. Проверить использование ресурсов
docker stats

# 5. Попытаться перезапустить
docker-compose -f docker-compose.prod.yml restart backend

# 6. Если не помогло - проверить БД
docker-compose -f docker-compose.prod.yml logs postgres

# 7. Проверить сеть
docker-compose -f docker-compose.prod.yml exec backend \
  curl http://postgres:5432
```

**Эскалация:**
- Если не восстановлено за 15 мин → DevOps Lead
- Если не восстановлено за 30 мин → Tech Lead

---

### PB-002: База данных недоступна

**Симптомы:**
- 🔴 Ошибки подключения к БД в логах
- 🔴 Алерт DatabaseDown
- 🔴 500 ошибки API

**Действия:**

```bash
# 1. Проверить статус PostgreSQL
docker-compose -f docker-compose.prod.yml ps postgres

# 2. Проверить логи БД
docker-compose -f docker-compose.prod.yml logs postgres

# 3. Проверить подключения
docker-compose -f docker-compose.prod.yml exec postgres \
  psql -U interview_admin -d interview_trainer -c \
  "SELECT count(*) FROM pg_stat_activity;"

# 4. Проверить диск
df -h
docker-compose -f docker-compose.prod.yml exec postgres \
  df -h /var/lib/postgresql/data

# 5. Проверить долгие запросы
docker-compose -f docker-compose.prod.yml exec postgres \
  psql -U interview_admin -d interview_trainer -c \
  "SELECT pid, now() - query_start AS duration, query \
   FROM pg_stat_activity \
   WHERE state = 'active' \
   ORDER BY duration DESC LIMIT 10;"

# 6. Если диск полон - очистить
docker-compose -f docker-compose.prod.yml exec postgres \
  rm -rf /var/log/postgresql/*.log

# 7. Перезапустить БД
docker-compose -f docker-compose.prod.yml restart postgres
```

**Восстановление из бэкапа:**

```bash
# 1. Остановить приложение
docker-compose -f docker-compose.prod.yml down

# 2. Восстановить из последнего бэкапа
./scripts/restore_postgres.sh --latest --force

# 3. Запустить приложение
docker-compose -f docker-compose.prod.yml up -d

# 4. Проверить
curl https://yourdomain.com/health
```

---

### PB-003: Высокая нагрузка (High Load)

**Симптомы:**
- 🟡 Медленные ответы (>2s)
- 🟡 Алерт HighLoad
- 🟡 CPU > 80%
- 🟡 Memory > 90%

**Действия:**

```bash
# 1. Проверить текущую нагрузку
docker stats

# 2. Проверить активные запросы в БД
docker-compose -f docker-compose.prod.yml exec postgres \
  psql -U interview_admin -d interview_trainer -c \
  "SELECT count(*) FROM pg_stat_activity WHERE state = 'active';"

# 3. Увеличить реплики backend
docker-compose -f docker-compose.prod.yml up -d --scale backend=5

# 4. Проверить кэш Redis
docker-compose -f docker-compose.prod.yml exec redis \
  redis-cli INFO stats

# 5. Включить rate limiting (если еще не включен)
# Проверить nginx config
docker-compose -f docker-compose.prod.yml exec nginx \
  nginx -t

# 6. Очистить кэш (если нужно)
docker-compose -f docker-compose.prod.yml exec redis \
  redis-cli FLUSHDB
```

---

### PB-004: Утечка памяти (Memory Leak)

**Симптомы:**
- 🟡 Memory usage постоянно растет
- 🟡 OOM killer срабатывает
- 🟡 Контейнеры перезапускаются

**Действия:**

```bash
# 1. Проверить использование памяти
docker stats

# 2. Найти процесс с утечкой
docker exec -it <container_id> top

# 3. Проверить логи на OOM
dmesg | grep -i "out of memory"

# 4. Перезапустить контейнер
docker-compose -f docker-compose.prod.yml restart backend

# 5. Включить memory limits
# Отредактировать docker-compose.prod.yml:
#   deploy:
#     resources:
#       limits:
#         memory: 512M

# 6. Применить изменения
docker-compose -f docker-compose.prod.yml up -d
```

---

### PB-005: Ошибки аутентификации

**Симптомы:**
- 🟡 Пользователи не могут войти
- 🟡 Много 401 ошибок в логах
- 🟡 Алерт AuthErrors

**Действия:**

```bash
# 1. Проверить логи auth
docker-compose -f docker-compose.prod.yml logs backend | \
  grep -i "auth\|login\|token"

# 2. Проверить JWT секрет
docker-compose -f docker-compose.prod.yml exec backend \
  env | grep SECRET

# 3. Проверить подключение к БД
docker-compose -f docker-compose.prod.yml exec backend \
  python -c "from app.database.engine import SessionLocal; \
             db = SessionLocal(); \
             print('DB OK')"

# 4. Проверить время на сервере
date
docker-compose -f docker-compose.prod.yml exec backend date

# 5. Перезапустить backend
docker-compose -f docker-compose.prod.yml restart backend
```

---

### PB-006: Бэкап не создан

**Симптомы:**
- 🟢 Алерт BackupFailed
- 🟢 Последний бэкап старше 25 часов

**Действия:**

```bash
# 1. Проверить последний бэкап
ls -lh /app/backups/postgresql/latest.sql.gz

# 2. Проверить логи бэкапа
cat /app/backups/backup.log

# 3. Проверить скрипт бэкапа
cat /app/scripts/backup_postgres.sh

# 4. Запустить бэкап вручную
./scripts/backup_postgres.sh --docker

# 5. Проверить результат
ls -lh /app/backups/postgresql/

# 6. Проверить cron
crontab -l | grep backup
```

---

## 📄 Post-mortem Template

### Post-mortem документа

```markdown
# Post-mortem: [Название инцидента]

## Информация

- **Дата:** YYYY-MM-DD
- **Время:** HH:MM - HH:MM (UTC)
- **Длительность:** X часов Y минут
- **Уровень:** P0/P1/P2/P3
- **Incident Commander:** @username

## Резюме

Краткое описание инцидента (2-3 предложения)

## Timeline

| Время | Событие |
|-------|---------|
| HH:MM | Обнаружен инцидент |
| HH:MM | Начата диагностика |
| HH:MM | Определена причина |
| HH:MM | Начато восстановление |
| HH:MM | Сервис восстановлен |

## Причина

Root cause анализа (5 Why's)

1. Почему X случилось? → Потому что Y
2. Почему Y случилось? → Потому что Z
...

## Воздействие

- Пользователей затронуто: X
- Потеря доходов: $X
- Репутационный ущерб: Low/Medium/High

## Что сработало хорошо

- ✅ Алерты сработали вовремя
- ✅ Runbook был полезен
- ✅ Команда быстро отреагировала

## Что можно улучшить

- ❌ Не хватило документации
- ❌ Долгая эскалация
- ❌ Нет автоматического failover

## Action Items

| Задача | Ответственный | Срок | Статус |
|--------|--------------|------|--------|
| Обновить runbook | @user | YYYY-MM-DD | TODO |
| Добавить мониторинг | @user | YYYY-MM-DD | TODO |
| Настроить авто-scaling | @user | YYYY-MM-DD | TODO |

## Уроки

Что мы узнали и как предотвратим в будущем:
1. ...
2. ...
```

---

## 📢 Communication

### Шаблоны сообщений

#### Initial Alert (в #incidents)

```
🚨 **INCIDENT ALERT** 🚨

**Level:** P0/P1/P2/P3
**Service:** Backend/Database/Frontend
**Symptoms:** 502 errors, health check fails
**Detected:** HH:MM UTC
**On-call:** @username

Investigating...
```

#### Update (каждые 30 мин для P0/P1)

```
🔄 **INCIDENT UPDATE** 🔄

**Level:** P0/P1
**Status:** Investigating / Identified / Fixing / Monitoring
**Progress:** Found root cause, applying fix
**Next update:** HH:MM UTC
```

#### Resolution

```
✅ **INCIDENT RESOLVED** ✅

**Level:** P0/P1
**Duration:** X hours Y minutes
**Root cause:** [brief description]
**Status:** Service restored, monitoring

Post-mortem scheduled for YYYY-MM-DD
```

### Уведомление пользователей

```
Subject: [Resolved] Service Disruption on YYYY-MM-DD

Dear Users,

We experienced service disruption from HH:MM to HH:MM UTC.
The issue has been resolved and all services are operating normally.

Impact: Some users experienced errors when [doing X]
Root cause: [brief non-technical description]

We apologize for the inconvenience and are taking steps to prevent this from happening again.

Best regards,
IT Interview Trainer Team
```

---

## 📞 Контакты для эскалации

| Роль | Имя | Телефон | Telegram |
|------|-----|---------|----------|
| **On-call** | Дежурный | +1-234-567-8900 | @oncall |
| **DevOps Lead** | ... | +1-234-567-8901 | @devops-lead |
| **Tech Lead** | ... | +1-234-567-8902 | @tech-lead |
| **CTO** | ... | +1-234-567-8903 | @cto |

---

**Последнее обновление:** 2026-03-19  
**Версия:** 1.0  
**Ответственный:** DevOps Team
