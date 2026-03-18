# DevOps Roadmap для IT Interview Trainer

## ✅ Выполнено

- [x] **Grafana дашборды** — 3 дашборда созданы:
  - `backend-overview.json` — метрики приложения
  - `infrastructure.json` — инфраструктурные метрики
  - `loki-monitoring.json` — мониторинг логов

- [x] **Alertmanager** — алерты в Telegram при ошибках:
  - ✅ Настроен Telegram бот
  - ✅ Созданы правила алертов (BackendDown, HighErrorRate, HighLatency, и т.д.)
  - ✅ Настроена маршрутизация по severity (critical/warning)
  - ✅ Протестирована доставка уведомлений

## 🚧 В работе

- [x] **Дополнительные алерты** — нагрузка, память, диск:
  - ✅ ContainerHighMemoryUsage — память контейнеров
  - ✅ ContainerRestarting — перезапуск контейнеров
  - ✅ BackendHighRequestRate — высокий трафик
  - ✅ BackendLowThroughput — низкая активность
  - ✅ ContainerHighDiskUsage — дисковое пространство
  - ✅ AlertmanagerNotificationFailed — ошибки уведомлений
  - ✅ PrometheusRuleEvaluationFailed — ошибки правил
- [ ] **Миграция на PostgreSQL** — production-ready БД
- [ ] **Kubernetes манифесты** — Deployment, Service, Ingress
- [ ] **Helm chart** — упаковка приложения
- [ ] **Real deploy pipeline** — реальный деплой вместо заглушки

## 📋 План работ

### 1. Alertmanager (Приоритет: 🔴 Высокий)

**Цель:** Настроить уведомления в Telegram при:
- Ошибках 5xx > 5% запросов
- Downtime приложения > 1 минуты
- High latency (p95 > 1s)

**Задачи:**
- [ ] Создать `monitoring/alertmanager/alertmanager.yml`
- [ ] Настроить Telegram бота (webhook)
- [ ] Добавить routing rules
- [ ] Протестировать алерты

### 2. PostgreSQL миграция (Приоритет: 🔴 Высокий)

**Цель:** Заменить SQLite на PostgreSQL для production

**Задачи:**
- [ ] Добавить PostgreSQL в docker-compose
- [ ] Обновить `backend/app/core/config.py`
- [ ] Обновить миграции Alembic
- [ ] Протестировать на локальном окружении
- [ ] Настроить pgAdmin для администрирования

### 3. Kubernetes манифесты (Приоритет: 🔴 Высокий)

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

### 4. Helm chart (Приоритет: 🟡 Средний)

**Цель:** Упаковать приложение для упрощения деплоя

**Задачи:**
- [ ] Создать структуру Helm chart
- [ ] Добавить values.yaml с конфигурацией
- [ ] Добавить templates для всех K8s ресурсов
- [ ] Протестировать установку в minikube/kind

### 5. Real deploy pipeline (Приоритет: 🔴 Высокий)

**Цель:** Реализовать реальный деплой в CI/CD

**Задачи:**
- [ ] Настроить deploy в .gitlab-ci.yml (kubectl apply)
- [ ] Добавить manual approval для production
- [ ] Настроить уведомления о деплое
- [ ] Добавить rollback механизм

---

## 🎯 Следующий шаг

Выберите задачу для реализации:
1. **Alertmanager** — быстрая победа, улучшит observability
2. **PostgreSQL** — критично для production
3. **Kubernetes** — основа для оркестрации
4. **Helm** — упрощение деплоя
5. **Deploy pipeline** — автоматизация релизов