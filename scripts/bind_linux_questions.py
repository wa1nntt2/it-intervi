#!/usr/bin/env python3
"""
Привязка вопросов Linux к категории "Linux".
Вопросы должны быть уже импортированы в базу данных.
"""

import sys
import os

# Добавляем backend в path
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
backend_dir = os.path.join(project_dir, 'backend')
sys.path.insert(0, backend_dir)
os.chdir(backend_dir)

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Создаем движок и сессию для PostgreSQL
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

try:
    # Находим категорию "Linux" для DevOps (profession_id=4)
    result = db.execute(
        text("SELECT id FROM categories WHERE name = 'Linux' AND profession_id = 4")
    ).first()
    
    if not result:
        print("❌ Категория 'Linux' для DevOps не найдена!")
        sys.exit(1)
    
    category_id = result[0]
    print(f"✅ Категория 'Linux' найдена (ID={category_id})")
    
    # Находим все вопросы DevOps с темой Linux (по ключевым словам в тексте)
    linux_keywords = [
        'cd ', 'ls ', 'pwd', 'echo ', 'touch ', 'mkdir ', 'rm ',
        'cat ', 'cp ', 'mv ', 'chmod ', 'chown ', 'grep ', 'find ',
        'ps ', 'kill ', 'ps aux', 'top ', 'htop ', 'tail ', 'head ',
        'man ', 'history', 'whoami', 'env ', 'tar ', 'lsof ',
        'cron', 'crontab', 'systemd', 'systemctl', 'iptables',
        'strace', 'cgroups', 'RAID', 'mdadm', 'rsyslog', 'SELinux',
        'netstat', 'ss ', 'TCP', 'SYN', 'ACK', 'bridge', 'ip link',
        'openssl', 'SSL', 'inode', 'hard link', 'soft link',
        'nohup', 'screen', 'tmux', 'sudo', 'su ', 'GRUB', 'kernel',
        'gdb', 'core dump', 'ldd', 'which ', 'whereis', 'ping ',
        'netcat', 'nc ', 'usermod', '/etc/', '/var/', '/proc/',
        'pipe', '|', 'permission denied', 'SIGTERM', 'SIGKILL',
        'SSH ключ', 'ssh ', '/dev/', 'lsof -p'
    ]
    
    # Ищем вопросы по ключевым словам
    conditions = []
    params = {}
    for i, keyword in enumerate(linux_keywords):
        param_name = f'kw{i}'
        conditions.append(f"text ILIKE :{param_name}")
        params[param_name] = f'%{keyword}%'
    
    where_clause = ' OR '.join(conditions)
    query = text(f"""
        SELECT id, text, profession_id 
        FROM questions 
        WHERE profession_id = 4 AND ({where_clause})
    """)
    
    result = db.execute(query, params).fetchall()
    question_ids = [row[0] for row in result]
    
    print(f"📚 Найдено {len(question_ids)} вопросов по Linux")
    
    if not question_ids:
        print("⚠️  Вопросы не найдены. Убедитесь, что вопросы импортированы.")
        sys.exit(0)
    
    # Привязываем вопросы к категории
    bound_count = 0
    for q_id in question_ids:
        # Проверяем, не привязана ли уже категория
        existing = db.execute(
            text("SELECT 1 FROM question_categories WHERE question_id = :qid AND category_id = :cid"),
            {"qid": q_id, "cid": category_id}
        ).first()
        
        if not existing:
            db.execute(
                text("INSERT INTO question_categories (question_id, category_id) VALUES (:qid, :cid)"),
                {"qid": q_id, "cid": category_id}
            )
            bound_count += 1
    
    db.commit()
    
    print(f"✅ Привязано {bound_count} вопросов к категории 'Linux'")
    
    # Выводим статистику
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
