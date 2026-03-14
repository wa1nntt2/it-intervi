#!/usr/bin/env python3
"""
Скрипт для восстановления вопросов из backup.
Восстанавливает все 141 вопрос из backup файла.

Использование:
    cd backend
    source venv/bin/activate
    python3 ../scripts/restore_questions.py
"""

import sys
import os
import json

# Добавляем backend в path
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
backend_dir = os.path.join(project_dir, 'backend')
sys.path.insert(0, backend_dir)
os.chdir(backend_dir)

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.models.question import Question
from app.models.profession import Profession

# Создаем движок и сессию
engine = create_engine('sqlite:///./interview_trainer.db')
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

try:
    print("🔄 Восстановление вопросов из backup...")
    print("=" * 50)

    # Читаем backup файл
    backup_path = os.path.join(project_dir, 'backups', 'questions_latest.json')
    with open(backup_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    questions_data = data.get('questions', [])
    print(f"📦 В backup найдено вопросов: {len(questions_data)}")

    # Получаем маппинг профессий
    professions_map = {}
    for p in db.query(Profession).all():
        professions_map[p.name.lower()] = p.id
        # Также добавляем сокращенные названия
        if 'frontend' in p.name.lower():
            professions_map['frontend developer'] = p.id
        if 'backend' in p.name.lower():
            professions_map['backend developer'] = p.id
        if 'fullstack' in p.name.lower():
            professions_map['fullstack developer'] = p.id
        if 'devops' in p.name.lower():
            professions_map['devops engineer'] = p.id

    # Считаем текущие вопросы
    current_count = db.query(Question).count()
    print(f"📊 Текущее количество вопросов в БД: {current_count}")

    # Импортируем вопросы
    imported_count = 0
    errors = []

    for idx, q_data in enumerate(questions_data):
        try:
            # Определяем profession_id
            prof_id = q_data.get('profession_id')
            if prof_id is None:
                prof_name = q_data.get('profession_name', '')
                prof_name_lower = prof_name.lower()
                
                # Ищем по названию
                if prof_name_lower in professions_map:
                    prof_id = professions_map[prof_name_lower]
                else:
                    errors.append(f"Вопрос {idx}: Профессия не найдена: {prof_name}")
                    continue

            # Проверяем, нет ли уже такого вопроса (по тексту)
            existing = db.query(Question).filter(
                Question.text == q_data['text'],
                Question.profession_id == prof_id
            ).first()

            if existing:
                # Обновляем существующий вопрос
                existing.question_type = q_data.get('question_type', 'mcq')
                existing.difficulty = q_data.get('difficulty', 'junior')
                existing.options = q_data.get('options', [])
                existing.correct_option = q_data.get('correct_option')
                existing.correct_order = q_data.get('correct_order')
                existing.explanation = q_data.get('explanation')
            else:
                # Создаем новый вопрос
                question = Question(
                    text=q_data['text'],
                    question_type=q_data.get('question_type', 'mcq'),
                    profession_id=int(prof_id),
                    difficulty=q_data.get('difficulty', 'junior'),
                    options=q_data.get('options', []),
                    correct_option=q_data.get('correct_option'),
                    correct_order=q_data.get('correct_order'),
                    explanation=q_data.get('explanation')
                )
                db.add(question)

            imported_count += 1

        except Exception as e:
            errors.append(f"Вопрос {idx}: {str(e)}")

    db.commit()

    print("\n" + "=" * 50)
    print("📊 ИТОГИ:")
    print(f"   ✅ Импортировано вопросов: {imported_count}")
    print(f"   ❌ Ошибок: {len(errors)}")
    
    if errors:
        print("\n⚠️  Ошибки:")
        for err in errors[:10]:  # Показываем первые 10
            print(f"   - {err}")
        if len(errors) > 10:
            print(f"   ... и ещё {len(errors) - 10} ошибок")

    final_count = db.query(Question).count()
    print(f"\n📈 Всего вопросов в БД: {final_count}")
    print("=" * 50)
    print("🎉 Восстановление завершено!")

except Exception as e:
    db.rollback()
    print(f"\n❌ Ошибка при восстановлении: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
finally:
    db.close()
