# IT Interview Trainer — Context for AI Assistant

## Project Overview

**IT Interview Trainer** — это платформа для подготовки к техническим собеседованиям в IT-сфере. Проект представляет собой fullstack-приложение с REST API backend и React frontend.

### Основные возможности
- Вопросы по профессиям: Frontend, Backend, Fullstack, DevOps
- Типы вопросов: Multiple Choice (MCQ) и Ordering (упорядочивание)
- Система сессий с подсчетом результатов
- Админ-панель для управления вопросами
- JWT аутентификация (вход/регистрация)

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

---

## Project Structure

```
it_interVI.it-interview-trainer/
├── backend/
│   ├── app/
│   │   ├── api/           # REST API endpoints (auth, professions, questions, sessions)
│   │   ├── core/          # Конфигурация (pydantic-settings)
│   │   ├── database/      # SQLAlchemy engine, session factory, seed data
│   │   ├── models/        # SQLAlchemy модели (User, Question, Answer, Profession, Session)
│   │   └── main.py        # Точка входа FastAPI
│   ├── requirements.txt
│   ├── requirements-dev.txt
│   └── venv/
├── frontend/
│   ├── src/
│   │   ├── components/    # UI компоненты (admin, layout, questions, ui)
│   │   ├── hooks/         # Custom React hooks
│   │   ├── pages/         # Страницы (Home, Login, Register, Session, Admin, NotFound)
│   │   ├── services/      # API клиенты (axios-based)
│   │   ├── stores/        # Zustand stores (auth, session)
│   │   ├── types/         # TypeScript типы
│   │   ├── utils/         # Утилиты
│   │   ├── App.tsx        # Главный компонент с роутингом
│   │   └── main.tsx       # Точка входа React
│   ├── index.html
│   ├── package.json
│   ├── vite.config.ts
│   └── tailwind.config.js
├── tests/
│   ├── conftest.py        # pytest fixtures (test DB, test client)
│   └── test_api/          # API тесты (auth, questions, sessions)
├── scripts/
│   ├── setup.sh           # Скрипт установки зависимостей
│   ├── run_backend.sh     # Запуск backend
│   └── run_frontend.sh    # Запуск frontend
├── .env.example           # Шаблон переменных окружения
└── README.md
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
```

### Сборка production

```bash
# Frontend build
cd frontend
npm run build
```

---

## API Endpoints

| Endpoint | Метод | Описание |
|----------|-------|----------|
| `/api/register` | POST | Регистрация пользователя |
| `/api/login` | POST | Вход (возвращает JWT) |
| `/api/professions` | GET | Список профессий |
| `/api/questions` | GET | Список вопросов (с фильтрами) |
| `/api/sessions` | GET/POST | Управление сессиями тестирования |

**Swagger UI:** http://localhost:8000/docs

---

## Database Models

- **User** — пользователи (email, hashed_password, is_admin)
- **Profession** — профессии (Frontend, Backend, etc.)
- **Question** — вопросы (text, question_type, difficulty, options, correct_option/correct_order)
- **Answer** — ответы пользователей на вопросы
- **Session** — сессии тестирования (user_id, profession_id, score)

---

## Environment Variables

Скопировать `.env.example` в `.env`:

```bash
DATABASE_URL=sqlite:///./interview_trainer.db
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
DEBUG=true
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

### Frontend
- **Язык:** TypeScript (строгая типизация)
- **Стили:** TailwindCSS utility classes
- **Состояние:** Zustand stores для глобального state
- **Линтинг:** ESLint с TypeScript правилами
  ```bash
  npm run lint
  ```

---

## Key Files Reference

| Файл | Описание |
|------|----------|
| `backend/app/main.py` | FastAPI приложение, регистрация роутеров |
| `backend/app/core/config.py` | Pydantic settings для env variables |
| `backend/app/database/engine.py` | SQLAlchemy engine и session factory |
| `backend/app/database/seed.py` | Seed данные (профессии, вопросы) |
| `frontend/src/stores/authStore.ts` | Zustand store для аутентификации |
| `frontend/src/services/api.ts` | Axios конфигурация и API вызовы |
| `tests/conftest.py` | pytest fixtures для тестирования API |
