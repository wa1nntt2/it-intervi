#!/usr/bin/env python3
"""
Скрипт для импорта вопросов DevOps из JSON бэкапа.
Запуск: cd backend && source venv/bin/activate && python3 ../scripts/import_devops_backup.py
"""

import sys
import os
import json

# Добавляем backend в path
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
backend_dir = os.path.join(project_dir, 'backend')
sys.path.insert(0, backend_dir)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Используем БД из backend директории
DATABASE_URL = "sqlite:///./data/interview_trainer.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

from app.models.profession import Profession
from app.models.question import Question

def import_questions(backup_file: str):
    """Импорт вопросов из JSON файла"""
    
    # Читаем бэкап
    with open(backup_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"📦 Загрузка вопросов из {backup_file}")
    print(f"   Версия: {data.get('version', 'unknown')}")
    print(f"   Всего вопросов в файле: {data.get('total', len(data.get('questions', [])))}")
    
    db = SessionLocal()
    
    try:
        # Получаем профессию DevOps (id=4)
        devops = db.query(Profession).filter(Profession.name == "DevOps").first()
        if not devops:
            print("❌ Профессия DevOps не найдена!")
            return
        
        print(f"✅ Профессия DevOps найдена (ID={devops.id})")
        
        # Считаем текущие вопросы
        current_count = db.query(Question).filter(Question.profession_id == devops.id).count()
        print(f"📊 Текущее количество вопросов DevOps: {current_count}")
        
        # Импортируем вопросы
        imported = 0
        skipped = 0
        
        for q_data in data.get('questions', []):
            # Проверяем что это вопрос по DevOps
            if q_data.get('profession_name', '').lower().find('devops') == -1 and q_data.get('profession_id') != 4:
                # Пропускаем не-DevOps вопросы
                continue
            
            # Проверяем дубликат по тексту
            existing = db.query(Question).filter(Question.text == q_data['text']).first()
            if existing:
                skipped += 1
                continue
            
            # Создаем вопрос
            question = Question(
                text=q_data['text'],
                question_type=q_data['question_type'],
                profession_id=devops.id,
                difficulty=q_data.get('difficulty', 'junior'),
                options=q_data['options'],
                correct_option=q_data.get('correct_option'),
                correct_order=q_data.get('correct_order'),
                explanation=q_data.get('explanation')
            )
            db.add(question)
            imported += 1
        
        db.commit()
        
        # Итоговая статистика
        final_count = db.query(Question).filter(Question.profession_id == devops.id).count()
        
        print(f"\n✅ Импорт завершен!")
        print(f"   📥 Импортировано: {imported} вопросов")
        print(f"   ⏭️  Пропущено (дубликаты): {skipped} вопросов")
        print(f"   📊 Всего вопросов DevOps: {final_count}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Ошибка импорта: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    # Пытаемся найти файл с вопросами
    backup_files = [
        os.path.join(project_dir, 'backups', 'questions_fixed_100_devops.json'),
        os.path.join(project_dir, 'scripts', 'questions_full_backup.json'),
        os.path.join(project_dir, 'scripts', 'questions_backup.json'),
    ]
    
    backup_file = None
    for f in backup_files:
        if os.path.exists(f):
            backup_file = f
            break
    
    if not backup_file:
        print("❌ Файл с бэкапом не найден!")
        print(f"Искал в: {backup_files}")
        sys.exit(1)
    
    print(f"📁 Найден файл: {backup_file}")
    import_questions(backup_file)
