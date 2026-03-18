# DevOps Roadmap для IT Interview Trainer

## ✅ Выполнено

### 1. Grafana дашборды

- [x] **Grafana дашборды** — 3 дашборда созданы:
  - `backend-overview.json` — метрики приложения
  - `infrastructure.json` — инфраструктурные метрики
  - `loki-monitoring.json` — мониторинг логов

### 2. Alertmanager и мониторинг

- [x] **Alertmanager** — алерты в Telegram при ошибках:
  - ✅ Настроен Telegram бот
  - ✅ Созданы правила алертов (BackendDown, HighErrorRate, HighLatency, и т.д.)
  - ✅ Настроена маршрутизация по severity (critical/warning)
  - ✅ Протестирована доставка уведомлений

- [x] **Дополнительные алерты** — 18 правил мониторинга:
  - ✅ Backend Health: BackendDown, BackendHighErrorRate, BackendHighLatency
  - ✅ Container: ContainerHighMemoryUsage, ContainerRestarting, ContainerHighDiskUsage
  - ✅ Application: BackendHighRequestRate, BackendLowThroughput
  - ✅ Infrastructure: LokiDown, PromtailDown, HighLogVolume
  - ✅ Alertmanager: AlertmanagerConfigNotSynced, AlertmanagerNotificationFailed
  - ✅ Prometheus: PrometheusTargetScrapeFailed, PrometheusRuleEvaluationFailed
  - ✅ Database: DatabaseConnectionHigh
  - ✅ Host: HighMemoryUsage, HighCPUUsage

### 3. PostgreSQL миграция

- [x] **Миграция на PostgreSQL** — production-ready БД:
  - ✅ PostgreSQL 15-alpine запущен (порт 5433)
  - ✅ pgAdmin доступен (http://localhost:5050)
  - ✅ Backend подключён к PostgreSQL
  - ✅ 12 таблиц созданы автоматически
  - ✅ Исправлен `engine.py` для работы с PostgreSQL/SQLite
  - ✅ Добавлен `psycopg2-binary` в зависимости
  - ✅ Обновлён `nginx.conf` для правильного proxy_pass

### 4. Очистка и пересборка

- [x] **Очистка системы**:
  - ✅ Удалены старые контейнеры GitLab CI runner
  - ✅ Удалены dangling Docker образы
  - ✅ Удалены неиспользуемые тома
  - ✅ Освобождено ~106 MB места

---

## 🚧 В работе

- [ ] **Kubernetes манифесты** — Deployment, Service, Ingress
- [ ] **Helm chart** — упаковка приложения
- [ ] **Real deploy pipeline** — реальный деплой вместо заглушки

---

## 📋 Текущая архитектура

### Сервисы и порты

| Сервис | Контейнер | Порт | URL |
|--------|-----------|------|-----|
| **Frontend** | it-interview-frontend | 3000 | http://localhost:3000 |
| **Backend API** | it-interview-backend | 8000 | http://localhost:8000 |
| **PostgreSQL** | it-interview-postgres | 5433 | localhost:5433 |
| **pgAdmin** | it-interview-pgadmin | 5050 | http://localhost:5050 |
| **Prometheus** | prometheus | 9090 | http://localhost:9090 |
| **Alertmanager** | alertmanager | 9093 | http://localhost:9093 |
| **Grafana** | grafana | 3002 | http://localhost:3002 |
| **Loki** | loki | 3100 | http://localhost:3100 |
| **Promtail** | promtail | — | — |

### Доступы

| Сервис | Логин | Пароль |
|--------|-------|--------|
| **pgAdmin** | admin@example.com | admin123 |
| **Grafana** | admin | admin123 |
| **Backend API** | admin@example.com | admin123 |

### Базы данных

- **PostgreSQL:** `interview_trainer`
- **Пользователь БД:** `postgres` / `postgres123`
- **Таблицы:** 12 (users, professions, questions, answers, sessions, и т.д.)

---

## 📁 Структура файлов

```
it_interVI.it-interview-trainer/
├── docker-compose.yml              # Основной compose (backend, frontend, postgres)
├── docker-compose.db.yml           # PostgreSQL + pgAdmin
├── docker-compose.monitoring.yml   # Prometheus + Grafana
├── docker-compose.loki.yml         # Loki + Promtail + Alertmanager
├── monitoring/
│   ├── prometheus/
│   │   ├── prometheus.yml          # Конфигурация Prometheus
│   │   └── alerts.yml              # 18 правил алертов
│   ├── alertmanager/
│   │   └── alertmanager.yml        # Конфигурация уведомлений
│   ├── grafana/
│   │   └── dashboards/             # 3 дашборда
│   ├── loki/
│   │   └── loki-config.yml         # Конфигурация Loki
│   └── promtail/
│       └── promtail-config.yml     # Конфигурация Promtail
├── backend/
│   ├── app/
│   │   ├── core/config.py          # Настройки (DATABASE_URL)
│   │   └── database/engine.py      # SQLAlchemy engine (SQLite/PostgreSQL)
│   └── requirements.txt            # psycopg2-binary добавлен
└── frontend/
    └── nginx.conf                  # Исправлен proxy_pass
```

---

## 🔧 Полезные команды

### Управление контейнерами

```bash
# Запуск всех сервисов
docker-compose -f docker-compose.yml up -d
docker-compose -f docker-compose.db.yml up -d
docker-compose -f docker-compose.monitoring.yml up -d
docker-compose -f docker-compose.loki.yml up -d

# Остановка всех
docker-compose down
docker-compose -f docker-compose.db.yml down
docker-compose -f docker-compose.monitoring.yml down
docker-compose -f docker-compose.loki.yml down

# Пересборка образов
docker-compose build backend frontend

# Просмотр логов
docker logs it-interview-backend --tail 50
docker logs prometheus --tail 50

# Очистка
docker container prune -f
docker image prune -f
docker volume prune -f
```

### PostgreSQL команды

```bash
# Подключение к БД
docker exec -it it-interview-postgres psql -U postgres -d interview_trainer

# Показать таблицы
\dt

# Показать структуру
\d users

# Выйти
\q

# Бэкап
docker exec it-interview-postgres pg_dump -U postgres interview_trainer > backup.sql

# Восстановление
cat backup.sql | docker exec -i it-interview-postgres psql -U postgres -d interview_trainer
```

### Проверка здоровья

```bash
# Backend
curl http://localhost:8000/health

# Prometheus
curl http://localhost:9090/-/healthy

# Alertmanager
curl http://localhost:9093/-/healthy

# Frontend
curl http://localhost:3000/health
```

---

## 📊 Мониторинг

### Prometheus алерты (18 правил)

| Категория | Алерты |
|-----------|--------|
| **Backend** | BackendDown, BackendHighErrorRate, BackendHighLatency, BackendHighRequestRate, BackendLowThroughput |
| **Container** | ContainerHighMemoryUsage, ContainerRestarting, ContainerHighDiskUsage |
| **Infrastructure** | LokiDown, PromtailDown, HighLogVolume |
| **Alertmanager** | AlertmanagerConfigNotSynced, AlertmanagerNotificationFailed |
| **Prometheus** | PrometheusTargetScrapeFailed, PrometheusRuleEvaluationFailed |
| **Database** | DatabaseConnectionHigh |
| **Host** | HighMemoryUsage, HighCPUUsage |

### Уведомления

- **Telegram:** Критические и предупреждающие алерты
- **Маршрутизация:**
  - `critical` → мгновенное уведомление, повтор каждые 1ч
  - `warning` → повтор каждые 6ч

---

## 🎯 Следующие шаги

### 1. Kubernetes манифесты (Приоритет: 🔴)

**Цель:** Развернуть приложение в K8s

**Задачи:**
- [ ] Создать `k8s/namespace.yaml`
- [ ] Создать `k8s/backend-deployment.yaml`
- [ ] Создать `k8s/frontend-deployment.yaml`
- [ ] Создать `k8s/services.yaml`
- [ ] Создать `k8s/ingress.yaml`
- [ ] Создать `k8s/configmap.yaml`
- [ ] Создать `k8s/secrets.yaml` (template)
- [ ] Создать `k8s/postgres-statefulset.yaml`

### 2. Helm chart (Приоритет: 🟡)

**Цель:** Упаковать приложение для упрощения деплоя

**Задачи:**
- [ ] Создать структуру Helm chart
- [ ] Добавить `values.yaml` с конфигурацией
- [ ] Добавить templates для всех K8s ресурсов
- [ ] Протестировать установку в minikube/kind

### 3. Real deploy pipeline (Приоритет: 🔴)

**Цель:** Реализовать реальный деплой в CI/CD

**Задачи:**
- [ ] Настроить deploy в `.gitlab-ci.yml` (kubectl apply)
- [ ] Добавить manual approval для production
- [ ] Настроить уведомления о деплое
- [ ] Добавить rollback механизм

---

## 📈 Статистика проекта

| Метрика | Значение |
|---------|----------|
| **Контейнеров** | 9 |
| **Docker образов** | 14 |
| **Правил алертов** | 18 |
| **Grafana дашбордов** | 3 |
| **Таблиц PostgreSQL** | 12 |
| **Пользователей** | 1 (admin) |
| **Вопросов в базе** | 5 (Frontend: 2, Backend: 2, Fullstack: 1) |

---

## 📝 История изменений

### 2026-03-18

- ✅ Настроены Grafana дашборды (3 шт.)
- ✅ Настроен Alertmanager с Telegram уведомлениями
- ✅ Добавлено 18 правил алертов
- ✅ Миграция на PostgreSQL завершена
- ✅ Добавлен pgAdmin для администрирования
- ✅ Исправлен `engine.py` для работы с PostgreSQL/SQLite
- ✅ Исправлен `nginx.conf` (proxy_pass)
- ✅ Проведена очистка системы (~106 MB освобождено)
- ✅ Все сервисы пересобраны и работают

---

**Последнее обновление:** 18 марта 2026 г.
