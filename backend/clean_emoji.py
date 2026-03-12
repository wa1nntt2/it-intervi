#!/usr/bin/env python3
"""Очистка вопросов от emoji ❌ ✅"""

from app.database.engine import SessionLocal
from app.models.question import Question

db = SessionLocal()

try:
    questions = db.query(Question).all()
    updated = 0
    
    for q in questions:
        cleaned_options = []
        for opt in q.options:
            opt = opt.replace("❌ ", "").replace("✅ ", "")
            opt = opt.replace("❌", "").replace("✅", "")
            cleaned_options.append(opt.strip())
        
        if cleaned_options != q.options:
            q.options = cleaned_options
            updated += 1
        
        if updated % 50 == 0:
            db.commit()
            print(f"   ✅ Очищено {updated} вопросов...")
    
    db.commit()
    print(f"\n✅ Всего очищено: {updated}")
    
except Exception as e:
    db.rollback()
    print(f"❌ Ошибка: {e}")
    raise
finally:
    db.close()
