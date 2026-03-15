# Seed данные для базы данных
# Создаются при первом запуске приложения

import json
import os
from sqlalchemy.orm import Session
from app.models.profession import Profession
from app.models.question import Question
from app.models.user import User
from app.core.security import get_password_hash


def load_devops_questions():
    """Загрузка вопросов DevOps из JSON файла"""
    # Пытаемся найти файл с вопросами в нескольких местах
    possible_paths = [
        '/app/backups/questions_fixed_100_devops.json',
        '/app/scripts/questions_fixed_100_devops.json',
        '/tmp/devops_questions.json',
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data.get('questions', [])
    
    return []


def seed_database(db: Session) -> None:
    """
    Сидирование базы данных начальными данными.
    Создает профессии, тестового пользователя и вопросы.

    Args:
        db: Сессия SQLAlchemy для работы с БД
    """
    # Проверяем есть ли уже профессии
    existing_professions = db.query(Profession).count()
    if existing_professions > 0:
        # Профессии уже есть, проверяем есть ли вопросы DevOps
        devops = db.query(Profession).filter(Profession.name == "DevOps").first()
        if devops:
            devops_questions = db.query(Question).filter(Question.profession_id == devops.id).count()
            if devops_questions >= 50:
                return  # Уже есть достаточно вопросов
    
    # Создаем профессии если их нет
    professions_data = [
        {"name": "Frontend", "description": "Разработка клиентской части веб-приложений (HTML, CSS, JavaScript, React, Vue, Angular)"},
        {"name": "Backend", "description": "Разработка серверной части веб-приложений (Python, Java, Node.js, базы данных, API)"},
        {"name": "Fullstack", "description": "Универсальная разработка веб-приложений (Frontend + Backend)"},
        {"name": "DevOps", "description": "Автоматизация развертывания, CI/CD, контейнеризация, мониторинг (Docker, Kubernetes, Jenkins)"},
    ]
    
    professions = {}
    for prof_data in professions_data:
        prof = db.query(Profession).filter(Profession.name == prof_data["name"]).first()
        if not prof:
            prof = Profession(**prof_data)
            db.add(prof)
            db.commit()
            db.refresh(prof)
        professions[prof_data["name"]] = prof
    
    # Создаем тестового пользователя с правами администратора
    admin = db.query(User).filter(User.email == "admin@example.com").first()
    if not admin:
        admin = User(
            email="admin@example.com",
            hashed_password=get_password_hash("admin123"),
            is_admin=True
        )
        db.add(admin)
        db.commit()
        print("✅ Создан тестовый пользователь: admin@example.com / admin123")
    
    # Загружаем вопросы DevOps из файла
    devops_questions_data = load_devops_questions()
    
    if devops_questions_data and professions.get("DevOps"):
        devops_prof = professions["DevOps"]
        imported = 0
        
        for q_data in devops_questions_data:
            # Проверяем что это вопрос по DevOps
            if q_data.get('profession_id') != 4:
                continue
            
            # Проверяем дубликат
            existing = db.query(Question).filter(Question.text == q_data['text']).first()
            if existing:
                continue
            
            question = Question(
                text=q_data['text'],
                question_type=q_data['question_type'],
                profession_id=devops_prof.id,
                difficulty=q_data.get('difficulty', 'junior'),
                options=q_data['options'],
                correct_option=q_data.get('correct_option'),
                correct_order=q_data.get('correct_order'),
                explanation=q_data.get('explanation')
            )
            db.add(question)
            imported += 1
        
        if imported > 0:
            db.commit()
            print(f"✅ Импортировано {imported} вопросов DevOps")
    
    # Создаем базовые вопросы для Frontend если их мало
    frontend_prof = professions.get("Frontend")
    if frontend_prof:
        frontend_count = db.query(Question).filter(Question.profession_id == frontend_prof.id).count()
        if frontend_count < 3:
            frontend_questions = [
                Question(
                    text="Что такое Virtual DOM в React?",
                    question_type="mcq",
                    profession_id=frontend_prof.id,
                    difficulty="junior",
                    options=[
                        "Прямая копия реального DOM",
                        "Легковесная копия DOM в памяти, используемая для оптимизации",
                        "Способ создания DOM элементов",
                        "Библиотека для работы с DOM"
                    ],
                    correct_option=1,
                    explanation="Virtual DOM - это легковесная копия реального DOM, которая хранится в памяти и используется React для оптимизации обновлений."
                ),
                Question(
                    text="Какой хук React используется для управления состоянием в функциональном компоненте?",
                    question_type="mcq",
                    profession_id=frontend_prof.id,
                    difficulty="junior",
                    options=["useEffect", "useState", "useContext", "useReducer"],
                    correct_option=1,
                    explanation="useState - это хук для управления локальным состоянием в функциональных компонентах React."
                ),
            ]
            db.add_all(frontend_questions)
            db.commit()
    
    # Создаем базовые вопросы для Backend если их мало
    backend_prof = professions.get("Backend")
    if backend_prof:
        backend_count = db.query(Question).filter(Question.profession_id == backend_prof.id).count()
        if backend_count < 3:
            backend_questions = [
                Question(
                    text="Что такое REST API?",
                    question_type="mcq",
                    profession_id=backend_prof.id,
                    difficulty="junior",
                    options=[
                        "Протокол передачи данных",
                        "Архитектурный стиль проектирования веб-сервисов",
                        "Язык программирования",
                        "База данных"
                    ],
                    correct_option=1,
                    explanation="REST (Representational State Transfer) - это архитектурный стиль для проектирования распределенных систем."
                ),
                Question(
                    text="Какой метод HTTP используется для обновления ресурса?",
                    question_type="mcq",
                    profession_id=backend_prof.id,
                    difficulty="junior",
                    options=["GET и POST", "PUT и PATCH", "DELETE", "OPTIONS"],
                    correct_option=1,
                    explanation="PUT используется для полной замены ресурса, PATCH - для частичного обновления."
                ),
            ]
            db.add_all(backend_questions)
            db.commit()
    
    # Создаем базовые вопросы для Fullstack если их мало
    fullstack_prof = professions.get("Fullstack")
    if fullstack_prof:
        fullstack_count = db.query(Question).filter(Question.profession_id == fullstack_prof.id).count()
        if fullstack_count < 2:
            fullstack_questions = [
                Question(
                    text="Что такое CORS?",
                    question_type="mcq",
                    profession_id=fullstack_prof.id,
                    difficulty="junior",
                    options=[
                        "Система управления версиями",
                        "Механизм безопасности браузеров для контроля доступа между источниками",
                        "Протокол передачи файлов",
                        "Язык разметки"
                    ],
                    correct_option=1,
                    explanation="CORS (Cross-Origin Resource Sharing) - механизм безопасности браузеров для контроля доступа между разными источниками."
                ),
            ]
            db.add_all(fullstack_questions)
            db.commit()
    
    # Итоговая статистика
    total_questions = db.query(Question).count()
    print(f"✅ Всего вопросов в базе: {total_questions}")
    
    for name, prof in professions.items():
        count = db.query(Question).filter(Question.profession_id == prof.id).count()
        print(f"   {name}: {count} вопросов")
