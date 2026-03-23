# 🚀 Руководство по деплою IT Interview Trainer

## 📋 Оглавление

1. [Требования](#требования)
2. [Подготовка](#подготовка)
3. [Развертывание](#развертывание)
4. [CI/CD](#cicd)
5. [Мониторинг](#мониторинг)
6. [Troubleshooting](#troubleshooting)

---

## 🛠 Требования

### Минимальные требования к серверу

| Ресурс | Minimum | Recommended | Production |
|--------|---------|-------------|------------|
| **CPU** | 2 cores | 4 cores | 8+ cores |
| **RAM** | 4 GB | 8 GB | 16+ GB |
| **Disk** | 50 GB | 100 GB | 200+ GB SSD |
| **Network** | 100 Mbps | 1 Gbps | 1 Gbps+ |

### Программное обеспечение

```bash
# Обязательное ПО
Docker >= 20.10
Docker Compose >= 2.0
Git
curl, wget

# Опционально
Python 3.9+ (для локальной разработки)
Node.js 18+ (для локальной разработки)
```

### Проверка требований

```bash
# Проверка Docker
docker --version
docker-compose --version

# Проверка ресурсов
nproc              # CPU
free -h            # RAM
df -h              # Disk
```

---

## 📦 Подготовка

### 1. Клонирование репозитория

```bash
# Клонировать репозиторий
git clone https://gitlab.com/your-repo/it-interview-trainer.git
cd it-interview-trainer

# Проверить структуру
ls -la
```

### 2. Настройка переменных окружения

```bash
# Создать production .env файл
cp .env.example .env.production

# Отредактировать .env.production
nano .env.production
```

### 3. Обязательные переменные

```bash
# .env.production

# === Database ===
POSTGRES_DB=interview_trainer
POSTGRES_USER=interview_admin
POSTGRES_PASSWORD=<сгенерируйте: openssl rand -base64 32>

# === Security ===
SECRET_KEY=<сгенерируйте: openssl rand -hex 32>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# === CORS ===
CORS_ORIGINS=https://yourdomain.com
CORS_ALLOW_CREDENTIALS=true

# === Production ===
DEBUG=false
RATE_LIMIT_PER_MINUTE=10

# === Grafana ===
GRAFANA_ADMIN_USER=admin
GRAFANA_ADMIN_PASSWORD=<смените пароль>
```

### 4. Генерация секретов

```bash
# Сгенерировать SECRET_KEY
echo "SECRET_KEY=$(openssl rand -hex 32)" >> .env.production

# Сгенерировать POSTGRES_PASSWORD
echo "POSTGRES_PASSWORD=$(openssl rand -base64 32)" >> .env.production

# Сгенерировать GRAFANA_PASSWORD
echo "GRAFANA_ADMIN_PASSWORD=$(openssl rand -base64 24)" >> .env.production
```

### 5. SSL сертификаты

```bash
# Создать директорию для SSL
mkdir -p nginx/ssl

# Создать самоподписанные сертификаты (для testing)
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout nginx/ssl/server.key \
  -out nginx/ssl/server.crt \
  -subj "/C=US/ST=State/L=City/O=Organization/CN=yourdomain.com"

# Для production используйте Let's Encrypt
# certbot --nginx -d yourdomain.com
```

### 6. Настройка firewall

```bash
# UFW (Ubuntu)
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS
ufw allow 22/tcp    # SSH
ufw deny 5432/tcp   # PostgreSQL (internal only)
ufw deny 6379/tcp   # Redis (internal only)
ufw deny 9090/tcp   # Prometheus (internal only)
ufw deny 3000/tcp   # Grafana (internal only, or allow with auth)
ufw enable

# Проверка
ufw status
```

---

## 🚀 Развертывание

### Вариант 1: Production деплой

```bash
# 1. Загрузить .env.production на сервер
scp .env.production user@server:/app/it-interview-trainer/

# 2. Подключиться к серверу
ssh user@server
cd /app/it-interview-trainer

# 3. Запустить production стек
docker-compose -f docker-compose.prod.yml up -d

# 4. Проверить статус
docker-compose -f docker-compose.prod.yml ps

# 5. Проверить логи
docker-compose -f docker-compose.prod.yml logs -f backend
```

### Вариант 2: Staging деплой

```bash
# Staging окружение (тестирование перед production)
docker-compose -f docker-compose.staging.yml up -d

# Проверка
curl http://localhost:8080/health
```

### Вариант 3: Development (локально)

```bash
# Локальная разработка
docker-compose up -d

# Backend: http://localhost:8000
# Frontend: http://localhost:3000
# Swagger: http://localhost:8000/docs
```

### Проверка деплоя

```bash
# 1. Health check
curl https://yourdomain.com/health
# Ожидаемый ответ: {"status":"healthy"}

# 2. API check
curl https://yourdomain.com/api/professions
# Ожидаемый ответ: список профессий

# 3. Frontend check
curl https://yourdomain.com
# Ожидаемый ответ: HTML страницы

# 4. Metrics check
curl https://yourdomain.com/metrics
# Ожидаемый ответ: Prometheus метрики
```

---

## 🔄 CI/CD

### GitLab CI/CD Pipeline

```yaml
# .gitlab-ci.yml
stages:
  - test
  - build
  - security
  - deploy
  - smoke-test

# 1. Тесты
backend-tests:
  stage: test
  script:
    - cd backend
    - pip install -r requirements.txt
    - pip install -r requirements-dev.txt
    - pytest ../tests/ -v --tb=short

frontend-tests:
  stage: test
  script:
    - cd frontend
    - npm ci
    - npm run lint
    - npm run build

# 2. Сборка образов
docker-build-backend:
  stage: build
  script:
    - docker build -t $CI_REGISTRY_IMAGE/backend:$CI_COMMIT_SHA ./backend
    - docker push $CI_REGISTRY_IMAGE/backend:$CI_COMMIT_SHA

docker-build-frontend:
  stage: build
  script:
    - docker build -t $CI_REGISTRY_IMAGE/frontend:$CI_COMMIT_SHA ./frontend
    - docker push $CI_REGISTRY_IMAGE/frontend:$CI_COMMIT_SHA

# 3. Security scan
security-scan:
  stage: security
  script:
    - pip install safety bandit
    - safety check -r backend/requirements.txt
    - bandit -r backend/app/

# 4. Deploy to staging
deploy-staging:
  stage: deploy
  script:
    - ssh user@staging-server "cd /app && docker-compose pull && docker-compose up -d"
  environment:
    name: staging
  only:
    - develop

# 5. Deploy to production
deploy-production:
  stage: deploy
  script:
    - ssh user@prod-server "cd /app && docker-compose pull && docker-compose up -d"
  environment:
    name: production
  only:
    - main
  when: manual

# 6. Smoke tests
smoke-tests:
  stage: smoke-test
  script:
    - python tests/smoke/test_production.py
  only:
    - main
```

### Ручной деплой (скрипт)

```bash
#!/bin/bash
# scripts/deploy.sh

set -e

echo "🚀 Starting deployment..."

# 1. Pull latest code
git pull origin main

# 2. Build images
docker-compose -f docker-compose.prod.yml build

# 3. Run migrations
docker-compose -f docker-compose.prod.yml run backend alembic upgrade head

# 4. Restart services
docker-compose -f docker-compose.prod.yml up -d

# 5. Wait for services
sleep 10

# 6. Health check
echo "🏥 Running health checks..."
curl -f http://localhost:8000/health || exit 1

echo "✅ Deployment successful!"
```

---

## 📊 Мониторинг

### Развертывание мониторинга

```bash
# Запустить стек мониторинга
docker-compose -f docker-compose.monitoring.yml up -d

# Сервисы:
# Prometheus: http://localhost:9090
# Grafana: http://localhost:3000 (admin/admin)
# Loki: http://localhost:3100
```

### Настройка Grafana

```bash
# 1. Открыть Grafana
# http://localhost:3000

# 2. Добавить datasource
# Configuration → Data sources → Add data source → Prometheus
# URL: http://prometheus:9090

# 3. Добавить Loki datasource
# Configuration → Data sources → Add data source → Loki
# URL: http://loki:3100

# 4. Импортировать дашборды
# Dashboards → Import → Upload JSON
```

### Prometheus метрики

```bash
# Проверка метрик backend
curl http://localhost:8000/metrics

# Ключевые метрики:
# http_requests_total - всего запросов
# http_request_duration_seconds - время ответа
# http_requests_in_progress - текущие запросы
```

### Алерты

```yaml
# prometheus/alerts.yml
groups:
  - name: application
    rules:
      - alert: BackendDown
        expr: up{job="backend"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Backend down"

      - alert: HighErrorRate
        expr: sum(rate(http_requests_total{status=~"5.."}[5m])) > 0.1
        for: 5m
        labels:
          severity: warning
```

---

## 🔧 Troubleshooting

### Backend не запускается

```bash
# 1. Проверить логи
docker-compose -f docker-compose.prod.yml logs backend

# 2. Проверить переменные окружения
docker-compose -f docker-compose.prod.yml exec backend env

# 3. Проверить подключение к БД
docker-compose -f docker-compose.prod.yml exec backend \
  python -c "from app.database.engine import engine; print('OK')"

# 4. Перезапустить
docker-compose -f docker-compose.prod.yml restart backend
```

### База данных не подключается

```bash
# 1. Проверить статус PostgreSQL
docker-compose -f docker-compose.prod.yml ps postgres

# 2. Проверить логи БД
docker-compose -f docker-compose.prod.yml logs postgres

# 3. Проверить сеть
docker-compose -f docker-compose.prod.yml exec backend \
  nc -zv postgres 5432

# 4. Применить миграции
docker-compose -f docker-compose.prod.yml run backend alembic upgrade head
```

### Frontend не загружается

```bash
# 1. Проверить сборку
docker-compose -f docker-compose.prod.yml logs frontend

# 2. Проверить nginx
docker-compose -f docker-compose.prod.yml logs nginx

# 3. Проверить подключение к backend
docker-compose -f docker-compose.prod.yml exec frontend \
  curl http://backend:8000/health
```

### Места на диске мало

```bash
# 1. Проверить место
df -h

# 2. Очистить старые образы
docker image prune -a

# 3. Очистить логи
docker-compose -f docker-compose.prod.yml logs --tail=100

# 4. Очистить старые бэкапы
find /app/backups -name "*.sql.gz" -mtime +30 -delete
```

### Миграции не применяются

```bash
# 1. Проверить текущую версию
docker-compose -f docker-compose.prod.yml run backend alembic current

# 2. Применить миграции
docker-compose -f docker-compose.prod.yml run backend alembic upgrade head

# 3. Проверить историю
docker-compose -f docker-compose.prod.yml run backend alembic history
```

---

## 📋 Чек-листы

### Pre-deploy

- [ ] Создать бэкап БД
- [ ] Проверить CI/CD pipeline
- [ ] Проверить .env.production
- [ ] Проверить SSL сертификаты
- [ ] Уведомить команду

### Deploy

- [ ] Запустить docker-compose
- [ ] Проверить статус сервисов
- [ ] Проверить логи
- [ ] Применить миграции
- [ ] Проверить health endpoints

### Post-deploy

- [ ] Проверить frontend
- [ ] Проверить API
- [ ] Проверить метрики
- [ ] Проверить логи
- [ ] Провести smoke тесты
- [ ] Обновить документацию

---

## 📞 Контакты

| Роль | Контакты |
|------|----------|
| **DevOps** | devops@yourdomain.com |
| **On-call** | oncall@yourdomain.com |
| **Slack** | #deployments |

---

**Последнее обновление:** 2026-03-19  
**Версия:** 1.0
