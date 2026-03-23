#!/usr/bin/env python3
"""
Скрипт для импорта данных из JSON в PostgreSQL.

Использование:
    python import_from_json.py backup_data.json

Перед импортом убедитесь:
1. PostgreSQL запущен и доступен
2. База данных создана
3. Миграции Alembic применены
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Добавляем родительскую директорию в path для импортов
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import text
from app.database.engine import SessionLocal, engine, DATABASE_URL

# Таблицы для импорта (в порядке зависимости)
TABLES_ORDER = [
    'users',
    'professions',
    'categories',
    'achievements',
    'interview_configs',
    'questions',
    'question_categories',
    'ordering_items',
    'category_configs',
    'sessions',
    'answers',
    'user_progress',
    'user_achievements',
]


def import_data(input_file: str):
    """Импорт данных из JSON в базу данных"""
    
    print("=" * 60)
    print("📥 Импорт данных в базу данных")
    print("=" * 60)
    print(f"📍 База данных: {DATABASE_URL}")
    print(f"📁 Файл: {input_file}")
    print()
    
    # Проверка что файл существует
    input_path = Path(input_file)
    if not input_path.exists():
        print(f"❌ Ошибка: Файл не найден: {input_file}")
        return False
    
    # Загружаем данные
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✅ Данные загружены ({len(data.get('tables', {}))} таблиц)")
    except Exception as e:
        print(f"❌ Ошибка загрузки JSON: {e}")
        return False
    
    db = SessionLocal()
    
    try:
        # Отключаем foreign key проверки на время импорта
        if DATABASE_URL.startswith("postgresql"):
            db.execute(text("SET CONSTRAINTS ALL DEFERRED"))
        
        total_imported = 0
        
        for table in TABLES_ORDER:
            if table not in data.get('tables', {}):
                print(f"⊘ Таблица {table} не найдена в файле, пропускаем")
                continue
            
            table_data = data['tables'][table]
            if table_data.get('error'):
                print(f"⊘ Таблица {table} имела ошибку при экспорте, пропускаем")
                continue
            
            count = table_data.get('count', 0)
            if count == 0:
                print(f"⊘ Таблица {table} пуста, пропускаем")
                continue
            
            print(f"📋 Импорт таблицы: {table} ({count} записей)...")
            
            try:
                # Получаем колонки
                columns = table_data.get('columns', [])
                if not columns:
                    print(f"   ⊘ Нет колонок для {table}, пропускаем")
                    continue
                
                # Формируем SQL для вставки
                placeholders = ', '.join([f':{col}' for col in columns])
                columns_str = ', '.join(columns)
                
                # Проверяем существование таблицы
                result = db.execute(text(f"SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = '{table}')"))
                exists = result.scalar()
                
                if not exists:
                    print(f"   ⊘ Таблица не существует, пропускаем")
                    continue
                
                # Вставляем данные
                imported = 0
                for row in table_data.get('data', []):
                    try:
                        # Конвертируем пустые строки в None
                        clean_row = {k: (v if v != '' else None) for k, v in row.items()}
                        
                        # Пропускаем id для auto-increment полей
                        if 'id' in clean_row:
                            del clean_row['id']
                        
                        # Для PostgreSQL нужно явно указать columns в VALUES
                        values_placeholders = ', '.join([f':{col}' for col in clean_row.keys()])
                        columns_for_insert = ', '.join(clean_row.keys())
                        
                        insert_sql = text(f"""
                            INSERT INTO {table} ({columns_for_insert}) 
                            VALUES ({values_placeholders})
                        """)
                        
                        db.execute(insert_sql, clean_row)
                        imported += 1
                        
                    except Exception as e:
                        # Игнорируем дубликаты и другие ошибки
                        pass
                
                db.commit()
                print(f"   ✓ Импортировано {imported} записей")
                total_imported += imported
                
            except Exception as e:
                print(f"   ❌ Ошибка импорта {table}: {e}")
                db.rollback()
        
        print()
        print("=" * 60)
        print(f"✅ Импорт завершен!")
        print(f"📊 Всего импортировано: {total_imported} записей")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка импорта: {e}")
        db.rollback()
        return False
        
    finally:
        db.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python import_from_json.py <файл.json>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    success = import_data(input_file)
    sys.exit(0 if success else 1)
