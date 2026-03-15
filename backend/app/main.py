# Основной модуль приложения FastAPI
# Точка входа для backend сервера

import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware  # Middleware для поддержки CORS
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded  # Обработчик ошибок rate limiting
from slowapi.middleware import SlowAPIMiddleware

from app.database.engine import Base, engine, SessionLocal
from app.database.seed import seed_database
from app.core.config import settings
from app.core.limiter import limiter

# Импорт моделей для создания таблиц базы данных
from app.models import user, profession, question, answer, ordering_item, session, user_progress

# Импорт API роутеров (endpoint'ов)
from app.api import auth, professions, questions, sessions, users, progress, interviews


def apply_migrations():
    """
    Применение миграций Alembic при запуске приложения.
    Если миграции еще не применены, создаем таблицы через create_all.
    """
    # Отключаем миграции для тестов
    skip_migrations = os.getenv("SKIP_MIGRATIONS", "false").lower() == "true"
    if skip_migrations:
        print("⏭️  Пропускаем миграции (SKIP_MIGRATIONS=true)")
        return
    
    try:
        from alembic import command
        from alembic.config import Config
        from pathlib import Path

        backend_dir = Path(__file__).parent.parent
        alembic_cfg = Config(backend_dir / "alembic.ini")

        # Проверяем, есть ли уже примененные миграции
        from alembic.script import ScriptDirectory
        from alembic.runtime.migration import MigrationContext

        script = ScriptDirectory.from_config(alembic_cfg)

        with engine.connect() as conn:
            context = MigrationContext.configure(conn)
            current_rev = context.get_current_revision()

            if current_rev is None:
                # Миграции не применены - создаем таблицы старым способом
                # для обратной совместимости
                print("⚠️  Миграции не найдены, создаем таблицы через create_all()...")
                Base.metadata.create_all(bind=engine)
            else:
                # Миграции уже применены
                print(f"✅ Миграции применены (текущая ревизия: {current_rev})")

    except Exception as e:
        print(f"⚠️  Ошибка при проверке миграций: {e}")
        print("Создаем таблицы через create_all()...")
        Base.metadata.create_all(bind=engine)


def rate_limit_exception_handler(request: Request, exc: RateLimitExceeded):
    """
    Обработчик исключений для rate limiter.
    Возвращает JSON ответ с ошибкой 429 (Too Many Requests).
    """
    return JSONResponse(
        status_code=429,
        content={
            "detail": "Слишком много запросов. Попробуйте позже.",
            "limit": str(exc.limit.limit)
        }
    )


def create_app() -> FastAPI:
    """
    Фабрика приложения FastAPI.
    Создает и настраивает экземпляр приложения со всеми middleware и роутерами.
    """
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        debug=settings.DEBUG
    )

    # Добавляем rate limiter для ограничения количества запросов
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, rate_limit_exception_handler)
    app.add_middleware(SlowAPIMiddleware)

    # CORS - настройка для конкретных origin (разрешенные домены)
    cors_origins = [origin.strip() for origin in settings.CORS_ORIGINS.split(",")]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Применение миграций или создание таблиц
    apply_migrations()

    # Сидирование базы данных начальными данными (отключаем для тестов)
    if not os.environ.get("SKIP_SEED"):
        db = SessionLocal()
        try:
            seed_database(db)
        finally:
            db.close()

    # Регистрация API роутеров с префиксом /api
    app.include_router(auth.router, prefix="/api")
    app.include_router(professions.router, prefix="/api")
    app.include_router(questions.router, prefix="/api")
    app.include_router(sessions.router, prefix="/api")
    app.include_router(users.router, prefix="/api")
    app.include_router(progress.router, prefix="/api")
    app.include_router(interviews.router, prefix="/api")

    @app.get("/")
    def root():
        """Корневой endpoint - возвращает информацию о API"""
        return {"message": "IT Interview Trainer API", "version": settings.VERSION}

    @app.get("/health")
    def health_check():
        """Endpoint для проверки здоровья приложения"""
        return {"status": "healthy"}

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
