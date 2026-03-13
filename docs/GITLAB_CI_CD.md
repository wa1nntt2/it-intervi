# GitLab CI/CD Pipeline Руководство

## Обзор

Проект использует GitLab CI/CD для автоматизации тестирования, сборки Docker образов и деплоя приложения IT Interview Trainer.

## Структура pipeline

Pipeline состоит из 4 стадий:

```
test → build → security → deploy
```

### 1. Stage: test
- **backend-tests** — запуск pytest тестов и flake8 линтера
- **frontend-tests** — ESLint, TypeScript проверка и сборка

### 2. Stage: build
- **docker-build-backend** — сборка и push Docker образа backend
- **docker-build-frontend** — сборка и push Docker образа frontend

### 3. Stage: security
- **security-scan-python** — проверка зависимостей на уязвимости (safety, bandit)
- **security-scan-frontend** — аудит npm зависимостей

### 4. Stage: deploy
- **deploy-staging** — ручной деплой на staging (только main branch)
- **deploy-production** — ручной деплой на production (только теги)

## Настройка в GitLab

### 1. GitLab Registry настройка

В настройках проекта (`Settings → CI/CD → General pipelines`):
- Убедитесь, что GitLab Container Registry включен

### 2. Переменные окружения

Добавьте следующие переменные в `Settings → CI/CD → Variables`:

| Переменная | Значение | Защищенная | Masked |
|------------|----------|-----------|--------|
| `SECRET_KEY` | Сгенерируйте: `openssl rand -hex 32` | ✅ | ✅ |
| `CORS_ORIGINS` | `http://localhost:3000,http://your-domain.com` | ❌ | ❌ |
| `VITE_API_URL` | URL backend API (например, `http://localhost:8000`) | ❌ | ❌ |

**Для production деплоя дополнительно:**
- Добавьте переменные для подключения к вашему серверу (SSH ключи, домен и т.д.)

### 3. GitLab Runners

Pipeline требует Docker runner. Варианты:

#### Использовать GitLab Shared Runners
- Включены по умолчанию
- Просто убедитесь, что в `.gitlab-ci.yml` указан тег `docker`

#### Настроить свой runner
```bash
# Установка GitLab Runner
sudo apt-get install gitlab-runner

# Регистрация runner
sudo gitlab-runner register
# Следуйте инструкциям, укажите docker executor
```

## Запуск pipeline

### Автоматический запуск
Pipeline запускается автоматически при:
- Push в ветки `main` или `develop`
- Создании merge request

### Ручной запуск деплоя
- Перейдите в `CI/CD → Pipelines`
- Найдите нужный pipeline
- Нажмите кнопку Play на стадии deploy

## Деплой на production

Для деплоя на production создайте тег:

```bash
git tag -a v0.1.0 -m "Release version 0.1.0"
git push origin v0.1.0
```

После push тега:
1. Запустится pipeline с production деплоем
2. В GitLab UI нажмите кнопку для ручного запуска деплоя

## Кэширование

Pipeline использует кэширование для ускорения:
- Python пакеты (`.pip-cache/`)
- npm пакеты (`.npm-cache/`)
- Python virtualenv (`backend/venv/`)
- Node modules (`frontend/node_modules/`)

## Артефакты

После выполнения pipeline доступны:
- **Отчет о покрытии тестами** — `backend/htmlcov/`
- **Cobertura report** — `backend/coverage.xml`
- **Сборка frontend** — `frontend/dist/`
- **Security reports** — `bandit-report.json`, `npm-audit-report.json`

## Troubleshooting

### Ошибка: "docker command not found"
Убедитесь, что runner использует docker executor:
```toml
# /etc/gitlab-runner/config.toml
[[runners]]
  executor = "docker"
```

### Ошибка: "unauthorized: authentication required"
Проверьте переменные CI_REGISTRY_USER и CI_REGISTRY_PASSWORD:
- Они должны быть автоматически установлены GitLab
- Убедитесь, что у вашего пользователя есть доступ к registry

### Ошибка: "SECRET_KEY не установлен"
Добавьте переменную SECRET_KEY в настройках GitLab CI/CD Variables

### Docker образы не пушатся
Проверьте:
- GitLab Registry включен в настройках проекта
- У runner есть права на запись в registry
- Переменные DOCKER_TLS_CERTDIR корректно установлены

## Кастомизация

### Изменение порта frontend
Отредактируйте `docker-compose.staging.yml`:
```yaml
frontend:
  ports:
    - "80:80"  # Измените на нужный порт
```

### Добавление email уведомлений
```yaml
# В конце .gitlab-ci.yml
workflow:
  rules:
    - when: always

notify:
  email:
    to:
      - admin@example.com
    on_failure: always
    on_success: change
```

### Параллельный запуск тестов
Для ускорения можно разделить тесты:
```yaml
backend-tests-unit:
  script: pytest tests/unit/

backend-tests-integration:
  script: pytest tests/integration/
```

## Ссылки

- [GitLab CI/CD Documentation](https://docs.gitlab.com/ee/ci/)
- [GitLab Container Registry](https://docs.gitlab.com/ee/user/packages/container_registry/)
- [GitLab Runners](https://docs.gitlab.com/runner/)
