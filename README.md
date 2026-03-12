# 💼 IT Interview Trainer

**Платформа для подготовки к техническим собеседованиям в IT-сфере**

Современное fullstack-приложение, которое поможет вам эффективно подготовиться к техническим интервью в ведущих IT-компаниях.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-green.svg)
![Node](https://img.shields.io/badge/node-16+-green.svg)
![React](https://img.shields.io/badge/react-18-blue.svg)

---

## 📋 О проекте

IT Interview Trainer — это интерактивная платформа для отработки навыков прохождения технических собеседований. Проект охватывает ключевые направления в IT и предоставляет разнообразные типы вопросов для комплексной подготовки.

### 🎯 Ключевые возможности

| Возможность | Описание |
|-------------|----------|
| 📚 **Профессии** | Вопросы по направлениям: Frontend, Backend, Fullstack, DevOps |
| ❓ **Типы вопросов** | Multiple Choice (выбор ответа) и Ordering (упорядочивание) |
| 📊 **Сессии** | Прохождение тестов с сохранением истории и подсчетом результатов |
| 🔐 **Аутентификация** | JWT-токены с refresh/access токенами |
| 🛠 **Админ-панель** | CRUD-операции для управления вопросами и профессиями |
| 📱 **Адаптивный UI** | Современный интерфейс с TailwindCSS |

---

## 🏗 Архитектура проекта

```
it_interVI.it-interview-trainer/
├── backend/                    # FastAPI REST API
│   ├── app/
│   │   ├── api/               # API endpoints (auth, professions, questions, sessions)
│   │   │   ├── auth.py        # Регистрация, логин, refresh токена
│   │   │   ├── professions.py # CRUD профессий
│   │   │   ├── questions.py   # CRUD вопросов
│   │   │   └── sessions.py    # Управление сессиями
│   │   ├── core/              # Ядро приложения
│   │   │   ├── config.py      # Pydantic settings (env variables)
│   │   │   ├── security.py    # JWT, password hashing
│   │   │   └── cache.py       # Кэширование данных
│   │   ├── database/          # Работа с БД
│   │   │   ├── engine.py      # SQLAlchemy engine & session factory
│   │   │   └── seed.py        # Seed данные для разработки
│   │   ├── models/            # SQLAlchemy модели
│   │   │   ├── user.py        # User модель
│   │   │   ├── profession.py  # Profession модель
│   │   │   ├── question.py    # Question модель
│   │   │   ├── answer.py      # Answer модель
│   │   │   └── session.py     # Session модель
│   │   └── main.py            # Точка входа FastAPI
│   ├── data/                  # SQLite database файлы
│   ├── venv/                  # Python virtual environment
│   ├── Dockerfile             # Docker образ backend
│   └── requirements*.txt      # Python зависимости
│
├── frontend/                   # React + TypeScript SPA
│   ├── src/
│   │   ├── components/        # Переиспользуемые UI компоненты
│   │   │   ├── admin/         # Админ-панель компоненты
│   │   │   ├── layout/        # Layout компоненты (Header, Footer)
│   │   │   ├── questions/     # Компоненты вопросов
│   │   │   └── ui/            # Базовые UI элементы
│   │   ├── hooks/             # Custom React hooks
│   │   ├── pages/             # Страницы приложения
│   │   │   ├── Home.tsx       # Главная страница
│   │   │   ├── Login.tsx      # Страница входа
│   │   │   ├── Register.tsx   # Страница регистрации
│   │   │   ├── Session.tsx    # Страница прохождения теста
│   │   │   ├── Admin.tsx      # Админ-панель
│   │   │   └── NotFound.tsx   # 404 страница
│   │   ├── services/          # API клиенты (axios-based)
│   │   │   └── api.ts         # Настроенный axios инстанс
│   │   ├── stores/            # Zustand stores
│   │   │   ├── authStore.ts   # Состояние аутентификации
│   │   │   └── sessionStore.ts# Состояние сессии
│   │   ├── types/             # TypeScript типы и интерфейсы
│   │   ├── utils/             # Утилитные функции
│   │   ├── App.tsx            # Главный компонент с роутингом
│   │   └── main.tsx           # Точка входа React
│   ├── index.html             # HTML шаблон
│   ├── package.json           # Node зависимости
│   ├── vite.config.ts         # Vite конфигурация
│   ├── tailwind.config.js     # TailwindCSS конфигурация
│   ├── tsconfig.json          # TypeScript конфигурация
│   └── Dockerfile             # Docker образ frontend
│
├── tests/                      # pytest тесты
│   ├── conftest.py            # Fixtures (test DB, test client)
│   └── test_api/              # API endpoint тесты
│       ├── test_auth.py       # Тесты аутентификации
│       ├── test_questions.py  # Тесты вопросов
│       └── test_sessions.py   # Тесты сессий
│
├── scripts/                    # Helper скрипты
│   ├── setup.sh               # Установка всех зависимостей
│   ├── run_backend.sh         # Запуск backend
│   └── run_frontend.sh        # Запуск frontend
│
├── docker-compose.yml          # Docker Compose конфигурация
├── .env.example                # Шаблон переменных окружения
├── .gitignore                  # Git ignore правила
└── QWEN.md                     # Документация проекта
```

---

## 🚀 Быстрый старт

### Вариант 1: Docker (рекомендуется)

```bash
# Запуск всех сервисов
docker-compose up -d

# Backend: http://localhost:8000
# Frontend: http://localhost:3000
# Swagger UI: http://localhost:8000/docs
```

### Вариант 2: Локальная установка

#### 1. Установка всех зависимостей

```bash
./scripts/setup.sh
```

#### 2. Ручная установка

**Backend:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

---

## 🏃 Запуск приложения

### Backend

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

| Endpoint | Описание |
|----------|----------|
| http://localhost:8000 | API сервер |
| http://localhost:8000/docs | Swagger UI (интерактивная документация) |
| http://localhost:8000/redoc | ReDoc документация |

### Frontend

```bash
cd frontend
npm run dev
```

| Endpoint | Описание |
|----------|----------|
| http://localhost:3000 | Приложение |
| http://localhost:3000/login | Страница входа |
| http://localhost:3000/register | Страница регистрации |
| http://localhost:3000/admin | Админ-панель (требуются права администратора) |

---

## 📡 API Endpoints

### Аутентификация

| Метод | Endpoint | Описание |
|-------|----------|----------|
| POST | `/api/register` | Регистрация нового пользователя |
| POST | `/api/login` | Вход (возвращает access + refresh токены) |
| POST | `/api/refresh` | Обновление access токена |

### Профессии

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/api/professions` | Получить список всех профессий |
| GET | `/api/professions/{id}` | Получить профессию по ID |
| POST | `/api/professions` | Создать профессию (admin only) |
| PUT | `/api/professions/{id}` | Обновить профессию (admin only) |
| DELETE | `/api/professions/{id}` | Удалить профессию (admin only) |

### Вопросы

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/api/questions` | Получить вопросы (с фильтрами) |
| GET | `/api/questions/{id}` | Получить вопрос по ID |
| POST | `/api/questions` | Создать вопрос (admin only) |
| PUT | `/api/questions/{id}` | Обновить вопрос (admin only) |
| DELETE | `/api/questions/{id}` | Удалить вопрос (admin only) |

**Параметры фильтрации для GET `/api/questions`:**
- `profession_id` — фильтр по профессии
- `question_type` — тип вопроса (mcq, ordering)
- `difficulty` — уровень сложности
- `limit` — количество вопросов
- `offset` — смещение для пагинации

### Сессии

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/api/sessions` | Получить историю сессий пользователя |
| POST | `/api/sessions` | Создать новую сессию |
| GET | `/api/sessions/{id}` | Получить детали сессии |
| PUT | `/api/sessions/{id}/complete` | Завершить сессию с результатом |

---

## 🗃 Модель данных

### User (Пользователи)
```python
id: int              # Первичный ключ
email: str           # Уникальный email
hashed_password: str # Хешированный пароль
is_admin: bool       # Флаг администратора
```

### Profession (Профессии)
```python
id: int       # Первичный ключ
name: str     # Название (Frontend, Backend, etc.)
description: str  # Описание
```

### Question (Вопросы)
```python
id: int            # Первичный ключ
profession_id: int # Внешний ключ на Profession
text: str          # Текст вопроса
question_type: str # "mcq" или "ordering"
difficulty: str    # "easy", "medium", "hard"
options: list      # Варианты ответов
correct_option: int  # Для MCQ - индекс правильного ответа
correct_order: list  # Для Ordering - правильный порядок
```

### Session (Сессии тестирования)
```python
id: int         # Первичный ключ
user_id: int    # Внешний ключ на User
profession_id: int  # Внешний ключ на Profession
score: int      # Количество правильных ответов
total: int      # Общее количество вопросов
completed: bool # Статус завершения
created_at: datetime  # Дата создания
```

### Answer (Ответы)
```python
id: int         # Первичный ключ
session_id: int # Внешний ключ на Session
question_id: int  # Внешний ключ на Question
user_answer: any  # Ответ пользователя
is_correct: bool  # Правильность ответа
```

---

## 🧪 Тестирование

### Запуск всех тестов

```bash
cd backend
source venv/bin/activate
pytest
```

### Запуск с покрытием

```bash
pytest --cov=app --cov-report=html
```

### Запуск конкретных тестов

```bash
# Тесты аутентификации
pytest tests/test_api/test_auth.py

# Тесты вопросов
pytest tests/test_api/test_questions.py -v

# Тесты с фильтрацией по имени
pytest -k "test_login"
```

---

## 🔐 Безопасность

### JWT Токены

Приложение использует двухтокенную систему:

| Токен | Время жизни | Назначение |
|-------|-------------|------------|
| Access Token | 30 минут | Доступ к защищенным endpoint'ам |
| Refresh Token | 7 дней | Обновление access токена |

### Хеширование паролей

Пароли хешируются с помощью **bcrypt** (через passlib) перед сохранением в базу данных.

### Защищенные endpoint'ы

Следующие endpoint'ы требуют JWT аутентификации:
- Создание/обновление/удаление вопросов
- Создание/обновление/удаление профессий
- Создание и получение сессий

---

## ⚙️ Переменные окружения

Создайте файл `.env` на основе `.env.example`:

```bash
cp .env.example .env
```

### Необходимые переменные

```bash
# База данных
DATABASE_URL=sqlite:///./interview_trainer.db

# JWT настройки
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Режим отладки
DEBUG=true
```

> ⚠️ **Важно:** В production измените `SECRET_KEY` на случайную строку!

---

## 👤 Тестовые учетные данные

После первого запуска backend автоматически создает тестового пользователя с правами администратора:

| Поле | Значение |
|------|----------|
| **Email** | `admin@example.com` |
| **Пароль** | `admin123` |

---

## 🛠 Технологический стек

### Backend

| Технология | Версия | Назначение |
|------------|--------|------------|
| **FastAPI** | 0.100+ | Веб-фреймворк |
| **SQLAlchemy** | 2.0+ | ORM |
| **SQLite** | 3.x | База данных |
| **Pydantic** | 2.0+ | Валидация данных |
| **python-jose** | 3.x | JWT токены |
| **passlib[bcrypt]** | 1.7+ | Хеширование паролей |
| **uvicorn** | 0.23+ | ASGI сервер |

### Frontend

| Технология | Версия | Назначение |
|------------|--------|------------|
| **React** | 18.x | UI библиотека |
| **TypeScript** | 5.x | Типизация |
| **Vite** | 4.x | Сборщик |
| **TailwindCSS** | 3.x | Стилизация |
| **Zustand** | 4.x | State management |
| **React Router** | 6.x | Маршрутизация |
| **Axios** | 1.x | HTTP клиент |

---

## 📦 Скрипты

| Скрипт | Описание |
|--------|----------|
| `./scripts/setup.sh` | Автоматическая установка всех зависимостей |
| `./scripts/run_backend.sh` | Запуск backend сервера |
| `./scripts/run_frontend.sh` | Запуск frontend dev сервера |

---

## 🐛 Troubleshooting

### Backend не запускается

```bash
# Проверьте установку зависимостей
cd backend
source venv/bin/activate
pip install -r requirements.txt

# Проверьте наличие .env файла
cp .env.example .env
```

### Frontend не запускается

```bash
# Очистите кэш и переустановите зависимости
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### Ошибки базы данных

```bash
# Удалите старый файл БД и перезапустите seed
cd backend
rm data/interview_trainer.db
uvicorn app.main:app --reload
```

---

## 📄 Лицензия

MIT License — см. [LICENSE](LICENSE) файл для деталей.

---

## 🤝 Вклад в проект

1. Fork репозиторий
2. Создайте feature branch (`git checkout -b feature/amazing-feature`)
3. Закоммитьте изменения (`git commit -m 'Add amazing feature'`)
4. Запушьте branch (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

---

## 📞 Контакты

Вопросы и предложения направляйте через Issues в репозитории.

---

**Happy coding & Good luck with your interviews! 🚀**
