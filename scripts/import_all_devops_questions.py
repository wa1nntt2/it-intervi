#!/usr/bin/env python3
"""
Скрипт для импорта вопросов DevOps в базу данных.
Запуск: cd backend && source venv/bin/activate && cd .. && python3 scripts/import_all_devops_questions.py
"""

import sys
import os

# Добавляем backend в path
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
backend_dir = os.path.join(project_dir, 'backend')
sys.path.insert(0, backend_dir)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Используем БД из backend директории
DATABASE_URL = "sqlite:///./interview_trainer.db"
from app.models.profession import Profession
from app.models.question import Question

# Вопросы DevOps Intern (15 вопросов)
intern_questions = [
    {
        "text": "Что такое контейнеризация?",
        "explanation": "Контейнеризация — технология виртуализации на уровне ОС. Преимущества: изоляция приложений, быстрый запуск, переносимость, эффективное использование ресурсов. Инструменты: Docker, Podman, containerd.",
        "difficulty": "intern",
        "options": [
            "Упаковка приложения со зависимостями в изолированную среду",
            "Создание виртуальных машин с полной ОС",
            "Резервное копирование данных",
            "Мониторинг производительности серверов",
        ],
        "correct_option": 0,
    },
    {
        "text": "Какая команда Docker используется для запуска контейнера?",
        "explanation": "docker run — основная команда для запуска контейнеров. Примеры: docker run nginx, docker run -d nginx (фоновый режим), docker run -p 8080:80 nginx (маппинг порта).",
        "difficulty": "intern",
        "options": [
            "docker run",
            "docker start",
            "docker create",
            "docker exec",
        ],
        "correct_option": 0,
    },
    {
        "text": "Что такое Docker Image?",
        "explanation": "Docker Image — шаблон только для чтения для создания контейнеров. Содержит приложение и зависимости, имеет слоистую структуру, неизменяемый, хранится в реестре (Docker Hub).",
        "difficulty": "intern",
        "options": [
            "Шаблон только для чтения для создания контейнеров",
            "Запущенный экземпляр приложения",
            "Файл с логами контейнера",
            "Скрипт для автоматизации развёртывания",
        ],
        "correct_option": 0,
    },
    {
        "text": "Что делает команда `docker ps`?",
        "explanation": "docker ps — показывает список запущенных контейнеров. Опции: docker ps -a (все), docker ps -l (последний).",
        "difficulty": "intern",
        "options": [
            "Показывает список запущенных контейнеров",
            "Останавливает контейнеры",
            "Создаёт новый контейнер",
            "Удаляет старые контейнеры",
        ],
        "correct_option": 0,
    },
    {
        "text": "Что такое Dockerfile?",
        "explanation": "Dockerfile — текстовый файл с инструкциями для сборки Docker образа. Основные инструкции: FROM, WORKDIR, COPY, RUN, CMD, EXPOSE.",
        "difficulty": "intern",
        "options": [
            "Текстовый файл с инструкциями для сборки Docker образа",
            "Скрипт для запуска контейнера",
            "Файл конфигурации Docker daemon",
            "Лог сборки контейнера",
        ],
        "correct_option": 0,
    },
    {
        "text": "Какая команда используется для остановки контейнера?",
        "explanation": "docker stop — корректная остановка контейнера. Также: docker start (запуск), docker restart (перезапуск), docker kill (принудительно).",
        "difficulty": "intern",
        "options": [
            "docker stop",
            "docker pause",
            "docker kill",
            "docker down",
        ],
        "correct_option": 0,
    },
    {
        "text": "Что такое Docker Hub?",
        "explanation": "Docker Hub — облачный реестр для хранения и распространения Docker образов. Поддерживает публичные и приватные репозитории, автоматическую сборку из GitHub.",
        "difficulty": "intern",
        "options": [
            "Облачный реестр для хранения Docker образов",
            "Инструмент для мониторинга контейнеров",
            "Среда разработки для Docker",
            "Панель управления Docker daemon",
        ],
        "correct_option": 0,
    },
    {
        "text": "Что означает директива FROM в Dockerfile?",
        "explanation": "FROM — указывает базовый образ для сборки. Должна быть первой инструкцией, может использоваться несколько раз (multi-stage).",
        "difficulty": "intern",
        "options": [
            "Указывает базовый образ для сборки",
            "Определяет команду запуска",
            "Копирует файлы в образ",
            "Устанавливает переменные окружения",
        ],
        "correct_option": 0,
    },
    {
        "text": "Какая команда показывает логи контейнера?",
        "explanation": "docker logs — вывод логов контейнера. Опции: -f (follow), --tail (последние N строк), --since (за время).",
        "difficulty": "intern",
        "options": [
            "docker logs",
            "docker inspect",
            "docker events",
            "docker stats",
        ],
        "correct_option": 0,
    },
    {
        "text": "Что такое Docker Compose?",
        "explanation": "Docker Compose — инструмент для запуска multi-container приложений. Использует YAML файл (docker-compose.yml) для описания сервисов, сетей, volumes.",
        "difficulty": "intern",
        "options": [
            "Инструмент для запуска multi-container приложений",
            "Редактор Dockerfile",
            "Мониторинг контейнеров",
            "Реестр для образов",
        ],
        "correct_option": 0,
    },
    {
        "text": "Какой порт используется по умолчанию для SSH?",
        "explanation": "Порт 22 — стандартный порт для SSH. Популярные порты: 22 (SSH), 80 (HTTP), 443 (HTTPS), 3306 (MySQL), 5432 (PostgreSQL), 6379 (Redis).",
        "difficulty": "intern",
        "options": [
            "22",
            "80",
            "8080",
            "443",
        ],
        "correct_option": 0,
    },
    {
        "text": "Что делает команда `git clone`?",
        "explanation": "git clone — копирует удалённый репозиторий на локальную машину. Примеры: git clone <url>, git clone --depth 1 (shallow), git clone --branch name.",
        "difficulty": "intern",
        "options": [
            "Копирует удалённый репозиторий на локальную машину",
            "Создаёт новую ветку",
            "Отправляет изменения на сервер",
            "Показывает историю коммитов",
        ],
        "correct_option": 0,
    },
    {
        "text": "Какая команда показывает текущую директорию в Linux?",
        "explanation": "pwd (print working directory) — показывает полный путь к текущей директории. Смежные команды: cd (перейти), ls (список файлов).",
        "difficulty": "intern",
        "options": [
            "pwd",
            "cd",
            "ls",
            "dir",
        ],
        "correct_option": 0,
    },
    {
        "text": "Что такое переменная окружения?",
        "explanation": "Переменная окружения — именованное значение, доступное процессам в системе. Примеры: PATH, HOME, USER, DATABASE_URL, API_KEY.",
        "difficulty": "intern",
        "options": [
            "Именованное значение, доступное процессам в системе",
            "Глобальная переменная в коде программы",
            "Настройка конфигурации Git",
            "Параметр командной строки",
        ],
        "correct_option": 0,
    },
    {
        "text": "Какая команда используется для создания новой ветки в Git?",
        "explanation": "git branch — создание и управление ветками. Также: git checkout -b name (создать и переключиться), git switch -c name (новая команда).",
        "difficulty": "intern",
        "options": [
            "git branch",
            "git commit",
            "git merge",
            "git push",
        ],
        "correct_option": 0,
    },
]

# Вопросы DevOps Junior (15 вопросов)
junior_questions = [
    {
        "text": "Что такое Kubernetes Pod?",
        "explanation": "Pod — минимальная единица в Kubernetes. Группа из одного или нескольких контейнеров с общими IP, портами и volumes. Эфемерный — при сбое создаётся новый.",
        "difficulty": "junior",
        "options": [
            "Минимальная единица K8s, группа контейнеров с общими ресурсами",
            "Тип балансировщика нагрузки",
            "Хранилище данных в кластере",
            "Сервис для мониторинга",
        ],
        "correct_option": 0,
    },
    {
        "text": "Какая команда Kubernetes показывает список подов?",
        "explanation": "kubectl get pods — вывод списка подов. Опции: -A (все namespace), -n name (конкретный), -o wide (подробно).",
        "difficulty": "junior",
        "options": [
            "kubectl get pods",
            "kubectl list pods",
            "kubectl show pods",
            "kubectl describe pods",
        ],
        "correct_option": 0,
    },
    {
        "text": "Что такое Kubernetes Deployment?",
        "explanation": "Deployment — контроллер для управления репликами и обновлениями подов. Держит нужное количество реплик, поддерживает rolling updates и rollback.",
        "difficulty": "junior",
        "options": [
            "Контроллер для управления репликами и обновлениями подов",
            "Тип хранилища данных",
            "Сервис для балансировки нагрузки",
            "Инструмент мониторинга",
        ],
        "correct_option": 0,
    },
    {
        "text": "Что делает команда `docker build`?",
        "explanation": "docker build — собирает Docker образ из Dockerfile. Примеры: docker build -t name:tag . (с именем), docker build -f Dockerfile.prod .",
        "difficulty": "junior",
        "options": [
            "Собирает Docker образ из Dockerfile",
            "Запускает контейнер",
            "Загружает образ из реестра",
            "Показывает историю слоёв",
        ],
        "correct_option": 0,
    },
    {
        "text": "Что такое Kubernetes Service?",
        "explanation": "Service — абстракция для сетевого доступа к группе подов. Типы: ClusterIP (внутренний), NodePort (порт на ноде), LoadBalancer (облачный балансировщик).",
        "difficulty": "junior",
        "options": [
            "Абстракция для сетевого доступа к группе подов",
            "Хранилище конфигураций",
            "Инструмент развёртывания",
            "Сервис мониторинга",
        ],
        "correct_option": 0,
    },
    {
        "text": "Какая команда показывает использование ресурсов в Linux?",
        "explanation": "top / htop — мониторинг ресурсов в реальном времени. Также: free -h (RAM), df -h (диск), du -sh (размер папок).",
        "difficulty": "junior",
        "options": [
            "top",
            "pwd",
            "ls",
            "cat",
        ],
        "correct_option": 0,
    },
    {
        "text": "Что такое Docker Volume?",
        "explanation": "Volume — механизм для постоянного хранения данных контейнера. Данные сохраняются после удаления контейнера, управляется Docker.",
        "difficulty": "junior",
        "options": [
            "Механизм для постоянного хранения данных контейнера",
            "Временное хранилище в контейнере",
            "Резервная копия образа",
            "Сетевой драйвер",
        ],
        "correct_option": 0,
    },
    {
        "text": "Что делает команда `git merge`?",
        "explanation": "git merge — объединяет изменения из одной ветки в другую. Конфликты возникают при изменении одних строк, решаются вручную.",
        "difficulty": "junior",
        "options": [
            "Объединяет изменения из одной ветки в другую",
            "Создаёт новую ветку",
            "Удаляет ветку",
            "Показывает различия между файлами",
        ],
        "correct_option": 0,
    },
    {
        "text": "Что такое Kubernetes Namespace?",
        "explanation": "Namespace — способ разделения кластера K8s на виртуальные кластеры. Используется для изоляции команд, проектов, сред (dev, staging, prod).",
        "difficulty": "junior",
        "options": [
            "Виртуальный кластер внутри K8s для изоляции ресурсов",
            "Физический сервер в кластере",
            "Тип хранилища данных",
            "Сетевой плагин",
        ],
        "correct_option": 0,
    },
    {
        "text": "Какая команда показывает версию Docker?",
        "explanation": "docker version — показывает версию клиента и сервера. Также: docker --version (кратко), docker info (подробная информация).",
        "difficulty": "junior",
        "options": [
            "docker version",
            "docker --info",
            "docker show",
            "docker check",
        ],
        "correct_option": 0,
    },
    {
        "text": "Что такое CI/CD pipeline?",
        "explanation": "CI/CD pipeline — автоматизированный процесс доставки кода. Этапы: Build (сборка), Test (тестирование), Deploy (развертывание), Monitor (мониторинг).",
        "difficulty": "junior",
        "options": [
            "Автоматизированный процесс доставки кода от разработки до продакшена",
            "Инструмент мониторинга",
            "Система управления задачами",
            "Платформа для видеоконференций",
        ],
        "correct_option": 0,
    },
    {
        "text": "Что делает команда `docker exec`?",
        "explanation": "docker exec — выполняет команду в запущенном контейнере. Пример: docker exec -it container bash (интерактивная оболочка).",
        "difficulty": "junior",
        "options": [
            "Выполняет команду в запущенном контейнере",
            "Запускает новый контейнер",
            "Останавливает контейнер",
            "Копирует файлы в контейнер",
        ],
        "correct_option": 0,
    },
    {
        "text": "Что такое LoadBalancer в Kubernetes?",
        "explanation": "LoadBalancer — тип Service для внешнего доступа через облачный балансировщик. Автоматически распределяет трафик между подами.",
        "difficulty": "junior",
        "options": [
            "Тип Service для внешнего доступа через облачный балансировщик",
            "Инструмент для сборки образов",
            "Хранилище конфигураций",
            "Мониторинг кластера",
        ],
        "correct_option": 0,
    },
    {
        "text": "Какая команда показывает использование диска в Linux?",
        "explanation": "df -h — использование дискового пространства. Также: du -sh * (размер папок), ls -lh (размер файлов).",
        "difficulty": "junior",
        "options": [
            "df -h",
            "pwd",
            "cd",
            "mkdir",
        ],
        "correct_option": 0,
    },
    {
        "text": "Что такое Docker Network?",
        "explanation": "Docker Network — виртуальная сеть для связи контейнеров. Типы: bridge (по умолчанию), host (без изоляции), none (без сети), overlay (между хостами).",
        "difficulty": "junior",
        "options": [
            "Виртуальная сеть для связи контейнеров",
            "Физический сетевой кабель",
            "Протокол передачи данных",
            "Брандмауэр Docker",
        ],
        "correct_option": 0,
    },
]

def main():
    # Создаем движок и сессию (используем БД из backend/)
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    try:
        # Находим DevOps профессию
        devops = db.query(Profession).filter(Profession.name == "DevOps Engineer").first()
        if not devops:
            print("❌ Профессия DevOps Engineer не найдена!")
            return
        
        print(f"✅ Найдена профессия: {devops.name} (id={devops.id})")
        
        # Счетчики
        added_intern = 0
        added_junior = 0
        skipped = 0
        
        # Добавляем Intern вопросы
        print("\n📚 Добавляем Intern вопросы...")
        for q_data in intern_questions:
            # Проверяем, есть ли уже такой вопрос
            existing = db.query(Question).filter(
                Question.text == q_data["text"],
                Question.profession_id == devops.id
            ).first()
            
            if existing:
                skipped += 1
                print(f"   ⚠️  Пропущен: {q_data['text'][:50]}...")
                continue
            
            # Создаем вопрос
            question = Question(
                text=q_data["text"],
                question_type="mcq",
                profession_id=devops.id,
                difficulty=q_data["difficulty"],
                options=q_data["options"],
                correct_option=q_data["correct_option"],
                explanation=q_data.get("explanation", "")
            )
            db.add(question)
            added_intern += 1
            print(f"   ✅ Добавлен: {q_data['text'][:50]}...")
        
        db.commit()
        print(f"\n✅ Добавлено Intern вопросов: {added_intern}")
        
        # Добавляем Junior вопросы
        print("\n📚 Добавляем Junior вопросы...")
        for q_data in junior_questions:
            # Проверяем, есть ли уже такой вопрос
            existing = db.query(Question).filter(
                Question.text == q_data["text"],
                Question.profession_id == devops.id
            ).first()
            
            if existing:
                skipped += 1
                print(f"   ⚠️  Пропущен: {q_data['text'][:50]}...")
                continue
            
            # Создаем вопрос
            question = Question(
                text=q_data["text"],
                question_type="mcq",
                profession_id=devops.id,
                difficulty=q_data["difficulty"],
                options=q_data["options"],
                correct_option=q_data["correct_option"],
                explanation=q_data.get("explanation", "")
            )
            db.add(question)
            added_junior += 1
            print(f"   ✅ Добавлен: {q_data['text'][:50]}...")
        
        db.commit()
        print(f"\n✅ Добавлено Junior вопросов: {added_junior}")
        
        # Итоги
        print("\n" + "="*50)
        print(f"📊 ИТОГИ:")
        print(f"   Добавлено: {added_intern + added_junior}")
        print(f"   Пропущено (дубликаты): {skipped}")
        print(f"   Intern: {added_intern}")
        print(f"   Junior: {added_junior}")
        print("="*50)
        
    except Exception as e:
        db.rollback()
        print(f"❌ Ошибка: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main()
