# IT Interview Trainer — Context for AI Assistant

## Project Overview

**IT Interview Trainer** — это платформа для подготовки к техническим собеседованиям в IT-сфере. Проект представляет собой fullstack-приложение с REST API backend и React frontend.

### Основные возможности
- Вопросы по профессиям: Frontend, Backend, Fullstack, DevOps
- Типы вопросов: Multiple Choice (MCQ) и Ordering (упорядочивание с drag-and-drop)
- Система сессий с подсчетом результатов и историей
- Админ-панель для управления вопросами, пользователями и сессиями
- JWT аутентификация (access + refresh токены)
- Интервью-режимы: practice, learning, timed, exam
- Прогресс пользователя и статистика
- Rate limiting для защиты API

---

## Tech Stack

### Backend
| Технология | Назначение |
|------------|------------|
| **FastAPI** | Веб-фреймворк |
| **SQLAlchemy** | ORM |
| **SQLite** | База данных |
| **Pydantic** | Валидация данных |
| **python-jose** | JWT токены |
| **passlib + bcrypt** | Хеширование паролей |
| **Alembic** | Миграции БД |
| **SlowAPI** | Rate limiting |
| **fastapi-csrf-protect** | CSRF защита |

### Frontend
| Технология | Назначение |
|------------|------------|
| **React 18** | UI библиотека |
| **TypeScript** | Типизация |
| **Vite** | Сборщик |
| **TailwindCSS** | Стилизация |
| **Zustand** | State management |
| **React Router** | Маршрутизация |
| **Axios** | HTTP клиент |
| **@dnd-kit** | Drag-and-drop (ordering вопросы) |
| **React Hook Form** | Управление формами |
| **Zod** | Валидация форм |
| **canvas-confetti** | Эффекты庆祝 |

---

## Project Structure

```
it_interVI.it-interview-trainer/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── auth.py           # Аутентификация (login, register, refresh)
│   │   │   ├── professions.py    # CRUD профессий
│   │   │   ├── questions.py      # CRUD вопросов
│   │   │   ├── sessions.py       # Управление сессиями
│   │   │   ├── users.py          # Управление пользователями (admin)
│   │   │   ├── progress.py       # Прогресс и статистика
│   │   │   ├── interviews.py     # Интервью режимы
│   │   │   ├── schemas.py        # Pydantic схемы
│   │   │   └── deps.py           # Зависимости (auth, db session)
│   │   ├── core/
│   │   │   ├── config.py         # Pydantic settings
│   │   │   ├── security.py       # JWT, password hashing
│   │   │   ├── limiter.py        # Rate limiter конфигурация
│   │   │   └── cache.py          # Кэширование
│   │   ├── database/
│   │   │   ├── engine.py         # SQLAlchemy engine
│   │   │   └── seed.py           # Seed данные
│   │   ├── models/
│   │   │   ├── user.py           # User модель
│   │   │   ├── profession.py     # Profession модель
│   │   │   ├── question.py       # Question модель
│   │   │   ├── answer.py         # Answer модель
│   │   │   ├── session.py        # Session модель
│   │   │   ├── category.py       # Category модель (теги вопросов)
│   │   │   ├── ordering_item.py  # OrderingItem модель
│   │   │   ├── interview_config.py # InterviewConfig модель
│   │   │   └── user_progress.py  # UserProgress модель
│   │   └── main.py               # Точка входа FastAPI
│   ├── alembic/
│   │   ├── versions/             # Файлы миграций
│   │   └── env.py                # Alembic конфигурация
│   ├── data/                     # SQLite файлы
│   ├── scripts/                  # Скрипты для БД
│   ├── venv/                     # Python venv
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── requirements-dev.txt
│   ├── alembic.ini
│   └── pytest.ini
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── admin/            # Админ-панель компоненты
│   │   │   ├── layout/           # Layout (Header, Footer, Sidebar)
│   │   │   ├── questions/        # Вопрос компоненты (MCQ, Ordering)
│   │   │   └── ui/               # Базовые UI компоненты
│   │   ├── hooks/                # Custom React hooks
│   │   ├── pages/
│   │   │   ├── Home.tsx          # Главная
│   │   │   ├── Login.tsx         # Вход
│   │   │   ├── Register.tsx      # Регистрация
│   │   │   ├── Session.tsx       # Прохождение сессии
│   │   │   ├── SessionNew.tsx    # Новая сессия
│   │   │   ├── InterviewSetup.tsx # Настройка интервью
│   │   │   ├── Profile.tsx       # Профиль
│   │   │   ├── ProfileEnhanced.tsx # Расширенный профиль
│   │   │   ├── Admin.tsx         # Админ-панель
│   │   │   ├── AdminSessions.tsx # Админ: сессии
│   │   │   ├── AdminUsers.tsx    # Админ: пользователи
│   │   │   └── NotFound.tsx      # 404
│   │   ├── services/
│   │   │   └── api.ts            # Axios инстанс
│   │   ├── stores/
│   │   │   ├── authStore.ts      # Auth Zustand store
│   │   │   └── sessionStore.ts   # Session Zustand store
│   │   ├── types/                # TypeScript типы
│   │   ├── utils/                # Утилиты
│   │   ├── data/                 # Статические данные
│   │   ├── App.tsx               # Главный компонент
│   │   ├── main.tsx              # Точка входа
│   │   └── index.css             # Глобальные стили
│   ├── index.html
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   ├── tsconfig.json
│   ├── Dockerfile
│   └── nginx.conf
├── tests/
│   ├── conftest.py               # pytest fixtures
│   └── test_api/
│       ├── test_auth.py
│       ├── test_questions.py
│       └── test_sessions.py
├── scripts/
│   ├── setup.sh                  # Установка зависимостей
│   ├── run_backend.sh            # Запуск backend
│   ├── run_frontend.sh           # Запуск frontend
│   ├── backup_db.sh              # Бэкап БД
│   ├── generate-secret-key.sh    # Генерация SECRET_KEY
│   ├── export_questions.py       # Экспорт вопросов
│   ├── import_questions_from_json.py # Импорт вопросов
│   └── import_devops_markdown.py # Импорт DevOps вопросов
├── backups/                      # Бэкапы вопросов
├── docker-compose.yml            # Docker Compose (prod)
├── docker-compose.staging.yml    # Docker Compose (staging)
├── .env.example                  # Шаблон env переменных
├── .env.production               # Production env
├── .gitlab-ci.yml                # GitLab CI/CD pipeline
└── QWEN.md                       # Этот файл
```

---

## Building and Running

### Установка зависимостей

```bash
# Быстрая установка (все зависимости)
./scripts/setup.sh

# Или вручную:
# Backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Frontend
cd frontend
npm install
```

### Запуск приложения

#### Docker (рекомендуется)

```bash
# Запуск всех сервисов
docker-compose up -d

# Backend: http://localhost:8000
# Frontend: http://localhost:3000
# Swagger UI: http://localhost:8000/docs

# Просмотр логов
docker-compose logs -f backend
docker-compose logs -f frontend

# Остановка
docker-compose down
```

#### Локальный запуск

```bash
# Backend (порт 8000)
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Frontend (порт 3000, Vite dev server)
cd frontend
npm run dev
```

### Тесты

```bash
cd backend
source venv/bin/activate
pytest

# С покрытием
pytest --cov=app --cov-report=html

# Конкретные тесты
pytest tests/test_api/test_auth.py -v
```

### Миграции БД

```bash
cd backend
source venv/bin/activate

# Применить миграции
alembic upgrade head

# Создать новую миграцию
alembic revision --autogenerate -m "Description"

# Откатить миграцию
alembic downgrade -1
```

### Сборка production

```bash
# Frontend build
cd frontend
npm run build
# Результат в dist/
```

---

## API Endpoints

### Аутентификация

| Endpoint | Метод | Описание |
|----------|-------|----------|
| `/api/register` | POST | Регистрация пользователя |
| `/api/login` | POST | Вход (возвращает JWT) |
| `/api/refresh` | POST | Обновление access токена |

### Профессии

| Endpoint | Метод | Описание |
|----------|-------|----------|
| `/api/professions` | GET | Список профессий (пагинированный) |
| `/api/professions/{id}` | GET | Профессия по ID |
| `/api/professions` | POST | Создать профессию (admin) |
| `/api/professions/{id}` | PUT | Обновить профессию (admin) |
| `/api/professions/{id}` | DELETE | Удалить профессию (admin) |

### Вопросы

| Endpoint | Метод | Описание |
|----------|-------|----------|
| `/api/questions` | GET | Список вопросов (с фильтрами, пагинация) |
| `/api/questions/{id}` | GET | Вопрос по ID |
| `/api/questions` | POST | Создать вопрос (admin) |
| `/api/questions/{id}` | PUT | Обновить вопрос (admin) |
| `/api/questions/{id}` | DELETE | Удалить вопрос (admin) |
| `/api/questions/{id}/duplicate` | POST | Дублировать вопрос (admin) |
| `/api/questions/import` | POST | Импорт вопросов (admin) |
| `/api/questions/export` | GET | Экспорт вопросов (admin) |

**Параметры фильтрации для GET `/api/questions`:**
- `profession_id` — фильтр по профессии
- `question_type` — тип вопроса (mcq, ordering)
- `difficulty` — уровень (intern, junior, middle)
- `category_id` — фильтр по категории
- `limit`, `offset` — пагинация

### Сессии

| Endpoint | Метод | Описание |
|----------|-------|----------|
| `/api/sessions` | GET | История сессий пользователя |
| `/api/sessions` | POST | Создать новую сессию |
| `/api/sessions/{id}` | GET | Детали сессии |
| `/api/sessions/{id}/complete` | PUT | Завершить сессию |

### Пользователи (Admin)

| Endpoint | Метод | Описание |
|----------|-------|----------|
| `/api/users` | GET | Список пользователей |
| `/api/users/{id}` | GET | Пользователь по ID |
| `/api/users/{id}` | PUT | Обновить пользователя |
| `/api/users/{id}` | DELETE | Удалить пользователя |

### Прогресс

| Endpoint | Метод | Описание |
|----------|-------|----------|
| `/api/progress` | GET | Прогресс пользователя |
| `/api/progress/stats` | GET | Статистика по профессиям |

### Интервью

| Endpoint | Метод | Описание |
|----------|-------|----------|
| `/api/interviews` | POST | Создать интервью сессию |
| `/api/interviews/config` | GET | Конфигурация интервью |

**Swagger UI:** http://localhost:8000/docs

---

## Database Models

| Модель | Описание |
|--------|----------|
| **User** | Пользователи (email, hashed_password, is_admin, created_at) |
| **Profession** | Профессии (Frontend, Backend, DevOps, Fullstack) |
| **Question** | Вопросы (text, question_type, difficulty, options, correct_option, correct_order, explanation) |
| **Category** | Категории/теги вопросов (многие-ко-многим с Question) |
| **Answer** | Ответы пользователей (session_id, question_id, selected_option, is_correct) |
| **Session** | Сессии тестирования (user_id, profession_id, question_ids, score, status, mode, time_limit) |
| **OrderingItem** | Элементы для ordering вопросов |
| **InterviewConfig** | Конфигурация интервью режимов |
| **UserProgress** | Прогресс пользователя по профессиям |

---

## Environment Variables

### Минимальный набор (.env)

```bash
# Database
DATABASE_URL=sqlite:///./interview_trainer.db

# Security - ОБЯЗАТЕЛЬНО измените в production!
SECRET_KEY=your-secret-key-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
CORS_ALLOW_CREDENTIALS=true

# Rate limiting
RATE_LIMIT_PER_MINUTE=10

# Debug
DEBUG=true

# Pagination
DEFAULT_PAGE_SIZE=20
MAX_PAGE_SIZE=100

# Sessions
QUESTIONS_PER_SESSION=20
MIN_QUESTIONS_IN_SESSION=5

# Cache
CACHE_CAPACITY=100
```

### Генерация SECRET_KEY

```bash
./scripts/generate-secret-key.sh
# или
openssl rand -hex 32
```

---

## Test Credentials

После первого запуска backend создается тестовый пользователь:

- **Email:** admin@example.com
- **Пароль:** admin123

---

## Development Conventions

### Backend
- **Стиль:** PEP 8, type hints
- **Импорты:** относительные внутри пакета `app`
- **API response:** Pydantic схемы в `api/schemas.py`
- **Тесты:** pytest с fixtures для изоляции БД
- **Линтинг:** flake8
  ```bash
  flake8 app --count --select=E9,F63,F7,F82 --show-source --statistics
  ```

### Frontend
- **Язык:** TypeScript (строгая типизация)
- **Стили:** TailwindCSS utility classes
- **Состояние:** Zustand stores для глобального state
- **Формы:** React Hook Form + Zod валидация
- **Линтинг:** ESLint с TypeScript правилами
  ```bash
  npm run lint
  ```

---

## Key Files Reference

| Файл | Описание |
|------|----------|
| `backend/app/main.py` | FastAPI приложение, middleware, регистрация роутеров |
| `backend/app/core/config.py` | Pydantic settings для env variables |
| `backend/app/core/security.py` | JWT, password hashing утилиты |
| `backend/app/core/limiter.py` | Rate limiter конфигурация |
| `backend/app/database/engine.py` | SQLAlchemy engine и session factory |
| `backend/app/database/seed.py` | Seed данные (профессии, вопросы, admin) |
| `backend/app/api/schemas.py` | Pydantic схемы для API |
| `backend/app/api/deps.py` | Зависимости (auth, db session) |
| `backend/alembic/versions/` | Файлы миграций БД |
| `frontend/src/stores/authStore.ts` | Zustand store для аутентификации |
| `frontend/src/stores/sessionStore.ts` | Zustand store для сессии |
| `frontend/src/services/api.ts` | Axios конфигурация и API вызовы |
| `frontend/src/components/questions/` | Компоненты вопросов (MCQ, Ordering) |
| `tests/conftest.py` | pytest fixtures для тестирования |
| `docker-compose.yml` | Docker Compose конфигурация |
| `.gitlab-ci.yml` | GitLab CI/CD pipeline |

---

## Docker & CI/CD

### Docker Compose

```bash
# Запуск
docker-compose up -d

# Production (с другими переменными окружения)
docker-compose -f docker-compose.yml --env-file .env.production up -d

# Staging
docker-compose -f docker-compose.staging.yml up -d

# Пересборка
docker-compose build --no-cache

# Логи
docker-compose logs -f backend
docker-compose logs -f frontend
```

### GitLab CI/CD Pipeline

| Stage | Jobs | Описание |
|-------|------|----------|
| **test** | backend-tests, frontend-tests | pytest, flake8, ESLint, tsc, build |
| **build** | docker-build-backend, docker-build-frontend | Kaniko build образов |
| **security** | security-scan-python, security-scan-frontend | safety, bandit, npm audit |
| **deploy** | deploy-staging, deploy-production | Deploy на staging/prod |

**Триггеры:**
- `main`, `develop`, `release/*` → build образов
- `main`, `develop` → deploy на staging (manual)
- Теги → deploy на production (manual)

---

## Scripts Reference

| Скрипт | Описание |
|--------|----------|
| `./scripts/setup.sh` | Автоматическая установка всех зависимостей |
| `./scripts/run_backend.sh` | Запуск backend сервера |
| `./scripts/run_frontend.sh` | Запуск frontend dev сервера |
| `./scripts/backup_db.sh` | Бэкап SQLite базы данных |
| `./scripts/generate-secret-key.sh` | Генерация случайного SECRET_KEY |
| `./scripts/export_questions.py` | Экспорт вопросов в JSON |
| `./scripts/import_questions_from_json.py` | Импорт вопросов из JSON |
| `./scripts/import_devops_markdown.py` | Импорт DevOps вопросов из Markdown |
| `./scripts/bind_questions_to_categories.py` | Привязка вопросов к категориям |

---

## Troubleshooting

### Backend не запускается

```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

### Frontend не запускается

```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### Ошибки миграций

```bash
cd backend
source venv/bin/activate
alembic downgrade -1
alembic upgrade head
```

### Ошибки базы данных

```bash
# Удалить старую БД и пересоздать
cd backend
rm data/interview_trainer.db
# Перезапустить backend для seed
```

### Docker проблемы

```bash
# Очистить и пересобрать
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

---

## Production Notes

### Рекомендации

1. **Измените SECRET_KEY** в `.env.production`
2. **Используйте PostgreSQL** вместо SQLite для production
3. **Настройте HTTPS** через reverse proxy (nginx, traefik)
4. **Включите rate limiting** (по умолчанию 10 запросов/минуту)
5. **Настройте CORS_ORIGINS** под ваш домен

### Environment для production

```bash
# .env.production
DATABASE_URL=postgresql://user:password@localhost:5432/interview_trainer
SECRET_KEY=<сгенерируйте случайный ключ>
DEBUG=false
CORS_ORIGINS=https://yourdomain.com
RATE_LIMIT_PER_MINUTE=10
```

### Deploy

```bash
docker-compose -f docker-compose.yml --env-file .env.production up -d
```

---

## Improvement Ideas

См. файлы для идей по улучшению:
- `IMPROVEMENTS.md` — общие улучшения
- `SECURITY_IMPROVEMENTS.md` — улучшения безопасности
- `PRODUCTION_READY.md` — production готовность
- `BACKUP_INSTRUCTIONS.md` — инструкции бэкапа
- `SIMPLE_DATA_MANAGEMENT.md` — управление данными
