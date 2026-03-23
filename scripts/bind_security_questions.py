#!/usr/bin/env python3
"""
Привязка вопросов Security к категории "Безопасность".
"""

import sys
import os

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
backend_dir = os.path.join(project_dir, 'backend')
sys.path.insert(0, backend_dir)
os.chdir(backend_dir)

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

try:
    # Находим категорию "Безопасность" для DevOps (profession_id=4)
    result = db.execute(
        text("SELECT id FROM categories WHERE name = 'Безопасность' AND profession_id = 4")
    ).first()
    
    if not result:
        print("❌ Категория 'Безопасность' не найдена!")
        sys.exit(1)
    
    category_id = result[0]
    print(f"✅ Категория 'Безопасность' найдена (ID={category_id})")
    
    # Получаем последние вопросы DevOps без категории (security)
    result = db.execute(
        text("""
            SELECT q.id FROM questions q
            WHERE q.profession_id = 4
            AND q.id NOT IN (
                SELECT qc.question_id FROM question_categories qc
                WHERE qc.category_id = :cid
            )
            ORDER BY q.id DESC
            LIMIT 30
        """),
        {"cid": category_id}
    ).fetchall()
    question_ids = [row[0] for row in result]
    
    total = len(question_ids)
    print(f"📚 Найдено {total} вопросов для категории Безопасность")
    
    if not question_ids:
        print("✅ Все вопросы уже привязаны к категории 'Безопасность'")
        sys.exit(0)
    
    # Привязываем вопросы к категории
    bound_count = 0
    for q_id in question_ids:
        db.execute(
            text("INSERT INTO question_categories (question_id, category_id) VALUES (:qid, :cid)"),
            {"qid": q_id, "cid": category_id}
        )
        bound_count += 1
    
    db.commit()
    
    print(f"✅ Привязано {bound_count} вопросов к категории 'Безопасность'")
    
    # Статистика
    stats = db.execute(
        text("""
            SELECT c.name, COUNT(qc.question_id) as count
            FROM categories c
            LEFT JOIN question_categories qc ON c.id = qc.category_id
            WHERE c.profession_id = 4
            GROUP BY c.id, c.name
            ORDER BY c.id
        """)
    ).fetchall()
    
    print("\n📊 Категории DevOps:")
    for row in stats:
        print(f"   {row[0]}: {row[1]} вопросов")

except Exception as e:
    db.rollback()
    print(f"❌ Ошибка: {e}")
    sys.exit(1)

finally:
    db.close()
