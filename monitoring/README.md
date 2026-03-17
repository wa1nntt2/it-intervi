# Мониторинг IT Interview Trainer

## Обзор

Система мониторинга проекта IT Interview Trainer включает:

- **Prometheus** - сбор и хранение метрик
- **Grafana** - визуализация метрик и дашборды
- **Loki** - агрегация логов
- **Promtail** - сбор и отправка логов в Loki

## Компоненты

| Сервис | Порт | Описание |
|--------|------|----------|
| **Grafana** | http://localhost:3002 | Визуализация и дашборды |
| **Prometheus** | http://localhost:9090 | Сбор метрик |
| **Loki** | http://localhost:3100 | Агрегация логов |
| **Promtail** | 9080 (внутренний) | Сбор логов |

## Доступы Grafana

- **Логин:** `admin`
- **Пароль:** `admin123`

## Дашборды

### 1. IT Interview - Backend Overview
**UID:** `backend-overview`

Мониторинг backend приложения:
- Статус backend сервиса
- Requests per Second (RPS)
- API Latency (p50, p95, p99)
- Error Rate
- HTTP Requests по методам (GET, POST, PUT, DELETE)
- HTTP Status Codes по endpoint'ам
- Memory Usage (Heap)
- Goroutines & File Descriptors
- Application Errors (логи)

### 2. IT Interview - Infrastructure
**UID:** `infrastructure`

Мониторинг инфраструктуры:
- Статус всех сервисов (Prometheus, Loki, Promtail, Backend)
- TSDB Samples & Time Series
- Loki Request Rate
- Promtail Sent Entries Rate
- Promtail Push Errors
- Loki Memory Chunks
- Promtail Request Latency
- Prometheus TSDB Stats
- Memory Usage by Service

### 3. Loki & Promtail Monitoring
**UID:** `loki-monitoring`

Детальный мониторинг Loki и Promtail:
- Loki Status
- Promtail Status
- Loki Request Rate
- Loki Memory Chunks
- Promtail Sent Entries Rate
- Promtail Push Errors
- Container Logs

## Метрики Backend

Backend приложение экспортирует следующие метрики:

### HTTP метрики

```prometheus
# Общее количество HTTP запросов
http_requests_total{method, endpoint, status}

# Длительность HTTP запросов
http_request_duration_seconds{method, endpoint}
```

### Go Runtime метрики

```prometheus
# Количество горутин
go_goroutines

# Использование памяти
go_memory_classes_heap_objects_bytes
go_memory_classes_heap_free_bytes

# GC метрики
go_gc_duration_seconds
go_gc_heap_objects_objects
```

## Логи

Логи собираются со всех Docker контейнеров и доступны в Grafana через Loki.

### Поиск логов в Grafana

Примеры LogQL запросов:

```logql
# Все логи backend контейнера
{job="containerlogs"} |= "it-interview-backend"

# Только ошибки
{job="containerlogs"} |= "ERROR" or |= "error"

# Логи по конкретному контейнеру
{container_name="it-interview-backend"}

# Логи за последний час с фильтром по тексту
{job="containerlogs"} |= "login" | line_format "{{.output}}"
```

## Алерты

### Настройка алертов в Grafana

1. Откройте дашборд
2. Нажмите на панель → ⋮ → Edit
3. Перейдите на вкладку "Alert"
4. Создайте правило алерта

### Примеры алертов

| Алерт | Условие | Критичность |
|-------|---------|-------------|
| Backend Down | `up{job="backend"} == 0` | Critical |
| High Error Rate | `error_rate > 5%` | Warning |
| High Latency | `p95_latency > 1s` | Warning |
| Loki Down | `up{job="loki"} == 0` | Critical |
| Promtail Errors | `rate(promtail_push_errors_total[5m]) > 10` | Warning |

## Запуск мониторинга

```bash
# Запуск Loki и Promtail
docker-compose -f docker-compose.loki.yml up -d

# Запуск Prometheus и Grafana
docker-compose -f docker-compose.monitoring.yml up -d

# Просмотр логов
docker-compose -f docker-compose.loki.yml logs -f
docker-compose -f docker-compose.monitoring.yml logs -f

# Остановка
docker-compose -f docker-compose.loki.yml down
docker-compose -f docker-compose.monitoring.yml down
```

## Конфигурация

### Prometheus

Файл конфигурации: `monitoring/prometheus/prometheus.yml`

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
  
  - job_name: 'loki'
    static_configs:
      - targets: ['loki:3100']
  
  - job_name: 'promtail'
    static_configs:
      - targets: ['promtail:9080']
```

### Grafana Datasources

Автоматически настраиваются через provisioning:

- **Prometheus**: `http://prometheus:9090`
- **Loki**: `http://loki:3100`

### Loki

Файл конфигурации: `monitoring/loki/loki-config.yml`

### Promtail

Файл конфигурации: `monitoring/promtail/promtail-config.yml`

## Добавление новых метрик

### В Backend (FastAPI)

```python
from prometheus_client import Counter, Histogram, Gauge

# Счётчик
MY_COUNTER = Counter(
    'my_metric_total',
    'Description of metric',
    ['label1', 'label2']
)

# Гистограмма
MY_HISTOGRAM = Histogram(
    'my_metric_duration_seconds',
    'Description',
    ['method']
)

# Gauge
MY_GAUGE = Gauge(
    'my_metric_gauge',
    'Description',
    ['type']
)

# Использование
MY_COUNTER.labels(label1='value1', label2='value2').inc()

@MY_HISTOGRAM.time()
def my_function():
    pass
```

### Endpoint для метрик

В backend уже настроен endpoint `/metrics`:

```python
from prometheus_client import generate_latest, CONTENT_TYPE

@app.get("/metrics")
async def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE)
```

## Troubleshooting

### Prometheus не собирает метрики

```bash
# Проверка targets
curl http://localhost:9090/api/v1/targets

# Проверка доступности backend
curl http://localhost:8000/metrics
```

### Loki не принимает логи

```bash
# Проверка статуса Loki
curl http://localhost:3100/ready

# Проверка логов Loki
docker logs loki

# Проверка логов Promtail
docker logs promtail
```

### Grafana не показывает данные

1. Проверьте datasource (Configuration → Data sources)
2. Проверьте запрос в Explore
3. Проверьте временной диапазон

## Полезные ссылки

- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [Loki Documentation](https://grafana.com/docs/loki/)
- [PromQL Cheat Sheet](https://promlabs.com/promql-cheat-sheet/)
- [LogQL Documentation](https://grafana.com/docs/loki/latest/logql/)
