#!/usr/bin/env python3
"""
Скрипт для импорта вопросов DevOps из JSON внутри контейнера.
"""

import json
from app.database.engine import SessionLocal
from app.models.profession import Profession
from app.models.question import Question

def import_questions():
    """Импорт вопросов из JSON файла"""
    
    # Читаем бэкап
    with open('/tmp/devops_questions.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"📦 Загрузка вопросов...")
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
            prof_name = q_data.get('profession_name', '').lower()
            prof_id = q_data.get('profession_id')
            
            # Импортируем только DevOps вопросы (profession_id=4 или имя содержит devops)
            if prof_id != 4 and 'devops' not in prof_name:
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
    import_questions()
