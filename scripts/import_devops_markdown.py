#!/usr/bin/env python3
"""
Импорт вопросов DevOps из markdown файла.
Использование: python3 scripts/import_devops_markdown.py
"""

import sys
import os
import re

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
backend_dir = os.path.join(project_dir, 'backend')
sys.path.insert(0, backend_dir)
os.chdir(backend_dir)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.profession import Profession
from app.models.question import Question

# Читаем файл
markdown_file = os.path.join(project_dir, 'scripts/devops_questions.md')

with open(markdown_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Парсим вопросы
questions_data = []

# Регулярка для поиска строк таблицы
table_pattern = r'\|\s*\*\*(\d+)\*\*\s*\|\s*`(\w+)`\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*\*\*([ABCD])\*\*\s*\|\s*(.+?)\s*\|'

matches = re.findall(table_pattern, content, re.DOTALL)

for match in matches:
    (
        num, level, question_text, option_a, option_b, option_c, option_d,
        correct_letter, explanation
    ) = match
    
    # Очищаем текст от лишних символов
    question_text = question_text.strip()
    option_a = option_a.strip()
    option_b = option_b.strip()
    option_c = option_c.strip()
    option_d = option_d.strip()
    explanation = explanation.strip()
    
    # Определяем индекс правильного ответа
    correct_map = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
    correct_option = correct_map.get(correct_letter, 0)
    
    # Создаем варианты ответов
    options = [option_a, option_b, option_c, option_d]
    
    # Определяем сложность
    difficulty_map = {
        'Intern': 'intern',
        'Junior': 'junior',
        'Middle': 'middle'
    }
    difficulty = difficulty_map.get(level, 'junior')
    
    questions_data.append({
        'text': question_text,
        'difficulty': difficulty,
        'options': options,
        'correct_option': correct_option,
        'explanation': explanation
    })

print(f"📚 Распарсено вопросов: {len(questions_data)}")

# Создаем движок и сессию
engine = create_engine('sqlite:///./interview_trainer.db')
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

try:
    # Находим DevOps профессию
    devops = db.query(Profession).filter(Profession.name == "DevOps Engineer").first()
    if not devops:
        print("❌ Профессия DevOps Engineer не найдена!")
        sys.exit(1)
    
    print(f"✅ Найдена профессия: {devops.name} (id={devops.id})")
    
    # Счетчики
    added = 0
    skipped = 0
    
    # Добавляем вопросы
    print("\n📚 Добавляем вопросы...")
    for q_data in questions_data:
        # Проверяем, есть ли уже такой вопрос
        existing = db.query(Question).filter(
            Question.text == q_data["text"],
            Question.profession_id == devops.id
        ).first()
        
        if existing:
            skipped += 1
            continue
        
        # Создаем вопрос
        question = Question(
            text=q_data["text"],
            question_type="mcq",
            profession_id=devops.id,
            difficulty=q_data["difficulty"],
            options=q_data["options"],
            correct_option=q_data["correct_option"],
            explanation=q_data.get("explanation", "")
        )
        db.add(question)
        added += 1
        
        # Коммитим каждые 50 вопросов
        if added % 50 == 0:
            db.commit()
            print(f"   ✅ Добавлено {added} вопросов...")
    
    db.commit()
    
    print("\n" + "=" * 50)
    print("📊 ИТОГИ:")
    print(f"   Добавлено: {added}")
    print(f"   Пропущено (дубликаты): {skipped}")
    print(f"   Всего в БД: {db.query(Question).filter(Question.profession_id == devops.id).count()}")
    print("=" * 50)
    print("✅ Импорт завершен!")
    
except Exception as e:
    db.rollback()
    print(f"❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()
    raise
finally:
    db.close()
