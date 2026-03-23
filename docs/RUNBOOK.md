# 🚀 Runbook для IT Interview Trainer

## 📋 Оглавление

1. [Контакты](#контакты)
2. [Архитектура](#архитектура)
3. [Мониторинг](#мониторинг)
4. [Деплой](#деплой)
5. [Бэкапы](#бэкапы)
6. [Инциденты](#инциденты)
7. [Чек-листы](#чек-листы)

---

## 📞 Контакты

### Команда

| Роль | Имя | Контакты |
|------|-----|----------|
| **On-call** | Дежурный | oncall@yourdomain.com |
| **DevOps Lead** | ... | devops-lead@yourdomain.com |
| **Tech Lead** | ... | tech-lead@yourdomain.com |
| **CTO** | ... | cto@yourdomain.com |

### Эскалация

```
Уровень 1 → On-call инженер (15 мин)
Уровень 2 → DevOps Lead (30 мин)
Уровень 3 → Tech Lead (1 час)
Уровень 4 → CTO (2 часа)
```

### Внешние сервисы

| Сервис | URL | Статус |
|--------|-----|--------|
| **Grafana** | https://grafana.yourdomain.com | 🟢 |
| **Prometheus** | https://prometheus.yourdomain.com | 🟢 |
| **GitLab CI** | https://gitlab.com/... | 🟢 |
| **Production** | https://yourdomain.com | 🟢 |

---

## 🏗 Архитектура

### Схема инфраструктуры

```
                    ┌─────────────┐
                    │   Nginx     │
                    │  (Reverse   │
                    │   Proxy)    │
                    └──────┬──────┘
                           │
           ┌───────────────┼───────────────┐
           │               │               │
    ┌──────▼──────┐ ┌──────▼──────┐ ┌──────▼──────┐
    │  Frontend   │ │   Backend   │ │   Backend   │
    │   (React)   │ │  (FastAPI)  │ │  (FastAPI)  │
    │   :80       │ │   :8000     │ │   :8000     │
    └─────────────┘ └──────┬──────┘ └──────┬──────┘
                           │               │
                           └───────┬───────┘
                                   │
                    ┌──────────────▼──────────────┐
                    │      PostgreSQL             │
                    │      (Primary)              │
                    └──────────────┬──────────────┘
                                   │
                    ┌──────────────▼──────────────┐
                    │       Redis                 │
                    │    (Cache/Sessions)         │
                    └─────────────────────────────┘
```

### Компоненты

| Сервис | Порт | Описание | Критичность |
|--------|------|----------|-------------|
| **Nginx** | 80, 443 | Reverse proxy, SSL | 🔴 Critical |
| **Backend** | 8000 | FastAPI API | 🔴 Critical |
| **Frontend** | 80 | React SPA | 🟡 High |
| **PostgreSQL** | 5432 | База данных | 🔴 Critical |
| **Redis** | 6379 | Кэш, сессии | 🟡 High |
| **Prometheus** | 9090 | Метрики | 🟢 Medium |
| **Grafana** | 3000 | Дашборды | 🟢 Medium |
| **Loki** | 3100 | Логи | 🟢 Medium |

---

## 📊 Мониторинг

### Дашборды

| Дашборд | URL | Описание |
|---------|-----|----------|
| **Application** | /d/app | Requests, errors, latency |
| **Database** | /d/db | PostgreSQL метрики |
| **Infrastructure** | /d/infra | CPU, memory, disk |
| **Business** | /d/biz | Пользователи, сессии |

### Ключевые метрики (SLO)

| Метрика | Target | Alert |
|---------|--------|-------|
| **Availability** | 99.9% | < 99% |
| **Error Rate** | < 0.1% | > 1% |
| **Latency (p95)** | < 500ms | > 2s |
| **Throughput** | 1000 req/s | < 100 req/s |

### Алерты

| Алерт | Severity | Действие |
|-------|----------|----------|
| **BackendDown** | 🔴 Critical | Проверить логи, перезапустить |
| **DatabaseDown** | 🔴 Critical | Проверить БД, failover |
| **HighErrorRate** | 🟡 Warning | Анализировать ошибки |
| **SlowResponses** | 🟡 Warning | Проверить нагрузку |
| **LowDiskSpace** | 🟡 Warning | Очистить место |
| **BackupFailed** | 🟡 Warning | Проверить скрипт бэкапа |

---

## 🚀 Деплой

### Автоматический (CI/CD)

```bash
# GitLab CI/CD
# 1. Создать тег
git tag v1.2.3
git push origin v1.2.3

# 2. Pipeline запустится автоматически
# https://gitlab.com/.../pipelines

# 3. Deploy to production (manual)
# В GitLab UI нажать "Deploy"
```

### Ручной деплой

```bash
# 1. Подключиться к серверу
ssh user@production-server

# 2. Перейти в директорию
cd /app/it-interview-trainer

# 3. Обновить код
git pull origin main

# 4. Применить миграции
cd backend
source venv/bin/activate
alembic upgrade head

# 5. Пересобрать образы
docker-compose -f docker-compose.prod.yml build

# 6. Перезапустить сервисы
docker-compose -f docker-compose.prod.yml up -d

# 7. Проверить логи
docker-compose -f docker-compose.prod.yml logs -f backend

# 8. Проверить здоровье
curl https://yourdomain.com/health
```

### Rollback

```bash
# 1. Откатить код
git checkout <previous-tag>

# 2. Пересобрать и перезапустить
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d

# 3. Проверить
curl https://yourdomain.com/health
```

---

## 💾 Бэкапы

### Расписание

| Тип | Расписание | Хранение |
|-----|------------|----------|
| **PostgreSQL** | Ежедневно в 02:00 | 30 дней |
| **Weekly** | Каждую пятницу | 8 недель |
| **Monthly** | 1-го числа | 12 месяцев |

### Проверка бэкапа

```bash
# 1. Проверить последний бэкап
ls -lh /app/backups/postgresql/latest.sql.gz

# 2. Проверить целостность
gzip -t /app/backups/postgresql/latest.sql.gz

# 3. Проверить размер (должен быть > 1MB)
du -h /app/backups/postgresql/latest.sql.gz
```

### Восстановление из бэкапа

```bash
# 1. Остановить приложение
docker-compose -f docker-compose.prod.yml down

# 2. Восстановить БД
./scripts/restore_postgres.sh --latest --force

# 3. Запустить приложение
docker-compose -f docker-compose.prod.yml up -d

# 4. Проверить
curl https://yourdomain.com/health
```

---

## 🚨 Инциденты

### Классификация

| Уровень | Описание | Время реакции |
|---------|----------|---------------|
| **P0** | Полный простой | 5 минут |
| **P1** | Критические функции не работают | 15 минут |
| **P2** | Частичная деградация | 1 час |
| **P3** | Минорные проблемы | 4 часа |

### Playbook для типовых инцидентов

#### 1. Backend не отвечает

**Симптомы:**
- 502 Bad Gateway
- Health check fails
- Алерт BackendDown

**Действия:**
```bash
# 1. Проверить статус контейнеров
docker-compose -f docker-compose.prod.yml ps

# 2. Проверить логи
docker-compose -f docker-compose.prod.yml logs backend

# 3. Проверить использование ресурсов
docker stats

# 4. Перезапустить backend
docker-compose -f docker-compose.prod.yml restart backend

# 5. Если не помогло - проверить БД
docker-compose -f docker-compose.prod.yml logs postgres
```

#### 2. База данных недоступна

**Симптомы:**
- Ошибки подключения к БД
- Алерт DatabaseDown
- 500 ошибки в логах

**Действия:**
```bash
# 1. Проверить статус PostgreSQL
docker-compose -f docker-compose.prod.yml ps postgres

# 2. Проверить логи БД
docker-compose -f docker-compose.prod.yml logs postgres

# 3. Проверить подключения
docker-compose -f docker-compose.prod.yml exec postgres \
  psql -U interview_admin -d interview_trainer -c "SELECT count(*) FROM pg_stat_activity;"

# 4. Проверить диск
df -h

# 5. Если диск полон - очистить старые логи
docker-compose -f docker-compose.prod.yml exec postgres \
  rm -rf /var/log/postgresql/*.log
```

#### 3. Высокая нагрузка

**Симптомы:**
- Медленные ответы (>2s)
- Алерт HighLoad
- CPU > 80%

**Действия:**
```bash
# 1. Проверить текущую нагрузку
docker stats

# 2. Проверить активные запросы
docker-compose -f docker-compose.prod.yml exec postgres \
  psql -U interview_admin -d interview_trainer -c \
  "SELECT pid, now() - pg_stat_activity.query_start AS duration, query \
   FROM pg_stat_activity WHERE state = 'active' ORDER BY duration DESC;"

# 3. Увеличить реплики backend
docker-compose -f docker-compose.prod.yml up -d --scale backend=5

# 4. Проверить кэш Redis
docker-compose -f docker-compose.prod.yml exec redis redis-cli INFO
```

#### 4. Утечка памяти

**Симптомы:**
- Memory usage растет постоянно
- OOM killer срабатывает
- Контейнеры перезапускаются

**Действия:**
```bash
# 1. Проверить использование памяти
docker stats

# 2. Найти процесс с утечкой
docker exec -it <container_id> top

# 3. Перезапустить контейнер
docker-compose -f docker-compose.prod.yml restart backend

# 4. Включить memory limits в docker-compose.yml
#   deploy:
#     resources:
#       limits:
#         memory: 512M
```

---

## ✅ Чек-листы

### Daily Check (утром)

- [ ] Проверить дашборд Grafana
- [ ] Проверить алерты за ночь
- [ ] Проверить успешность бэкапов
- [ ] Проверить место на диске
- [ ] Проверить логи ошибок

### Weekly Check (понедельник)

- [ ] Проверить метрики за неделю
- [ ] Проверить производительность
- [ ] Проверить логи на аномалии
- [ ] Обновить зависимости (security patches)
- [ ] Провести тестовое восстановление из бэкапа

### Monthly Check (1-го числа)

- [ ] Аудит безопасности
- [ ] Проверка SLO за месяц
- [ ] Анализ инцидентов
- [ ] Планирование улучшений
- [ ] Тест disaster recovery

### Pre-deploy Checklist

- [ ] Создать бэкап БД
- [ ] Проверить CI/CD pipeline
- [ ] Уведомить команду о деплое
- [ ] Проверить staging окружение
- [ ] Подготовить rollback план

### Post-deploy Checklist

- [ ] Проверить health endpoints
- [ ] Проверить метрики
- [ ] Проверить логи на ошибки
- [ ] Провести smoke тесты
- [ ] Обновить документацию

---

## 📞 Экстренные контакты

### Хостинг провайдер

| Сервис | Контакты | SLA |
|--------|----------|-----|
| **Server Provider** | support@provider.com | 24/7 |
| **Domain Registrar** | support@registrar.com | Business hours |
| **SSL Certificate** | support@ssl-provider.com | 24/7 |

### Команда

```
# On-call ротация
Понедельник-Воскресенье: +1-234-567-8900

# Slack каналы
#devops-alerts - автоматические алерты
#incidents - обсуждение инцидентов
#deployments - деплои
```

---

## 🔧 Полезные команды

### Диагностика

```bash
# Проверка здоровья всех сервисов
docker-compose -f docker-compose.prod.yml ps

# Проверка логов в реальном времени
docker-compose -f docker-compose.prod.yml logs -f

# Проверка использования ресурсов
docker stats

# Проверка сети
docker-compose -f docker-compose.prod.yml exec backend curl http://postgres:5432

# Проверка диска
df -h
du -sh /app/backups/*
```

### Обслуживание

```bash
# Очистка старых образов
docker image prune -a

# Очистка остановленных контейнеров
docker container prune

# Перезапуск всех сервисов
docker-compose -f docker-compose.prod.yml restart

# Полная пересборка
docker-compose -f docker-compose.prod.yml build --no-cache
```

---

**Последнее обновление:** 2026-03-19  
**Версия:** 1.0  
**Ответственный:** DevOps Team
