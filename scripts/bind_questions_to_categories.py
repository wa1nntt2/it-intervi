#!/usr/bin/env python3
"""
Скрипт для привязки вопросов к категориям.
Автоматически распределяет вопросы по категориям на основе ключевых слов.
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
from app.models.question import Question
from app.models.category import Category

# Создаем движок и сессию
engine = create_engine('sqlite:///./interview_trainer.db')
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

try:
    print("🔄 Привязка вопросов к категориям...")
    print("=" * 50)

    # Получаем все категории DevOps
    devops_categories = db.query(Category).filter(Category.profession_id == 4).all()
    print(f'Найдено категорий DevOps: {len(devops_categories)}')
    
    categories_map = {c.name.lower(): c.id for c in devops_categories}
    print(f'Категории: {list(categories_map.keys())}')

    # Получаем все вопросы DevOps
    devops_questions = db.query(Question).filter(Question.profession_id == 4).all()
    print(f'Вопросов DevOps: {len(devops_questions)}')

    # Ключевые слова для каждой категории
    category_keywords = {
        'linux': ['linux', 'команда', 'терминал', 'bash', 'shell', 'chmod', 'grep', 'find', 'top', 'ps aux', 'df -h', 'du -sh', 'tail -f', 'cat ', 'ssh', 'useradd', 'ping', 'dev/null', 'whoami', 'head ', 'stdin', 'stdout', 'stderr', 'symlink', 'kill', 'env', 'printenv', 'variable', 'окружени'],
        'docker': ['docker', 'контейнер', 'image', 'dockerfile', 'docker build', 'docker run', 'docker exec', 'docker push', 'docker pull', 'volume', 'network', 'cmd', 'entrypoint', 'docker-compose'],
        'kubernetes': ['kubernetes', 'k8s', 'pod', 'deployment', 'service', 'ingress', 'kubelet', 'kubectl', 'namespace', 'statefulset', 'daemonset', 'configmap', 'secret'],
        'ci/cd': ['ci/cd', 'pipeline', 'continuous integration', 'continuous delivery', 'continuous deployment', 'gitlab ci', 'github actions', 'jenkins', 'build', 'deploy', 'release'],
        'сети': ['сеть', 'tcp', 'udp', 'ip', 'dns', 'http', 'https', 'ssl', 'tls', 'порт', 'icmp', 'nat', 'mtu', 'маска подсети', 'osi', 'прокси', 'load balancer', 'ftp', 'smtp'],
        'monitoring': ['мониторинг', 'prometheus', 'grafana', 'alert', 'алерт', 'метрики', 'логи', 'logging', 'elk', 'elastic', 'logstash', 'kibana', 'наблюдаемость'],
        'iac': ['iac', 'infrastructure as code', 'terraform', 'ansible', 'puppet', 'chef', 'cloudformation', 'state']
    }

    # Привязываем вопросы к категориям
    bound_count = 0
    for question in devops_questions:
        text_lower = question.text.lower()
        
        for cat_name, keywords in category_keywords.items():
            cat_id = categories_map.get(cat_name)
            if not cat_id:
                continue
            
            for keyword in keywords:
                if keyword in text_lower:
                    # Проверяем, не привязана ли уже категория
                    existing = db.execute(text(
                        'SELECT 1 FROM question_categories WHERE question_id = :qid AND category_id = :cid'
                    ), {'qid': question.id, 'cid': cat_id}).first()
                    
                    if not existing:
                        # Привязываем категорию
                        category = db.query(Category).get(cat_id)
                        question.categories.append(category)
                        bound_count += 1
                    break
    
    db.commit()
    
    # Считаем результат
    result = db.execute(text('''
        SELECT c.name, COUNT(qc.question_id) as count
        FROM categories c
        LEFT JOIN question_categories qc ON c.id = qc.category_id
        WHERE c.profession_id = 4
        GROUP BY c.id, c.name
    '''))
    
    print("\n" + "=" * 50)
    print("📊 Итоги:")
    for row in result:
        print(f"   {row[0]}: {row[1]} вопросов")
    
    total = db.execute(text('SELECT COUNT(DISTINCT question_id) FROM question_categories qc JOIN categories c ON qc.category_id = c.id WHERE c.profession_id = 4')).scalar()
    print(f"\n✅ Всего вопросов с категориями: {total}")
    print("=" * 50)

except Exception as e:
    db.rollback()
    print(f"\n❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
finally:
    db.close()
