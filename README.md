# IT Interview Trainer

Платформа для подготовки к техническим собеседованиям в IT.

## 🚀 Возможности

- **Вопросы по профессиям**: Frontend, Backend, Fullstack, DevOps
- **Разные типы вопросов**: 
  - Multiple Choice (один правильный ответ)
  - Ordering (расположение в правильном порядке)
- **Система сессий**: Прохождение тестов с подсчетом результатов
- **Админ-панель**: Управление вопросами
- **JWT аутентификация**: Безопасный вход и регистрация

## 📁 Структура проекта

```
it_interVI.it-interview-trainer/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── api/         # REST API endpoints
│   │   ├── core/        # Конфигурация, безопасность, кэш
│   │   ├── database/    # SQLAlchemy engine, seed
│   │   └── models/      # SQLAlchemy модели
│   └── requirements*.txt
├── frontend/            # React + TypeScript + Vite
│   └── src/
│       ├── components/  # UI компоненты
│       ├── pages/       # Страницы приложения
│       ├── stores/      # Zustand stores
│       └── services/    # API клиенты
├── tests/               # pytest тесты
└── scripts/             # Скрипты запуска
```

## 🛠 Установка

### Быстрый старт

```bash
# Установка всех зависимостей
./scripts/setup.sh
```

### Ручная установка

#### Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Frontend

```bash
cd frontend
npm install
```

## 🏃 Запуск

### Backend

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API доступно по адресу: http://localhost:8000
Документация Swagger: http://localhost:8000/docs

### Frontend

```bash
cd frontend
npm run dev
```

Приложение доступно по адресу: http://localhost:3000

## 🧪 Тесты

```bash
cd backend
source venv/bin/activate
pytest
```

## 📝 Переменные окружения

Скопируйте `.env.example` в `.env` и настройте:

```bash
cp .env.example .env
```

### Основные переменные

- `DATABASE_URL` - URL базы данных (SQLite по умолчанию)
- `SECRET_KEY` - Секретный ключ для JWT (измените в production!)
- `DEBUG` - Режим отладки

## 🧪 Тестовые учетные данные

После запуска backend автоматически создаст тестового пользователя:

- **Email**: admin@example.com
- **Пароль**: admin123

## 📚 Технологии

### Backend
- **FastAPI** - современный веб-фреймворк
- **SQLAlchemy** - ORM для работы с БД
- **SQLite** - база данных
- **Pydantic** - валидация данных
- **JWT** - аутентификация
- **bcrypt** - хеширование паролей

### Frontend
- **React 18** - UI библиотека
- **TypeScript** - типизация
- **Vite** - сборщик
- **TailwindCSS** - стилизация
- **Zustand** - управление состоянием
- **React Router** - маршрутизация
- **Axios** - HTTP клиент

## 📄 Лицензия

MIT
