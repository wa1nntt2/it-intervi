#!/usr/bin/env python3
"""
Скрипт для автоматической привязки вопросов к категориям на основе анализа текста.
"""

import sys
import os
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
backend_dir = os.path.join(project_dir, 'backend')
sys.path.insert(0, backend_dir)
os.chdir(backend_dir)

from sqlalchemy import create_engine, text
from app.models.question import Question
from app.models.category import Category

engine = create_engine('sqlite:///./interview_trainer.db')
conn = engine.connect()

print("🔄 Анализ и привязка вопросов к категориям...")
print("=" * 60)

# Получаем все категории DevOps
devops_categories = conn.execute(text("""
    SELECT id, name FROM categories WHERE profession_id = 4
""")).fetchall()

categories_map = {name.lower(): id for id, name in devops_categories}
print(f"Найдено категорий DevOps: {len(categories_map)}")
print(f"Категории: {list(categories_map.keys())}\n")

# Ключевые слова для каждой категории
category_keywords = {
    'linux': [
        'linux', 'команда', 'терминал', 'bash', 'shell', 'chmod', 'grep', 'find',
        'top', 'ps aux', 'df -h', 'du -sh', 'tail -f', 'cat ', 'ssh', 'useradd',
        'ping', 'dev/null', 'whoami', 'head ', 'stdin', 'stdout', 'stderr',
        'symlink', 'kill', 'env', 'printenv', 'variable', 'окружени', 'ls ',
        'man ', 'cd ', 'pwd', 'mkdir', 'rm ', 'cp ', 'mv ', 'touch', 'nano',
        'vim', 'less', 'more', 'tar', 'gzip', 'curl', 'wget', 'pipe', 'redirection'
    ],
    'docker': [
        'docker', 'контейнер', 'image', 'dockerfile', 'docker build', 'docker run',
        'docker exec', 'docker push', 'docker pull', 'volume', 'network', 'cmd',
        'entrypoint', 'docker-compose', 'dockerfile', 'layer', 'registry', 'hub'
    ],
    'kubernetes': [
        'kubernetes', 'k8s', 'pod', 'deployment', 'service', 'ingress', 'kubelet',
        'kubectl', 'namespace', 'statefulset', 'daemonset', 'configmap', 'secret',
        'replicaset', 'hpa', 'vpa', 'node', 'cluster', 'etcd', 'kube-proxy'
    ],
    'ci/cd': [
        'ci/cd', 'pipeline', 'continuous integration', 'continuous delivery',
        'continuous deployment', 'gitlab ci', 'github actions', 'jenkins', 'build',
        'deploy', 'release', 'artifact', 'runner', 'workflow', 'stage', 'job'
    ],
    'сети': [
        'сеть', 'tcp', 'udp', 'ip', 'dns', 'http', 'https', 'ssl', 'tls', 'порт',
        'icmp', 'nat', 'mtu', 'маска подсети', 'osi', 'прокси', 'load balancer',
        'ftp', 'smtp', 'ssh', 'vpn', 'firewall', 'subnet', 'gateway', 'routing',
        'lb', 'оси модель', 'уровн', 'браузер'
    ],
    'monitoring': [
        'мониторинг', 'prometheus', 'grafana', 'alert', 'алерт', 'метрики', 'логи',
        'logging', 'elk', 'elastic', 'logstash', 'kibana', 'наблюдаемость',
        'observability', 'uptime', 'latency', 'throughput', 'dashboard'
    ],
    'iac': [
        'iac', 'infrastructure as code', 'terraform', 'ansible', 'puppet', 'chef',
        'cloudformation', 'state', 'playbook', 'role', 'module', 'provisioner',
        'vault', 'consul', 'packer'
    ],
    'other': [
        'devops', 'культура', 'философия', 'цель', 'automation', 'automat',
        'коллаборация', 'сотрудничество', 'agile', 'scrum', 'lean', 'calms',
        'shift left', 'security', 'безопасн', 'best practice', 'лучш практик'
    ]
}

# Получаем все вопросы DevOps
devops_questions = conn.execute(text("""
    SELECT id, text FROM questions WHERE profession_id = 4
""")).fetchall()

print(f"Вопросов DevOps для анализа: {len(devops_questions)}\n")

# Привязываем вопросы к категориям
bound_count = 0
not_bound = []

for q_id, q_text in devops_questions:
    text_lower = q_text.lower()
    matched_categories = []
    
    for cat_name, keywords in category_keywords.items():
        cat_id = categories_map.get(cat_name)
        if not cat_id:
            continue
        
        for keyword in keywords:
            if keyword in text_lower:
                matched_categories.append((cat_name, cat_id))
                break
    
    if matched_categories:
        # Привязываем к первой найденной категории
        primary_cat = matched_categories[0][1]
        
        # Проверяем, не привязана ли уже категория
        existing = conn.execute(text("""
            SELECT 1 FROM question_categories 
            WHERE question_id = :qid AND category_id = :cid
        """), {'qid': q_id, 'cid': primary_cat}).first()
        
        if not existing:
            conn.execute(text("""
                INSERT INTO question_categories (question_id, category_id)
                VALUES (:qid, :cid)
            """), {'qid': q_id, 'cid': primary_cat})
            bound_count += 1
    else:
        not_bound.append((q_id, q_text[:60]))

conn.commit()

# Выводим статистику
result = conn.execute(text("""
    SELECT c.name, COUNT(qc.question_id) as count
    FROM categories c
    LEFT JOIN question_categories qc ON c.id = qc.category_id
    WHERE c.profession_id = 4
    GROUP BY c.id, c.name
    ORDER BY count DESC
"""))

print("=" * 60)
print("📊 Статистика привязки:")
for row in result:
    print(f"   {row[0]}: {row[1]} вопросов")

total = conn.execute(text("""
    SELECT COUNT(DISTINCT question_id) FROM question_categories qc
    JOIN categories c ON qc.category_id = c.id
    WHERE c.profession_id = 4
""")).scalar()

print(f"\n✅ Всего вопросов с категориями: {total} из {len(devops_questions)}")

if not_bound:
    print(f"\n⚠️  Не привязано вопросов: {len(not_bound)}")
    print("Вопросы без категорий:")
    for q_id, q_text in not_bound[:10]:
        print(f"   ID {q_id}: {q_text}...")
    if len(not_bound) > 10:
        print(f"   ... и ещё {len(not_bound) - 10}")

print("=" * 60)
print("🎉 Готово!")
