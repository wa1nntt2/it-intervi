#!/usr/bin/env python3
"""
Скрипт для категоризации вопросов DevOps по темам.
Запуск: docker exec -w /app it-interview-backend python3 /app/scripts/categorize_devops_questions.py
"""

import re
from app.database.engine import SessionLocal
from app.models.category import Category
from app.models.question import Question
from app.models.category import question_categories

# Категории для DevOps вопросов с ключевыми словами
CATEGORIES = {
    "Linux": {
        "description": "Команды Linux, файловая система, процессы, пользователи, права доступа",
        "keywords": [
            "linux", "команда", "файл", "процесс", "пользователь", "каталог", "директория",
            "chmod", "chown", "ps", "top", "grep", "tail", "head", "cat", "ls", "df", "du",
            "/var", "/home", "/etc", "sudo", "su ", "bash", "shell", "скрипт", "исполняемый",
            "whoami", "ping", "env", "переменные окружения", "лог", "journalctl", "systemd"
        ]
    },
    "Docker": {
        "description": "Контейнеризация, Docker команды, Dockerfile, образы, контейнеры",
        "keywords": [
            "docker", "контейнер", "образ", "image", "container", "dockerfile", "docker-compose",
            "docker run", "docker build", "docker ps", "docker exec", "docker stop", "docker rm",
            "том", "volume", "сеть", "network", "порт", "маппинг", "слой", "layer"
        ]
    },
    "CI/CD": {
        "description": "Непрерывная интеграция и доставка, Jenkins, GitLab CI, GitHub Actions",
        "keywords": [
            "ci/cd", "pipeline", "jenkins", "gitlab ci", "github actions", "непрерывная интеграция",
            "непрерывная доставка", "непрерывное развертывание", "сборка", "build", "deploy",
            "артефакт", "stage", "этап", "workflow", "runner", "job", "триггер"
        ]
    },
    "Kubernetes": {
        "description": "Оркестрация контейнеров, K8s, pods, deployments, services",
        "keywords": [
            "kubernetes", "k8s", "pod", "deployment", "service", "replica", "node", "cluster",
            "namespace", "configmap", "secret", "ingress", "helm", "chart", "kubectl",
            "оркестрация", "оркестровки", "orchestration"
        ]
    },
    "Infrastructure as Code": {
        "description": "Terraform, Ansible, CloudFormation, автоматизация инфраструктуры",
        "keywords": [
            "terraform", "ansible", "cloudformation", "puppet", "chef", "iac", "инфраструктура как код",
            "infrastructure as code", "provisioning", "конфигурация", "playbook", "manifest",
            "resource", "state", "план", "apply"
        ]
    },
    "Monitoring": {
        "description": "Мониторинг, логирование, Prometheus, Grafana, ELK Stack",
        "keywords": [
            "monitoring", "мониторинг", "prometheus", "grafana", "elk", "elastic", "logstash",
            "kibana", "alert", "алерт", "уведомление", "метрика", "metric", "dashboard",
            "логирование", "logging", "trace", "tracing", "jaeger", "zipkin"
        ]
    },
    "Network": {
        "description": "Сети, TCP/IP, DNS, HTTP/HTTPS, балансировка нагрузки",
        "keywords": [
            "network", "сеть", "tcp", "ip", "dns", "http", "https", "ssl", "tls", "port", "порт",
            "балансировка", "load balancer", "nginx", "haproxy", "firewall", "iptables",
            "subnet", "маска", "gateway", "route", "osi", "уровень", "пакет", "сокет"
        ]
    },
    "Security": {
        "description": "Безопасность, RBAC, секреты, шифрование, аутентификация",
        "keywords": [
            "security", "безопасность", "rbac", "role", "secret", "секрет", "шифрование",
            "encryption", "authentication", "аутентификация", "authorization", "авторизация",
            "certificate", "сертификат", "token", "токен", "vault", "hash", "хеш"
        ]
    },
    "Cloud": {
        "description": "Облачные платформы: AWS, Azure, GCP",
        "keywords": [
            "cloud", "облако", "aws", "azure", "gcp", "google cloud", "ec2", "s3", "lambda",
            "cloudwatch", "iam", "vpc", "instance", "регион", "зона доступности"
        ]
    },
    "Git": {
        "description": "Система контроля версий Git, ветвление, слияние",
        "keywords": [
            "git", "repository", "репозиторий", "commit", "коммит", "branch", "ветка",
            "merge", "слияние", "pull request", "push", "fetch", "clone", "checkout",
            "rebase", "conflict", "конфликт", "remote", "origin", "tag"
        ]
    },
    "DevOps Culture": {
        "description": "Культура DevOps, Agile, сотрудничество, автоматизация",
        "keywords": [
            "devops", "культура", "culture", "collaboration", "сотрудничество", "agile",
            "scrum", "kanban", "automation", "автоматизация", "процесс", "методология",
            "команда", "разработка", "эксплуатация", "ops", "dev"
        ]
    }
}


def categorize_question(text: str, explanation: str = "") -> list:
    """
    Определить категории для вопроса по ключевым словам.
    Возвращает список названий категорий.
    """
    text_lower = (text + " " + explanation).lower()
    matched_categories = []
    
    for category_name, category_data in CATEGORIES.items():
        for keyword in category_data["keywords"]:
            if keyword.lower() in text_lower:
                matched_categories.append(category_name)
                break  # Достаточно одного совпадения для категории
    
    # Если ничего не найдено, назначаем общую категорию
    if not matched_categories:
        matched_categories.append("DevOps Culture")
    
    return matched_categories


def add_categories_and_assign():
    """Добавить категории и привязать их к вопросам"""
    
    db = SessionLocal()
    
    try:
        # Создаем категории
        categories_map = {}
        for category_name, category_data in CATEGORIES.items():
            cat = db.query(Category).filter(Category.name == category_name).first()
            if not cat:
                cat = Category(
                    name=category_name,
                    description=category_data["description"],
                    profession_id=4  # DevOps
                )
                db.add(cat)
                db.commit()
                db.refresh(cat)
                print(f"✅ Создана категория: {category_name}")
            else:
                print(f"✓ Категория существует: {category_name}")
            categories_map[category_name] = cat.id
        
        # Получаем все вопросы DevOps
        devops_questions = db.query(Question).filter(Question.profession_id == 4).all()
        print(f"\n📊 Всего вопросов DevOps: {len(devops_questions)}")
        
        # Категоризируем каждый вопрос
        categorized_count = 0
        for question in devops_questions:
            categories = categorize_question(question.text, question.explanation or "")
            
            # Привязываем категории к вопросу
            for cat_name in categories:
                cat_id = categories_map[cat_name]
                
                # Проверяем есть ли уже связь
                existing = db.query(question_categories).filter(
                    question_categories.c.question_id == question.id,
                    question_categories.c.category_id == cat_id
                ).first()
                
                if not existing:
                    db.execute(
                        question_categories.insert().values(
                            question_id=question.id,
                            category_id=cat_id
                        )
                    )
                    categorized_count += 1
        
        db.commit()
        
        # Статистика
        print(f"\n✅ Категоризация завершена!")
        print(f"   Добавлено связей вопрос-категория: {categorized_count}")
        
        # Показываем распределение по категориям
        print("\n📊 Распределение вопросов по категориям:")
        for cat_name, cat_id in categories_map.items():
            count = db.query(question_categories).filter(
                question_categories.c.category_id == cat_id
            ).count()
            if count > 0:
                print(f"   {cat_name}: {count} вопросов")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Ошибка: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    add_categories_and_assign()
