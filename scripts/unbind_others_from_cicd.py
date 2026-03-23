#!/usr/bin/env python3
"""
Отвязать вопросы Linux, Сети и Docker от категории CI/CD.
"""

import sys
import os

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
backend_dir = os.path.join(project_dir, 'backend')
sys.path.insert(0, backend_dir)
os.chdir(backend_dir)

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

try:
    # Находим категории
    linux_result = db.execute(
        text("SELECT id FROM categories WHERE name = 'Linux' AND profession_id = 4")
    ).first()
    network_result = db.execute(
        text("SELECT id FROM categories WHERE name = 'Сети' AND profession_id = 4")
    ).first()
    docker_result = db.execute(
        text("SELECT id FROM categories WHERE name = 'Docker' AND profession_id = 4")
    ).first()
    cicd_result = db.execute(
        text("SELECT id FROM categories WHERE name = 'CI/CD' AND profession_id = 4")
    ).first()
    
    if not all([linux_result, network_result, docker_result, cicd_result]):
        print("❌ Категории не найдены!")
        sys.exit(1)
    
    linux_cat_id = linux_result[0]
    network_cat_id = network_result[0]
    docker_cat_id = docker_result[0]
    cicd_cat_id = cicd_result[0]
    print(f"✅ Linux ID={linux_cat_id}, Сети ID={network_cat_id}, Docker ID={docker_cat_id}, CI/CD ID={cicd_cat_id}")
    
    # Вопросы Linux (ID 448-507) - отвязать от CI/CD
    linux_question_ids = list(range(448, 508))
    unbound_linux = 0
    for q_id in linux_question_ids:
        result = db.execute(
            text("DELETE FROM question_categories WHERE question_id = :qid AND category_id = :cid"),
            {"qid": q_id, "cid": cicd_cat_id}
        )
        if result.rowcount > 0:
            unbound_linux += 1
    
    # Вопросы Сети (ID 508-567) - отвязать от CI/CD
    network_question_ids = list(range(508, 568))
    unbound_network = 0
    for q_id in network_question_ids:
        result = db.execute(
            text("DELETE FROM question_categories WHERE question_id = :qid AND category_id = :cid"),
            {"qid": q_id, "cid": cicd_cat_id}
        )
        if result.rowcount > 0:
            unbound_network += 1
    
    # Вопросы Docker (ID 568-624) - отвязать от CI/CD
    docker_question_ids = list(range(568, 625))
    unbound_docker = 0
    for q_id in docker_question_ids:
        result = db.execute(
            text("DELETE FROM question_categories WHERE question_id = :qid AND category_id = :cid"),
            {"qid": q_id, "cid": cicd_cat_id}
        )
        if result.rowcount > 0:
            unbound_docker += 1
    
    db.commit()
    
    print(f"✅ Отвязано {unbound_linux} вопросов Linux от CI/CD")
    print(f"✅ Отвязано {unbound_network} вопросов Сети от CI/CD")
    print(f"✅ Отвязано {unbound_docker} вопросов Docker от CI/CD")
    
    # Финальная статистика
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
