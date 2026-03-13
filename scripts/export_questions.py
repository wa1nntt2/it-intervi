#!/usr/bin/env python3
"""
Экспорт всех вопросов из БД в JSON файл.
Использование: python scripts/export_questions.py > backend/data/questions_backup.json
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
from datetime import datetime

# Создаем движок
engine = create_engine('sqlite:///./interview_trainer.db')

with engine.connect() as conn:
    # Получаем все вопросы с названиями профессий
    query = text("""
        SELECT 
            q.id,
            q.text,
            q.question_type,
            q.difficulty,
            q.options,
            q.correct_option,
            q.correct_order,
            q.explanation,
            p.name as profession_name
        FROM questions q
        JOIN professions p ON q.profession_id = p.id
        ORDER BY p.name, q.difficulty, q.id
    """)
    
    result = conn.execute(query)
    questions = []
    
    for row in result:
        questions.append({
            "id": row.id,
            "text": row.text,
            "question_type": row.question_type,
            "difficulty": row.difficulty,
            "options": json.loads(row.options) if row.options else [],
            "correct_option": row.correct_option,
            "correct_order": json.loads(row.correct_order) if row.correct_order else None,
            "explanation": row.explanation,
            "profession_name": row.profession_name
        })
    
    # Выводим JSON
    output = {
        "version": "1.0",
        "exported_at": datetime.utcnow().isoformat(),
        "total": len(questions),
        "questions": questions
    }
    
    print(json.dumps(output, ensure_ascii=False, indent=2))
    print(f"\n# Экспортировано вопросов: {len(questions)}", file=sys.stderr)
