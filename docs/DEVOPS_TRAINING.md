# DevOps Training — История обучения

**Студент:** Владелец проекта IT Interview Trainer  
**Цель:** Стать DevOps инженером  
**Полигон:** Проект it_interVI.it-interview-trainer  

---

## 📅 Урок 1: Введение в мониторинг (16 марта 2026)

### Цель урока
Настроить систему мониторинга для FastAPI приложения:
- Prometheus — сбор метрик
- Grafana — визуализация
- Научиться добавлять метрики в приложение

---

## ✅ Выполненные шаги

### Шаг 1: Создание структуры директорий

```bash
mkdir -p monitoring/prometheus
mkdir -p monitoring/grafana/provisioning/dashboards
mkdir -p monitoring/grafana/provisioning/datasources
mkdir -p monitoring/grafana/dashboards
mkdir -p monitoring/alertmanager
```

**Статус:** ✅ Выполнено

---

### Шаг 2: Конфигурация Prometheus

**Файл:** `monitoring/prometheus/prometheus.yml`

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'backend'
    static_configs:
      - targets: ['backend:8000']
    metrics_path: /metrics
```

**Статус:** ✅ Выполнено

---

### Шаг 3: Добавление метрик в FastAPI

**Файл:** `backend/app/main.py`

**Изменения:**
1. Добавлены импорты:
   ```python
   from prometheus_client import generate_latest, Counter, Histogram
   from fastapi.responses import Response
   from starlette.requests import Request
   import time
   
   CONTENT_TYPE = "text/plain; version=0.0.4; charset=utf-8"
   ```

2. Созданы метрики:
   ```python
   REQUEST_COUNT = Counter(
       'http_requests_total',
       'Total HTTP requests',
       ['method', 'endpoint', 'status']
   )
   
   REQUEST_TIME = Histogram(
       'http_request_duration_seconds',
       'HTTP request duration',
       ['method', 'endpoint']
   )
   ```

3. Добавлен middleware внутри `create_app()`:
   ```python
   @app.middleware("http")
   async def track_requests(request: Request, call_next):
       start_time = time.time()
       response = await call_next(request)
       duration = time.time() - start_time
       
       REQUEST_COUNT.labels(
           method=request.method,
           endpoint=request.url.path,
           status=response.status_code
       ).inc()
       
       REQUEST_TIME.labels(
           method=request.method,
           endpoint=request.url.path
       ).observe(duration)
       
       return response
   ```

4. Добавлен endpoint `/metrics`:
   ```python
   @app.get("/metrics")
   async def metrics():
       return Response(generate_latest(), media_type=CONTENT_TYPE)
   ```

**Статус:** ✅ Выполнено

---

### Шаг 4: Обновление зависимостей

**Файл:** `backend/requirements.txt`

Добавлено:
```
prometheus-client>=0.19.0
```

**Статус:** ✅ Выполнено

---

### Шаг 5: Docker volume для hot-reload

**Файл:** `docker-compose.yml`

Добавлен volume в сервис backend:
```yaml
volumes:
  - ./backend/data:/app/data
  - ./backups:/app/backups
  - ./backend/app:/app/app  # ← Добавлено для разработки
```

**Статус:** ✅ Выполнено

---

### Шаг 6: Конфигурация Grafana

**Файл:** `monitoring/grafana/provisioning/datasources/datasources.yml`

```yaml
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
    editable: true
```

**Файл:** `monitoring/grafana/provisioning/dashboards/dashboards.yml`

```yaml
apiVersion: 1

providers:
  - name: 'Default'
    orgId: 1
    folder: ''
    type: file
    disableDeletion: false
    updateIntervalSeconds: 10
    options:
      path: /etc/grafana/provisioning/dashboards
```

**Статус:** ✅ Выполнено

---

### Шаг 7: Docker Compose для мониторинга

**Файл:** `docker-compose.monitoring.yml`

```yaml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
    restart: unless-stopped
    networks:
      - it-interview-network

  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    ports:
      - "3001:3000"
    volumes:
      - grafana_data:/var/lib/grafana
      - ./monitoring/grafana/provisioning/datasources:/etc/grafana/provisioning/datasources
      - ./monitoring/grafana/provisioning/dashboards:/etc/grafana/provisioning/dashboards
      - ./monitoring/grafana/dashboards:/etc/grafana/provisioning/dashboards/dashboards
    environment:
      - GF_SECURITY_ADMIN_USER=admin
      - GF_SECURITY_ADMIN_PASSWORD=admin123
      - GF_USERS_ALLOW_SIGN_UP=false
    restart: unless-stopped
    networks:
      - it-interview-network
    depends_on:
      - prometheus

volumes:
  prometheus_data:
  grafana_data:

networks:
  it-interview-network:
    external: true
```

**Статус:** ✅ Выполнено

---

### Шаг 8: Запуск и проверка

**Команды:**
```bash
docker compose -f docker-compose.yml -f docker-compose.monitoring.yml up -d
docker compose ps
```

**Результат:**
- ✅ Prometheus: http://localhost:9090 (up)
- ✅ Grafana: http://localhost:3001 (up)
- ✅ Backend: http://localhost:8000/metrics (up)
- ✅ Метрики собираются: `http_requests_total`, `http_request_duration_seconds`

**Статус:** ✅ Выполнено

---

### Шаг 9: Grafana дашборд

**Созданные панели:**
1. **Requests per second** — `rate(http_requests_total[1m])`
2. **P95 Response Time** — `histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[1m]))`
3. **Requests by Status Code** — `sum by (status) (rate(http_requests_total[5m]))`
4. **RPS by Endpoint** — `sum by (endpoint) (rate(http_requests_total[1m]))`

**Статус:** ✅ Выполнено

---

## 🎯 Итоги урока 1

### Изученные технологии
- ✅ Prometheus (настройка, scrape configs)
- ✅ Grafana (datasources, provisioning, dashboards)
- ✅ Prometheus metrics (Counter, Histogram)
- ✅ FastAPI middleware
- ✅ Docker Compose (multi-file setup)
- ✅ Docker volumes

### Навыки
- ✅ Добавление метрик в Python приложение
- ✅ Настройка Prometheus для сбора метрик
- ✅ Создание дашбордов в Grafana
- ✅ Работа с Docker Compose
- ✅ Hot-reload для разработки

### Текущее состояние системы

```
┌─────────────────────────────────────────────────────────┐
│                   IT Interview Trainer                  │
│                                                         │
│   Backend (FastAPI) ────→ Frontend (React)             │
│        │                         │                      │
│        ↓                         │                      │
│   [Prometheus Metrics]           │                      │
│        │                         │                      │
│        ↓                         │                      │
│   ┌─────────────┐               │                      │
│   │ Prometheus  │ ← scrapes     │                      │
│   │  (9090)     │               │                      │
│   └──────┬──────┘               │                      │
│          │                      │                      │
│          ↓                      │                      │
│   ┌─────────────┐               │                      │
│   │   Grafana   │ ← dashboards  │                      │
│   │   (3001)    │               │                      │
│   └─────────────┘               │                      │
└─────────────────────────────────────────────────────────┘
```

**Порты:**
- Backend: http://localhost:8000
- Frontend: http://localhost:3000
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3001 (admin/admin123)

---

## 📋 Следующий урок: Уровень 2

### Темы для изучения

1. **Node Exporter** — метрики сервера
   - CPU, RAM, диск, сеть
   - Готовые дашборды (ID: 1860)

2. **Alertmanager** — уведомления
   - Настройка правил алертов
   - Уведомления в Telegram
   - Email уведомления

3. **Логирование (Loki + Promtail)**
   - Сбор логов в Grafana
   - LogQL запросы
   - Алерты по логам

4. **Бизнес-метрики**
   - Количество сессий
   - Активные пользователи
   - Ошибки по типам
   - Конверсия

---

## 🔧 Полезные команды

### Перезапуск мониторинга
```bash
docker compose -f docker-compose.monitoring.yml restart
```

### Просмотр логов
```bash
docker compose logs -f prometheus
docker compose logs -f grafana
```

### Проверка targets
```bash
curl "http://localhost:9090/api/v1/targets" | python3 -m json.tool
```

### Проверка метрик
```bash
curl http://localhost:8000/metrics
```

### Prometheus queries
```promql
# RPS
rate(http_requests_total[1m])

# P95 время ответа
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[1m]))

# Запросов по статусам
sum by (status) (rate(http_requests_total[5m]))

# Запросов по endpoint'ам
sum by (endpoint) (rate(http_requests_total[1m]))
```

---

## 📁 Структура файлов мониторинга

```
it_interVI.it-interview-trainer/
├── docker-compose.monitoring.yml    # Prometheus + Grafana
├── monitoring/
│   ├── prometheus/
│   │   └── prometheus.yml           # Конфиг Prometheus
│   └── grafana/
│       ├── provisioning/
│       │   ├── datasources/
│       │   │   └── datasources.yml  # Datasource конфиг
│       │   └── dashboards/
│       │       └── dashboards.yml   # Dashboards provisioning
│       └── dashboards/              # JSON файлы дашбордов
└── backend/app/main.py              # Метрики приложения
```

---

## 🚀 Как продолжить обучение

1. Открой этот файл
2. Прочитай раздел "Следующий урок: Уровень 2"
3. Выбери тему для изучения
4. Начни с первого шага

**Контакт для продолжения:** Скажи "продолжаем обучение с Урока 2" и выбери тему.

---

**Дата последнего обновления:** 16 марта 2026  
**Статус:** Урок 1 завершён ✅
