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
    
    # Получаем ID профессий для вопросов
    professions_map = {}
    for p in db.query(Profession).all():
        professions_map[p.name] = p.id
    
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
    # 4. Создаём начальные вопросы
    # ============================================
    print("\n📚 Добавление начальных вопросов...")
    
    # Frontend вопросы
    if professions_map.get("Frontend Developer"):
        frontend_id = professions_map["Frontend Developer"]
        if db.query(Question).filter(Question.profession_id == frontend_id).count() == 0:
            frontend_questions = [
                Question(
                    text="Что такое HTML?",
                    question_type="mcq",
                    profession_id=frontend_id,
                    difficulty="intern",
                    options=["Язык разметки", "Язык программирования", "База данных", "Фреймворк"],
                    correct_option=0,
                    explanation="HTML (HyperText Markup Language) — это язык гипертекстовой разметки."
                ),
                Question(
                    text="Что такое Virtual DOM?",
                    question_type="mcq",
                    profession_id=frontend_id,
                    difficulty="intern",
                    options=["Прямая копия реального DOM", "Легковесная копия реального DOM", "База данных", "Библиотека"],
                    correct_option=1,
                    explanation="Virtual DOM — это легковесная копия реального DOM в памяти."
                ),
                Question(
                    text="Что такое useEffect в React?",
                    question_type="mcq",
                    profession_id=frontend_id,
                    difficulty="junior",
                    options=["Хук для состояния", "Хук для побочных эффектов", "Хук для мемоизации", "Хук для навигации"],
                    correct_option=1,
                    explanation="useEffect — хук для выполнения побочных эффектов."
                ),
                Question(
                    text="Расположите этапы жизненного цикла React",
                    question_type="ordering",
                    profession_id=frontend_id,
                    difficulty="junior",
                    options=["Mounting", "Updating", "Unmounting"],
                    correct_order=[0, 1, 2],
                    explanation="Жизненный цикл: Mounting → Updating → Unmounting"
                ),
                Question(
                    text="Что такое React Fiber?",
                    question_type="mcq",
                    profession_id=frontend_id,
                    difficulty="middle",
                    options=["Новая версия React", "Архитектура рендеринга", "Библиотека анимаций", "Инструмент отладки"],
                    correct_option=1,
                    explanation="React Fiber — архитектура движка согласования в React 16+."
                ),
                Question(
                    text="Что такое TypeScript?",
                    question_type="mcq",
                    profession_id=frontend_id,
                    difficulty="intern",
                    options=["Язык программирования", "Надстройка над JS с типами", "Фреймворк", "Библиотека"],
                    correct_option=1,
                    explanation="TypeScript — это язык с статической типизацией, компилируемый в JavaScript."
                ),
            ]
            db.add_all(frontend_questions)
            db.commit()
            print(f"   ✅ Frontend: {len(frontend_questions)} вопросов")
        else:
            print("   ⚠️  Frontend вопросы уже существуют (пропущено)")
    
    # Backend вопросы
    if professions_map.get("Backend Developer"):
        backend_id = professions_map["Backend Developer"]
        if db.query(Question).filter(Question.profession_id == backend_id).count() == 0:
            backend_questions = [
                Question(
                    text="Что такое REST API?",
                    question_type="mcq",
                    profession_id=backend_id,
                    difficulty="intern",
                    options=["Протокол", "Архитектурный стиль", "Язык", "База данных"],
                    correct_option=1,
                    explanation="REST — архитектурный стиль для проектирования веб-сервисов."
                ),
                Question(
                    text="Что такое SQL?",
                    question_type="mcq",
                    profession_id=backend_id,
                    difficulty="intern",
                    options=["Язык программирования", "Язык запросов к БД", "Фреймворк", "ОС"],
                    correct_option=1,
                    explanation="SQL — язык для работы с реляционными базами данных."
                ),
                Question(
                    text="Что такое микросервисы?",
                    question_type="mcq",
                    profession_id=backend_id,
                    difficulty="junior",
                    options=["Монолит", "Архитектура из небольших сервисов", "База данных", "Фреймворк"],
                    correct_option=1,
                    explanation="Микросервисы — архитектура приложения как набора небольших независимых сервисов."
                ),
                Question(
                    text="Что такое FastAPI?",
                    question_type="mcq",
                    profession_id=backend_id,
                    difficulty="intern",
                    options=["База данных", "Веб-фреймворк Python", "Язык", "Библиотека"],
                    correct_option=1,
                    explanation="FastAPI — современный веб-фреймворк для Python с автоматической документацией."
                ),
            ]
            db.add_all(backend_questions)
            db.commit()
            print(f"   ✅ Backend: {len(backend_questions)} вопросов")
        else:
            print("   ⚠️  Backend вопросы уже существуют (пропущено)")
    
    # Fullstack вопросы
    if professions_map.get("Fullstack Developer"):
        fullstack_id = professions_map["Fullstack Developer"]
        if db.query(Question).filter(Question.profession_id == fullstack_id).count() == 0:
            fullstack_questions = [
                Question(
                    text="Что такое MVC паттерн?",
                    question_type="mcq",
                    profession_id=fullstack_id,
                    difficulty="junior",
                    options=["Model-View-Controller", "Model-View-Component", "Module-View", "Model-Visual"],
                    correct_option=0,
                    explanation="MVC — паттерн: Model (данные), View (отображение), Controller (логика)."
                ),
                Question(
                    text="Что такое JWT токен?",
                    question_type="mcq",
                    profession_id=fullstack_id,
                    difficulty="junior",
                    options=["База данных", "Токен аутентификации", "Язык", "Фреймворк"],
                    correct_option=1,
                    explanation="JWT — стандарт для передачи данных аутентификации между сторонами."
                ),
            ]
            db.add_all(fullstack_questions)
            db.commit()
            print(f"   ✅ Fullstack: {len(fullstack_questions)} вопросов")
        else:
            print("   ⚠️  Fullstack вопросы уже существуют (пропущено)")
    
    # DevOps вопросы
    if professions_map.get("DevOps Engineer"):
        devops_id = professions_map["DevOps Engineer"]
        if db.query(Question).filter(Question.profession_id == devops_id).count() == 0:
            devops_questions = [
                Question(
                    text="Что такое CI/CD?",
                    question_type="mcq",
                    profession_id=devops_id,
                    difficulty="intern",
                    options=["Continuous Integration / Continuous Delivery", "Computer Interface", "Central Display", "Continuous Display"],
                    correct_option=0,
                    explanation="CI/CD — непрерывная интеграция и доставка/развертывание."
                ),
                Question(
                    text="Что такое Docker?",
                    question_type="mcq",
                    profession_id=devops_id,
                    difficulty="intern",
                    options=["Платформа виртуализации", "Платформа контейнеризации", "ОС", "Язык"],
                    correct_option=1,
                    explanation="Docker — платформа для разработки, доставки и запуска приложений в контейнерах."
                ),
                Question(
                    text="Что такое Kubernetes?",
                    question_type="mcq",
                    profession_id=devops_id,
                    difficulty="junior",
                    options=["СУБД", "Система оркестрации контейнеров", "Мониторинг", "Контроль версий"],
                    correct_option=1,
                    explanation="Kubernetes — система оркестрации контейнеров."
                ),
                Question(
                    text="Что такое Infrastructure as Code?",
                    question_type="mcq",
                    profession_id=devops_id,
                    difficulty="junior",
                    options=["Документация", "Управление инфраструктурой через код", "Язык", "Физическая инфраструктура"],
                    correct_option=1,
                    explanation="IaC — управление инфраструктурой через код и автоматизацию."
                ),
                Question(
                    text="Расположите этапы CI/CD pipeline",
                    question_type="ordering",
                    profession_id=devops_id,
                    difficulty="junior",
                    options=["Build", "Test", "Deploy", "Monitor"],
                    correct_order=[0, 1, 2, 3],
                    explanation="Стандартный pipeline: Build → Test → Deploy → Monitor"
                ),
                Question(
                    text="Что такое Prometheus?",
                    question_type="mcq",
                    profession_id=devops_id,
                    difficulty="middle",
                    options=["Логирование", "Мониторинг и алертинг", "CI/CD", "Управление контейнерами"],
                    correct_option=1,
                    explanation="Prometheus — система мониторинга и алертинга."
                ),
                Question(
                    text="Что такое Terraform?",
                    question_type="mcq",
                    profession_id=devops_id,
                    difficulty="middle",
                    options=["Мониторинг", "IaC инструмент от HashiCorp", "Контейнеризация", "Тестирование"],
                    correct_option=1,
                    explanation="Terraform — инструмент IaC от HashiCorp."
                ),
                Question(
                    text="Что такое Blue-Green Deployment?",
                    question_type="mcq",
                    profession_id=devops_id,
                    difficulty="middle",
                    options=["Тестирование", "Стратегия развертывания с двумя средами", "Мониторинг", "Бэкап"],
                    correct_option=1,
                    explanation="Blue-Green — стратегия развертывания с двумя идентичными средами."
                ),
            ]
            db.add_all(devops_questions)
            db.commit()
            print(f"   ✅ DevOps: {len(devops_questions)} вопросов")
        else:
            print("   ⚠️  DevOps вопросы уже существуют (пропущено)")
    
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
