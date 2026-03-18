#!/usr/bin/env python3
"""
Скрипт для создания категорий для всех профессий.
"""

import sys
import os

# Добавляем backend в path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.database.engine import SessionLocal
from app.models.category import Category
from app.models.profession import Profession

# Категории для каждой профессии
CATEGORIES = {
    "Frontend": [
        "HTML & CSS",
        "JavaScript",
        "React",
        "Vue",
        "Angular",
        "TypeScript",
        "CSS Frameworks",
        "Build Tools",
    ],
    "Backend": [
        "Python",
        "Базы данных",
        "API Design",
        "Архитектура",
        "Безопасность",
        "Кэширование",
        "Микросервисы",
        "Тестирование",
    ],
    "Fullstack": [
        "Frontend + Backend",
        "Архитектура приложений",
        "Базы данных",
        "DevOps основы",
        "API Integration",
        "Аутентификация",
        "Deployment",
        "Производительность",
    ],
    "DevOps": [
        "Linux",
        "Docker",
        "Kubernetes",
        "CI/CD",
        "Infrastructure as Code",
        "Мониторинг",
        "Сети",
        "Безопасность",
        "Git",
        "Scripting",
    ],
}


def create_categories():
    db = SessionLocal()
    try:
        # Получаем все профессии
        professions = db.query(Profession).all()
        
        for profession in professions:
            print(f"\n📁 Профессия: {profession.name}")
            
            # Получаем категории для этой профессии
            prof_categories = CATEGORIES.get(profession.name, [])
            
            for cat_name in prof_categories:
                # Проверяем существует ли категория
                existing = db.query(Category).filter(
                    Category.name == cat_name,
                    Category.profession_id == profession.id
                ).first()
                
                if not existing:
                    category = Category(
                        name=cat_name,
                        description=f"Вопросы по теме {cat_name}",
                        profession_id=profession.id
                    )
                    db.add(category)
                    print(f"  ✅ Добавлена: {cat_name}")
                else:
                    print(f"  ⏭️  Пропущена: {cat_name} (уже есть)")
        
        db.commit()
        print("\n✅ Категории успешно созданы!")
        
        # Выводим статистику
        total = db.query(Category).count()
        print(f"📊 Всего категорий: {total}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Ошибка: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    create_categories()
