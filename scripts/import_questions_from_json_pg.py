#!/usr/bin/env python3
"""
Импорт вопросов из JSON файла в PostgreSQL БД.
Использование: python scripts/import_questions_from_json_pg.py docs/linux_questions.json
"""

import sys
import os
import json

if len(sys.argv) < 2:
    print("Использование: python import_questions_from_json_pg.py <файл.json>")
    sys.exit(1)

json_file = sys.argv[1]

# Добавляем backend в path
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
backend_dir = os.path.join(project_dir, 'backend')
sys.path.insert(0, backend_dir)
os.chdir(backend_dir)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.profession import Profession
from app.models.question import Question
from app.core.config import settings

# Создаем движок и сессию для PostgreSQL
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

try:
    # Читаем JSON
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    questions_data = data.get('questions', data if isinstance(data, list) else [])

    print(f"📚 Импортируем вопросы из {json_file}...")
    print(f"   Всего вопросов в файле: {len(questions_data)}")

    # Кэш профессий
    professions_cache = {}
    for p in db.query(Profession).all():
        professions_cache[p.name] = p.id

    added = 0
    updated = 0
    skipped = 0

    for q_data in questions_data:
        profession_name = q_data.get('profession_name')
        profession_id = professions_cache.get(profession_name)

        if not profession_id:
            print(f"⚠️  Профессия не найдена: {profession_name}")
            skipped += 1
            continue

        # Проверяем дубликат по тексту вопроса
        existing = db.query(Question).filter(Question.text == q_data['text']).first()
        if existing:
            print(f"⏭️  Пропущен дубликат: {q_data['text'][:50]}...")
            skipped += 1
            continue

        question = Question(
            text=q_data['text'],
            question_type=q_data.get('question_type', 'mcq'),
            profession_id=profession_id,
            difficulty=q_data.get('difficulty', 'junior'),
            options=q_data['options'],
            correct_option=q_data.get('correct_option'),
            correct_order=q_data.get('correct_order'),
            explanation=q_data.get('explanation', '')
        )
        db.add(question)
        added += 1

    db.commit()

    print(f"\n✅ Готово!")
    print(f"   Добавлено: {added}")
    print(f"   Обновлено: {updated}")
    print(f"   Пропущено: {skipped}")

except Exception as e:
    db.rollback()
    print(f"❌ Ошибка: {e}")
    sys.exit(1)

finally:
    db.close()
