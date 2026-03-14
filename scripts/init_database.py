#!/usr/bin/env python3
"""
Первичная инициализация базы данных.
Запускается ОДИН РАЗ при первом запуске проекта.

Создаёт:
- Администратора (admin@example.com / admin123)
- Профессии (Frontend, Backend, Fullstack, DevOps)
- Достижения
- Начальные вопросы для каждой профессии

Использование:
    cd backend
    source venv/bin/activate
    python3 ../scripts/init_database.py
"""

import sys
import os

# Добавляем backend в path
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
backend_dir = os.path.join(project_dir, 'backend')
sys.path.insert(0, backend_dir)
os.chdir(backend_dir)

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.models.user import User
from app.models.profession import Profession
from app.models.question import Question
from app.models.category import Category
from app.models.user_progress import Achievement
from app.core.security import get_password_hash

# Создаем движок и сессию
engine = create_engine('sqlite:///./interview_trainer.db')
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

try:
    print("🚀 Начало инициализации базы данных...")
    print("=" * 50)
    
    # Проверяем что таблицы существуют
    from app.database.engine import Base, engine
    inspector = text("SELECT name FROM sqlite_master WHERE type='table'")
    with engine.connect() as conn:
        tables = conn.execute(inspector).fetchall()
        table_names = [t[0] for t in tables]
    
    if 'users' not in table_names:
        print("❌ Таблицы не найдены! Сначала примените миграции:")
        print("   cd backend && source venv/bin/activate")
        print("   python migrate.py upgrade")
        sys.exit(1)
    
    # ============================================
    # 1. Создаём администратора
    # ============================================
    if not db.query(User).first():
        admin = User(
            email="admin@example.com",
            hashed_password=get_password_hash("admin123"),
            is_admin=True
        )
        db.add(admin)
        print("✅ Администратор создан:")
        print("   Email: admin@example.com")
        print("   Пароль: admin123")
    else:
        print("⚠️  Пользователи уже существуют (пропущено)")
    
    # ============================================
    # 2. Создаём профессии
    # ============================================
    if not db.query(Profession).first():
        professions = [
            Profession(
                name="Frontend Developer",
                description="React, Vue, Angular, TypeScript, JavaScript"
            ),
            Profession(
                name="Backend Developer",
                description="Python, FastAPI, Django, Node.js, Go"
            ),
            Profession(
                name="Fullstack Developer",
                description="Frontend + Backend разработка"
            ),
            Profession(
                name="DevOps Engineer",
                description="CI/CD, Docker, Kubernetes, Cloud, Automation"
            ),
        ]
        db.add_all(professions)
        db.commit()
        print("✅ Профессии созданы (4)")
    else:
        print("⚠️  Профессии уже существуют (пропущено)")

    # Получаем ID профессий для категорий и вопросов
    professions_map = {}
    for p in db.query(Profession).all():
        professions_map[p.name] = p.id

    # ============================================
    # 3. Создаём категории для профессий
    # ============================================
    if not db.query(Category).first():
        # Frontend категории
        if professions_map.get("Frontend Developer"):
            frontend_id = professions_map["Frontend Developer"]
            frontend_categories = [
                Category(name="HTML/CSS", description="Основы вёрстки и стилей", profession_id=frontend_id),
                Category(name="JavaScript", description="Язык JavaScript и основы", profession_id=frontend_id),
                Category(name="React", description="Библиотека React", profession_id=frontend_id),
                Category(name="TypeScript", description="Типизация в JavaScript", profession_id=frontend_id),
            ]
            db.add_all(frontend_categories)

        # Backend категории
        if professions_map.get("Backend Developer"):
            backend_id = professions_map["Backend Developer"]
            backend_categories = [
                Category(name="Python", description="Язык Python", profession_id=backend_id),
                Category(name="REST API", description="Проектирование API", profession_id=backend_id),
                Category(name="Базы данных", description="SQL и NoSQL БД", profession_id=backend_id),
                Category(name="Архитектура", description="Микросервисы, паттерны", profession_id=backend_id),
            ]
            db.add_all(backend_categories)

        # Fullstack категории
        if professions_map.get("Fullstack Developer"):
            fullstack_id = professions_map["Fullstack Developer"]
            fullstack_categories = [
                Category(name="Frontend", description="Frontend разработка", profession_id=fullstack_id),
                Category(name="Backend", description="Backend разработка", profession_id=fullstack_id),
                Category(name="Базы данных", description="Работа с БД", profession_id=fullstack_id),
                Category(name="DevOps Basics", description="Основы DevOps", profession_id=fullstack_id),
            ]
            db.add_all(fullstack_categories)

        # DevOps категории
        if professions_map.get("DevOps Engineer"):
            devops_id = professions_map["DevOps Engineer"]
            devops_categories = [
                Category(name="Linux", description="ОС Linux, командная строка", profession_id=devops_id),
                Category(name="Docker", description="Контейнеризация", profession_id=devops_id),
                Category(name="Kubernetes", description="Оркестрация контейнеров", profession_id=devops_id),
                Category(name="CI/CD", description="Непрерывная интеграция и доставка", profession_id=devops_id),
                Category(name="Сети", description="Сетевые технологии", profession_id=devops_id),
                Category(name="Monitoring", description="Мониторинг и логирование", profession_id=devops_id),
                Category(name="IaC", description="Infrastructure as Code", profession_id=devops_id),
            ]
            db.add_all(devops_categories)

        db.commit()
        print("✅ Категории созданы")
    else:
        print("⚠️  Категории уже существуют (пропущено)")
    
    # ============================================
    # 3. Создаём достижения
    # ============================================
    if not db.query(Achievement).first():
        achievements = [
            Achievement(
                name="Первый шаг",
                description="Пройдите первую сессию",
                icon="🌱",
                xp_reward=50,
                requirement_type="sessions_completed",
                requirement_value=1,
                category="general"
            ),
            Achievement(
                name="Начинающий",
                description="Пройдите 5 сессий",
                icon="📚",
                xp_reward=100,
                requirement_type="sessions_completed",
                requirement_value=5,
                category="general"
            ),
            Achievement(
                name="Опытный",
                description="Пройдите 20 сессий",
                icon="🎓",
                xp_reward=250,
                requirement_type="sessions_completed",
                requirement_value=20,
                category="general"
            ),
            Achievement(
                name="Эксперт",
                description="Пройдите 50 сессий",
                icon="🏆",
                xp_reward=500,
                requirement_type="sessions_completed",
                requirement_value=50,
                category="general"
            ),
            Achievement(
                name="Перфекционист",
                description="Получите 100% в сессии",
                icon="💯",
                xp_reward=150,
                requirement_type="perfect_score",
                requirement_value=1,
                category="special"
            ),
            Achievement(
                name="Знаток",
                description="Ответьте правильно на 100 вопросов",
                icon="🧠",
                xp_reward=200,
                requirement_type="correct_answers",
                requirement_value=100,
                category="general"
            ),
            Achievement(
                name="Серия побед",
                description="Получите серию из 5 идеальных сессий",
                icon="🔥",
                xp_reward=300,
                requirement_type="streak",
                requirement_value=5,
                category="streak"
            ),
            Achievement(
                name="DevOps Мастер",
                description="Пройдите все DevOps вопросы",
                icon="⚙️",
                xp_reward=400,
                requirement_type="sessions_completed",
                requirement_value=10,
                category="profession"
            ),
        ]
        db.add_all(achievements)
        db.commit()
        print("✅ Достижения созданы (8)")
    else:
        print("⚠️  Достижения уже существуют (пропущено)")

    # ============================================
    # 4. Вопросы НЕ создаём!
    # ============================================
    # ВАЖНО: Этот скрипт БОЛЬШЕ НИКОГДА не создаёт вопросы.
    # Вопросы добавляются только через:
    # - Админ-панель (/admin)
    # - Импорт из JSON/CSV
    # - Прямое редактирование БД
    #
    # Данные пользователей (вопросы) НЕПРИКОСНОВЕННЫ!
    # ============================================
    print("\n📚 Вопросы не создаются (данные пользователей неприкосновенны)")
    print("   Для добавления вопросов используйте админ-панель или импорт")
    
    # ============================================
    # Итоги
    # ============================================
    print("\n" + "=" * 50)
    print("📊 ИТОГИ:")
    
    users_count = db.query(User).count()
    professions_count = db.query(Profession).count()
    questions_count = db.query(Question).count()
    achievements_count = db.query(Achievement).count()
    
    print(f"   Пользователей: {users_count}")
    print(f"   Профессий: {professions_count}")
    print(f"   Вопросов: {questions_count}")
    print(f"   Достижений: {achievements_count}")
    print("=" * 50)
    print("🎉 Инициализация завершена успешно!")
    print("\n📝 Для запуска приложения:")
    print("   cd backend && source venv/bin/activate")
    print("   uvicorn app.main:app --reload")
    print("\n🔐 Администратор:")
    print("   Email: admin@example.com")
    print("   Пароль: admin123")
    
except Exception as e:
    db.rollback()
    print(f"\n❌ Ошибка при инициализации: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
finally:
    db.close()
