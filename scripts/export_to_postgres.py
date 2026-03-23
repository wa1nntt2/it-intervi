#!/usr/bin/env python3
"""
Скрипт для экспорта данных из SQLite в JSON формат для последующего импорта в PostgreSQL.

Использование:
    python export_to_postgres.py

Создает файл backup_data.json со всеми данными из базы данных.
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Добавляем родительскую директорию в path для импортов
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import text
from app.database.engine import SessionLocal, engine, DATABASE_URL

# Таблицы для экспорта (в порядке зависимости)
TABLES = [
    'users',
    'professions',
    'categories',
    'questions',
    'question_categories',
    'ordering_items',
    'achievements',
    'sessions',
    'answers',
    'user_progress',
    'user_achievements',
    'interview_configs',
    'category_configs',
]


def export_data():
    """Экспорт всех данных из SQLite в JSON"""
    
    print("=" * 60)
    print("📦 Экспорт данных из SQLite")
    print("=" * 60)
    print(f"📍 База данных: {DATABASE_URL}")
    print()
    
    # Проверка что это SQLite
    if not DATABASE_URL.startswith("sqlite"):
        print("❌ Ошибка: Этот скрипт предназначен только для SQLite!")
        print(f"   Текущая БД: {DATABASE_URL}")
        return False
    
    db = SessionLocal()
    export_data = {
        'exported_at': datetime.utcnow().isoformat(),
        'database': DATABASE_URL,
        'tables': {}
    }
    
    try:
        for table in TABLES:
            print(f"📋 Экспорт таблицы: {table}...")
            
            try:
                # Проверяем существование таблицы
                result = db.execute(text(f"SELECT COUNT(*) FROM {table}"))
                count = result.scalar()
                
                # Получаем все данные
                result = db.execute(text(f"SELECT * FROM {table}"))
                columns = result.keys()
                rows = result.fetchall()
                
                # Конвертируем в список словарей
                rows_list = []
                for row in rows:
                    row_dict = {}
                    for i, col in enumerate(columns):
                        value = row[i]
                        # Конвертируем datetime в строку
                        if isinstance(value, datetime):
                            value = value.isoformat()
                        row_dict[col] = value
                    rows_list.append(row_dict)
                
                export_data['tables'][table] = {
                    'count': count,
                    'columns': list(columns),
                    'data': rows_list
                }
                
                print(f"   ✓ {count} записей экспортировано")
                
            except Exception as e:
                print(f"   ⊘ Таблица не найдена или ошибка: {e}")
                export_data['tables'][table] = {
                    'count': 0,
                    'columns': [],
                    'data': [],
                    'error': str(e)
                }
        
        # Сохраняем в файл
        output_file = Path(__file__).parent / 'backup_data.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2, default=str)
        
        print()
        print("=" * 60)
        print(f"✅ Экспорт завершен!")
        print(f"📁 Файл сохранен: {output_file.absolute()}")
        print("=" * 60)
        
        # Статистика
        total_records = sum(t.get('count', 0) for t in export_data['tables'].values())
        print(f"📊 Всего записей: {total_records}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка экспорта: {e}")
        return False
        
    finally:
        db.close()


if __name__ == "__main__":
    success = export_data()
    sys.exit(0 if success else 1)
