#!/usr/bin/env python3
"""
Отвязать вопросы Linux от категории Сети.
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
    # Находим категории
    linux_result = db.execute(
        text("SELECT id FROM categories WHERE name = 'Linux' AND profession_id = 4")
    ).first()
    network_result = db.execute(
        text("SELECT id FROM categories WHERE name = 'Сети' AND profession_id = 4")
    ).first()
    
    if not linux_result or not network_result:
        print("❌ Категории не найдены!")
        sys.exit(1)
    
    linux_cat_id = linux_result[0]
    network_cat_id = network_result[0]
    print(f"✅ Linux ID={linux_cat_id}, Сети ID={network_cat_id}")
    
    # Вопросы Linux (ID 448-507) - отвязать от Сети
    linux_question_ids = list(range(448, 508))
    
    unbound = 0
    for q_id in linux_question_ids:
        result = db.execute(
            text("DELETE FROM question_categories WHERE question_id = :qid AND category_id = :cid"),
            {"qid": q_id, "cid": network_cat_id}
        )
        if result.rowcount > 0:
            unbound += 1
    
    db.commit()
    
    print(f"✅ Отвязано {unbound} вопросов Linux от категории Сети")
    
    # Финальная статистика
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
