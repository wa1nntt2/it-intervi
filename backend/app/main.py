# Основной модуль приложения FastAPI
# Точка входа для backend сервера

import os
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware  # Middleware для поддержки CORS
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded  # Обработчик ошибок rate limiting
from slowapi.middleware import SlowAPIMiddleware

from app.database.engine import Base, engine, SessionLocal
from app.database.seed import seed_database
from app.core.config import settings
from app.core.limiter import limiter
from app.core.logging_config import setup_logging, get_logger

# Настройка логирования
logger = setup_logging(
    log_level="DEBUG" if settings.DEBUG else "INFO",
    log_file="logs/app.log" if not settings.DEBUG else None,
    json_format=not settings.DEBUG,  # JSON формат для production
    log_sql=settings.DEBUG,  # Логирование SQL только в development
)

# Импорт моделей для создания таблиц базы данных
from app.models import user, profession, question, answer, ordering_item, session, user_progress

# Импорт API роутеров (endpoint'ов)
from app.api import auth, professions, questions, sessions, users, progress, interviews

# Prometheus метрики
from prometheus_client import generate_latest, Counter, Histogram
from fastapi.responses import Response
from starlette.requests import Request
import time

# Тип контента для Prometheus
CONTENT_TYPE = "text/plain; version=0.0.4; charset=utf-8"

# Счётчики метрик
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


def apply_migrations():
    """
    Применение миграций Alembic при запуске приложения.
    Если миграции еще не применены, создаем таблицы через create_all.
    """
    # Отключаем миграции для тестов
    skip_migrations = os.getenv("SKIP_MIGRATIONS", "false").lower() == "true"
    if skip_migrations:
        logger.info("⏭️  Пропускаем миграции (SKIP_MIGRATIONS=true)")
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
                logger.warning("⚠️  Миграции не найдены, создаем таблицы через create_all()...")
                Base.metadata.create_all(bind=engine)
            else:
                # Миграции уже применены
                logger.info(f"✅ Миграции применены (текущая ревизия: {current_rev})")

    except Exception as e:
        logger.error(f"⚠️  Ошибка при проверке миграций: {e}", exc_info=True)
        logger.warning("Создаем таблицы через create_all()...")
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
    logger.info(f"🚀 Запуск {settings.PROJECT_NAME} v{settings.VERSION}")
    logger.info(f"Режим: {'DEBUG' if settings.DEBUG else 'PRODUCTION'}")
    
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        debug=settings.DEBUG
    )

    # Добавляем rate limiter для ограничения количества запросов
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, rate_limit_exception_handler)
    app.add_middleware(SlowAPIMiddleware)
    logger.debug("✅ Rate limiter добавлен")

    # CORS - настройка для конкретных origin (разрешенные домены)
    cors_origins = [origin.strip() for origin in settings.CORS_ORIGINS.split(",")]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    logger.debug(f"✅ CORS настроен для: {cors_origins}")

    # Prometheus middleware для сбора метрик
    @app.middleware("http")
    async def track_requests(request: Request, call_next):
        """Middleware для сбора метрик каждого запроса"""
        start_time = time.time()

        response = await call_next(request)

        duration = time.time() - start_time

        # Считаем запросы
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.url.path,
            status=response.status_code
        ).inc()

        # Замеряем время
        REQUEST_TIME.labels(
            method=request.method,
            endpoint=request.url.path
        ).observe(duration)

        # Логгируем медленные запросы
        if duration > 1.0:
            logger.warning(f"🐌 Медленный запрос: {request.method} {request.url.path} - {duration:.2f}s")

        return response

    # Применение миграций или создание таблиц
    apply_migrations()

    # Сидирование базы данных начальными данными (отключаем для тестов)
    if not os.environ.get("SKIP_SEED"):
        logger.info("🌱 Сидирование базы данных...")
        db = SessionLocal()
        try:
            seed_database(db)
            logger.info("✅ База данных засидирована")
        except Exception as e:
            logger.error(f"❌ Ошибка при сидировании БД: {e}", exc_info=True)
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
    logger.info("✅ API роутеры зарегистрированы")

    @app.get("/")
    def root():
        """Корневой endpoint - возвращает информацию о API"""
        return {"message": "IT Interview Trainer API", "version": settings.VERSION}

    @app.get("/health")
    def health_check():
        """Endpoint для проверки здоровья приложения"""
        return {"status": "healthy"}

    @app.get("/metrics")
    async def metrics():
        """Endpoint для Prometheus метрик"""
        return Response(generate_latest(), media_type=CONTENT_TYPE)

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
