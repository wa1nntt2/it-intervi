#!/usr/bin/env python3
"""
Инициализация БД для PRODUCTION.
Создаёт ТОЛЬКО:
- Администратора
- Профессии
- Достижения

Вопросы НЕ создаются - добавляются через админку или импорт!
"""

import sys
import os

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
backend_dir = os.path.join(project_dir, 'backend')
sys.path.insert(0, backend_dir)
os.chdir(backend_dir)

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.models.user import User
from app.models.profession import Profession
from app.models.user_progress import Achievement
from app.core.security import get_password_hash

engine = create_engine('sqlite:///./interview_trainer.db')
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

try:
    print("🚀 Production инициализация...")
    print("=" * 50)
    
    # Проверяем таблицы
    inspector = text("SELECT name FROM sqlite_master WHERE type='table'")
    with engine.connect() as conn:
        tables = conn.execute(inspector).fetchall()
        table_names = [t[0] for t in tables]
    
    if 'users' not in table_names:
        print("❌ Таблицы не найдены! Сначала примените миграции:")
        print("   python migrate.py upgrade")
        sys.exit(1)
    
    # 1. Админ
    if not db.query(User).first():
        admin = User(
            email="admin@example.com",
            hashed_password=get_password_hash("admin123"),
            is_admin=True
        )
        db.add(admin)
        print("✅ Администратор создан")
    else:
        print("⚠️  Пользователи существуют (пропущено)")
    
    # 2. Профессии
    if not db.query(Profession).first():
        professions = [
            Profession(name="Frontend Developer", description="React, Vue, Angular"),
            Profession(name="Backend Developer", description="Python, Node.js, Go"),
            Profession(name="Fullstack Developer", description="Frontend + Backend"),
            Profession(name="DevOps Engineer", description="CI/CD, Docker, Kubernetes"),
        ]
        db.add_all(professions)
        db.commit()
        print("✅ Профессии созданы (4)")
    else:
        print("⚠️  Профессии существуют (пропущено)")
    
    # 3. Достижения
    if not db.query(Achievement).first():
        achievements = [
            Achievement(name="Первый шаг", description="Пройдите первую сессию", icon="🌱", xp_reward=50, requirement_type="sessions_completed", requirement_value=1, category="general"),
            Achievement(name="Начинающий", description="Пройдите 5 сессий", icon="📚", xp_reward=100, requirement_type="sessions_completed", requirement_value=5, category="general"),
            Achievement(name="Опытный", description="Пройдите 20 сессий", icon="🎓", xp_reward=250, requirement_type="sessions_completed", requirement_value=20, category="general"),
            Achievement(name="Эксперт", description="Пройдите 50 сессий", icon="🏆", xp_reward=500, requirement_type="sessions_completed", requirement_value=50, category="general"),
            Achievement(name="Перфекционист", description="Получите 100% в сессии", icon="💯", xp_reward=150, requirement_type="perfect_score", requirement_value=1, category="special"),
            Achievement(name="Знаток", description="Ответьте правильно на 100 вопросов", icon="🧠", xp_reward=200, requirement_type="correct_answers", requirement_value=100, category="general"),
            Achievement(name="Серия побед", description="Серия из 5 идеальных сессий", icon="🔥", xp_reward=300, requirement_type="streak", requirement_value=5, category="streak"),
            Achievement(name="DevOps Мастер", description="Пройдите все DevOps вопросы", icon="⚙️", xp_reward=400, requirement_type="sessions_completed", requirement_value=10, category="profession"),
        ]
        db.add_all(achievements)
        db.commit()
        print("✅ Достижения созданы (8)")
    else:
        print("⚠️  Достижения существуют (пропущено)")
    
    db.close()
    
    print("\n" + "=" * 50)
    print("🎉 Production БД готова!")
    print("=" * 50)
    print("\n📝 Следующие шаги:")
    print("   1. Сделайте бэкап: ./scripts/backup_db.sh")
    print("   2. Добавьте вопросы через админку")
    print("   3. Или импортируйте: python3 scripts/import_questions_from_json.py <файл.json>")
    
except Exception as e:
    db.rollback()
    print(f"❌ Ошибка: {e}")
    raise
