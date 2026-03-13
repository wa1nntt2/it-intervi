#!/usr/bin/env python3
"""Добавляет новые вопросы для DevOps Intern и Junior."""

import asyncio
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
os.chdir('backend')

from sqlalchemy import select
from backend.app.models.profession import Profession
from backend.app.models.question import Question
from backend.app.models.answer import Answer
from backend.app.models.question_type import QuestionType
from backend.app.database import async_session_maker

# Новые вопросы для Intern (15 вопросов)
intern_questions = [
    {
        "text": "Что такое контейнеризация?",
        "explanation": "🔍 Контейнеризация — технология виртуализации на уровне ОС\n\n📦 Преимущества:\n    • Изоляция приложений\n    • Быстрый запуск (секунды)\n    • Переносимость между средами\n    • Эффективное использование ресурсов\n\n🛠️ Инструменты:\n    Docker, Podman, containerd",
        "difficulty": "intern",
        "answers": [
            {"text": "Упаковка приложения со зависимостями в изолированную среду", "is_correct": True},
            {"text": "Создание виртуальных машин с полной ОС", "is_correct": False},
            {"text": "Резервное копирование данных", "is_correct": False},
            {"text": "Мониторинг производительности серверов", "is_correct": False},
        ]
    },
    {
        "text": "Какая команда Docker используется для запуска контейнера?",
        "explanation": "🔍 docker run — основная команда для запуска контейнеров\n\n📦 Примеры:\n    docker run nginx — запустить nginx\n    docker run -d nginx — в фоновом режиме\n    docker run -p 8080:80 nginx — с маппингом порта\n    docker run --name my-nginx nginx — с именем\n\n🛠️ Опции:\n    -d (detached), -p (port), --name, -e (env)",
        "difficulty": "intern",
        "answers": [
            {"text": "docker run", "is_correct": True},
            {"text": "docker start", "is_correct": False},
            {"text": "docker create", "is_correct": False},
            {"text": "docker exec", "is_correct": False},
        ]
    },
    {
        "text": "Что такое Docker Image?",
        "explanation": "🔍 Docker Image — шаблон только для чтения для создания контейнеров\n\n📦 Особенности:\n    • Содержит приложение и зависимости\n    • Слоистая структура (layers)\n    • Неизменяемый (immutable)\n    • Хранится в реестре (Docker Hub)\n\n🛠️ Команды:\n    docker build — создать образ\n    docker pull — скачать\n    docker push — загрузить",
        "difficulty": "intern",
        "answers": [
            {"text": "Шаблон только для чтения для создания контейнеров", "is_correct": True},
            {"text": "Запущенный экземпляр приложения", "is_correct": False},
            {"text": "Файл с логами контейнера", "is_correct": False},
            {"text": "Скрипт для автоматизации развёртывания", "is_correct": False},
        ]
    },
    {
        "text": "Что делает команда `docker ps`?",
        "explanation": "🔍 docker ps — показывает список запущенных контейнеров\n\n📦 Опции:\n    docker ps — запущенные контейнеры\n    docker ps -a — все (включая остановленные)\n    docker ps -l — последний созданный\n\n🛠️ Вывод:\n    CONTAINER ID, IMAGE, COMMAND, CREATED, STATUS, PORTS, NAMES",
        "difficulty": "intern",
        "answers": [
            {"text": "Показывает список запущенных контейнеров", "is_correct": True},
            {"text": "Останавливает контейнеры", "is_correct": False},
            {"text": "Создаёт новый контейнер", "is_correct": False},
            {"text": "Удаляет старые контейнеры", "is_correct": False},
        ]
    },
    {
        "text": "Что такое Dockerfile?",
        "explanation": "🔍 Dockerfile — текстовый файл с инструкциями для сборки образа\n\n📦 Основные инструкции:\n    FROM — базовый образ\n    WORKDIR — рабочая директория\n    COPY — копирование файлов\n    RUN — выполнение команд\n    CMD — команда по умолчанию\n    EXPOSE — порт контейнера\n\n🛠️ Пример:\n    FROM python:3.11\n    WORKDIR /app\n    COPY . .\n    RUN pip install -r requirements.txt\n    CMD [\"python\", \"app.py\"]",
        "difficulty": "intern",
        "answers": [
            {"text": "Текстовый файл с инструкциями для сборки Docker образа", "is_correct": True},
            {"text": "Скрипт для запуска контейнера", "is_correct": False},
            {"text": "Файл конфигурации Docker daemon", "is_correct": False},
            {"text": "Лог сборки контейнера", "is_correct": False},
        ]
    },
    {
        "text": "Какая команда используется для остановки контейнера?",
        "explanation": "🔍 docker stop — корректная остановка контейнера\n\n📦 Команды управления:\n    docker stop container — остановить\n    docker start container — запустить\n    docker restart container — перезапустить\n    docker kill container — принудительно убить\n\n🛠️ Примеры:\n    docker stop my-app\n    docker stop $(docker ps -q) — все контейнеры",
        "difficulty": "intern",
        "answers": [
            {"text": "docker stop", "is_correct": True},
            {"text": "docker pause", "is_correct": False},
            {"text": "docker kill", "is_correct": False},
            {"text": "docker down", "is_correct": False},
        ]
    },
    {
        "text": "Что такое Docker Hub?",
        "explanation": "🔍 Docker Hub — облачный реестр для хранения и распространения Docker образов\n\n📦 Возможности:\n    • Публичные и приватные репозитории\n    • Автоматическая сборка из GitHub\n    • Сканирование на уязвимости\n    • Управление доступом\n\n🛠️ Использование:\n    docker pull nginx — скачать официальный образ\n    docker pull username/image — пользовательский\n    docker push username/image — загрузить свой",
        "difficulty": "intern",
        "answers": [
            {"text": "Облачный реестр для хранения Docker образов", "is_correct": True},
            {"text": "Инструмент для мониторинга контейнеров", "is_correct": False},
            {"text": "Среда разработки для Docker", "is_correct": False},
            {"text": "Панель управления Docker daemon", "is_correct": False},
        ]
    },
    {
        "text": "Что означает директива FROM в Dockerfile?",
        "explanation": "🔍 FROM — указывает базовый образ для сборки\n\n📦 Особенности:\n    • Должна быть первой инструкцией\n    • Может использоваться несколько раз (multi-stage)\n    • Определяет ОС и окружение\n\n🛠️ Примеры:\n    FROM ubuntu:22.04\n    FROM python:3.11-slim\n    FROM node:18-alpine\n    FROM scratch — пустой образ",
        "difficulty": "intern",
        "answers": [
            {"text": "Указывает базовый образ для сборки", "is_correct": True},
            {"text": "Определяет команду запуска", "is_correct": False},
            {"text": "Копирует файлы в образ", "is_correct": False},
            {"text": "Устанавливает переменные окружения", "is_correct": False},
        ]
    },
    {
        "text": "Какая команда показывает логи контейнера?",
        "explanation": "🔍 docker logs — вывод логов контейнера\n\n📦 Опции:\n    docker logs container — все логи\n    docker logs -f container — follow (как tail -f)\n    docker logs --tail 100 — последние 100 строк\n    docker logs --since 1h — за последний час\n\n🛠️ Примеры:\n    docker logs my-app\n    docker logs -f --tail 50 my-app",
        "difficulty": "intern",
        "answers": [
            {"text": "docker logs", "is_correct": True},
            {"text": "docker inspect", "is_correct": False},
            {"text": "docker events", "is_correct": False},
            {"text": "docker stats", "is_correct": False},
        ]
    },
    {
        "text": "Что такое Docker Compose?",
        "explanation": "🔍 Docker Compose — инструмент для запуска multi-container приложений\n\n📦 Особенности:\n    • YAML файл (docker-compose.yml)\n    • Описание сервисов, сетей, volumes\n    • Управление одной командой\n\n🛠️ Команды:\n    docker-compose up — запустить\n    docker-compose down — остановить\n    docker-compose ps — статус\n    docker-compose logs — логи\n\n📦 Пример:\n    version: '3'\n    services:\n      web:\n        build: .\n        ports:\n          - \"8000:8000\"\n      db:\n        image: postgres",
        "difficulty": "intern",
        "answers": [
            {"text": "Инструмент для запуска multi-container приложений", "is_correct": True},
            {"text": "Редактор Dockerfile", "is_correct": False},
            {"text": "Мониторинг контейнеров", "is_correct": False},
            {"text": "Реестр для образов", "is_correct": False},
        ]
    },
    {
        "text": "Какой порт используется по умолчанию для SSH?",
        "explanation": "🔍 Порт 22 — стандартный порт для SSH\n\n📦 Популярные порты:\n    22 — SSH\n    80 — HTTP\n    443 — HTTPS\n    3306 — MySQL\n    5432 — PostgreSQL\n    6379 — Redis\n    8080 — альтернативный HTTP\n\n🛠️ Проверка:\n    netstat -tulpn | grep :22\n    ss -tulpn | grep :22",
        "difficulty": "intern",
        "answers": [
            {"text": "22", "is_correct": True},
            {"text": "80", "is_correct": False},
            {"text": "8080", "is_correct": False},
            {"text": "443", "is_correct": False},
        ]
    },
    {
        "text": "Что делает команда `git clone`?",
        "explanation": "🔍 git clone — копирует удалённый репозиторий локально\n\n📦 Примеры:\n    git clone https://github.com/user/repo.git\n    git clone git@github.com:user/repo.git\n    git clone <url> folder-name\n\n🛠️ Опции:\n    --depth 1 — shallow clone (только последний коммит)\n    --branch name — клонировать конкретную ветку\n    --recursive — включая субмодули",
        "difficulty": "intern",
        "answers": [
            {"text": "Копирует удалённый репозиторий на локальную машину", "is_correct": True},
            {"text": "Создаёт новую ветку", "is_correct": False},
            {"text": "Отправляет изменения на сервер", "is_correct": False},
            {"text": "Показывает историю коммитов", "is_correct": False},
        ]
    },
    {
        "text": "Какая команда показывает текущую директорию в Linux?",
        "explanation": "🔍 pwd (print working directory) — показывает полный путь к текущей папке\n\n📦 Примеры:\n    pwd\n    /home/user/projects\n\n🛠️ Смежные команды:\n    cd /path — перейти в директорию\n    cd .. — на уровень вверх\n    cd ~ — в домашнюю директорию\n    ls — список файлов",
        "difficulty": "intern",
        "answers": [
            {"text": "pwd", "is_correct": True},
            {"text": "cd", "is_correct": False},
            {"text": "ls", "is_correct": False},
            {"text": "dir", "is_correct": False},
        ]
    },
    {
        "text": "Что такое переменная окружения?",
        "explanation": "🔍 Переменная окружения — именованное значение, доступное процессам\n\n📦 Примеры:\n    PATH — пути для поиска исполняемых файлов\n    HOME — домашняя директория\n    USER — имя пользователя\n    DATABASE_URL — строка подключения к БД\n    API_KEY — ключ API\n\n🛠️ Команды:\n    env — показать все переменные\n    export VAR=value — установить\n    echo $VAR — вывести\n    unset VAR — удалить",
        "difficulty": "intern",
        "answers": [
            {"text": "Именованное значение, доступное процессам в системе", "is_correct": True},
            {"text": "Глобальная переменная в коде программы", "is_correct": False},
            {"text": "Настройка конфигурации Git", "is_correct": False},
            {"text": "Параметр командной строки", "is_correct": False},
        ]
    },
    {
        "text": "Какая команда используется для создания новой ветки в Git?",
        "explanation": "🔍 git branch — создание и управление ветками\n\n📦 Команды:\n    git branch name — создать ветку\n    git checkout -b name — создать и переключиться\n    git switch -c name — создать и переключиться (новая команда)\n\n🛠️ Управление:\n    git branch — список веток\n    git checkout name — переключиться\n    git branch -d name — удалить",
        "difficulty": "intern",
        "answers": [
            {"text": "git branch", "is_correct": True},
            {"text": "git commit", "is_correct": False},
            {"text": "git merge", "is_correct": False},
            {"text": "git push", "is_correct": False},
        ]
    },
]

# Новые вопросы для Junior (15 вопросов)
junior_questions = [
    {
        "text": "Что такое Kubernetes Pod?",
        "explanation": "🔍 Pod — минимальная единица в Kubernetes\n\n📦 Особенности:\n    • Один или несколько контейнеров\n    • Общий IP и порты\n    • Общие volumes (хранилище)\n    • Эфемерный (при сбое создаётся новый)\n\n🛠️ Пример:\n    apiVersion: v1\n    kind: Pod\n    metadata:\n      name: my-pod\n    spec:\n      containers:\n      - name: app\n        image: nginx",
        "difficulty": "junior",
        "answers": [
            {"text": "Минимальная единица K8s, группа контейнеров с общими ресурсами", "is_correct": True},
            {"text": "Тип балансировщика нагрузки", "is_correct": False},
            {"text": "Хранилище данных в кластере", "is_correct": False},
            {"text": "Сервис для мониторинга", "is_correct": False},
        ]
    },
    {
        "text": "Какая команда Kubernetes показывает список подов?",
        "explanation": "🔍 kubectl get pods — вывод списка подов\n\n📦 Команды:\n    kubectl get pods — в текущем namespace\n    kubectl get pods -A — во всех namespace\n    kubectl get pods -n name — в конкретном\n    kubectl get pods -o wide — подробно\n\n🛠️ Другие команды:\n    kubectl describe pod name — детали\n    kubectl logs pod name — логи\n    kubectl delete pod name — удалить",
        "difficulty": "junior",
        "answers": [
            {"text": "kubectl get pods", "is_correct": True},
            {"text": "kubectl list pods", "is_correct": False},
            {"text": "kubectl show pods", "is_correct": False},
            {"text": "kubectl describe pods", "is_correct": False},
        ]
    },
    {
        "text": "Что такое Kubernetes Deployment?",
        "explanation": "🔍 Deployment — контроллер для управления подами\n\n📦 Функции:\n    • Держит нужное количество реплик\n    • Rolling updates (обновление без простоя)\n    • Rollback (откат при проблемах)\n    • Самовосстановление\n\n🛠️ Пример:\n    apiVersion: apps/v1\n    kind: Deployment\n    spec:\n      replicas: 3\n      template:\n        spec:\n          containers:\n          - name: app\n            image: nginx",
        "difficulty": "junior",
        "answers": [
            {"text": "Контроллер для управления репликами и обновлениями подов", "is_correct": True},
            {"text": "Тип хранилища данных", "is_correct": False},
            {"text": "Сервис для балансировки нагрузки", "is_correct": False},
            {"text": "Инструмент мониторинга", "is_correct": False},
        ]
    },
    {
        "text": "Что делает команда `docker build`?",
        "explanation": "🔍 docker build — собирает Docker образ из Dockerfile\n\n📦 Примеры:\n    docker build . — из текущей директории\n    docker build -t name:tag . — с именем\n    docker build -f Dockerfile.prod . — с другим файлом\n\n🛠️ Опции:\n    -t (tag), -f (file), --no-cache,\n    --build-arg VAR=value",
        "difficulty": "junior",
        "answers": [
            {"text": "Собирает Docker образ из Dockerfile", "is_correct": True},
            {"text": "Запускает контейнер", "is_correct": False},
            {"text": "Загружает образ из реестра", "is_correct": False},
            {"text": "Показывает историю слоёв", "is_correct": False},
        ]
    },
    {
        "text": "Что такое Kubernetes Service?",
        "explanation": "🔍 Service — абстракция для доступа к подам\n\n📦 Типы:\n    ClusterIP — внутренний IP (по умолчанию)\n    NodePort — порт на каждой ноде\n    LoadBalancer — облачный балансировщик\n    ExternalName — DNS CNAME\n\n🛠️ Пример:\n    apiVersion: v1\n    kind: Service\n    spec:\n      type: ClusterIP\n      selector:\n        app: my-app\n      ports:\n      - port: 80\n        targetPort: 8080",
        "difficulty": "junior",
        "answers": [
            {"text": "Абстракция для сетевого доступа к группе подов", "is_correct": True},
            {"text": "Хранилище конфигураций", "is_correct": False},
            {"text": "Инструмент развёртывания", "is_correct": False},
            {"text": "Сервис мониторинга", "is_correct": False},
        ]
    },
    {
        "text": "Какая команда показывает использование ресурсов в Linux?",
        "explanation": "🔍 top / htop — мониторинг ресурсов в реальном времени\n\n📦 Команды:\n    top — интерактивный мониторинг\n    htop — улучшенная версия top\n    free -h — использование RAM\n    df -h — использование диска\n    du -sh * — размер папок\n\n🛠️ top показывает:\n    PID, USER, %CPU, %MEM, TIME+, COMMAND",
        "difficulty": "junior",
        "answers": [
            {"text": "top", "is_correct": True},
            {"text": "pwd", "is_correct": False},
            {"text": "ls", "is_correct": False},
            {"text": "cat", "is_correct": False},
        ]
    },
    {
        "text": "Что такое Docker Volume?",
        "explanation": "🔍 Volume — механизм для постоянного хранения данных\n\n📦 Особенности:\n    • Данные сохраняются после удаления контейнера\n    • Общий доступ между контейнерами\n    • Управляется Docker\n\n🛠️ Команды:\n    docker volume create name\n    docker volume ls — список\n    docker volume inspect name\n    docker run -v name:/path image\n\n📦 Пример:\n    docker run -d -v mydata:/var/lib/mysql mysql",
        "difficulty": "junior",
        "answers": [
            {"text": "Механизм для постоянного хранения данных контейнера", "is_correct": True},
            {"text": "Временное хранилище в контейнере", "is_correct": False},
            {"text": "Резервная копия образа", "is_correct": False},
            {"text": "Сетевой драйвер", "is_correct": False},
        ]
    },
    {
        "text": "Что делает команда `git merge`?",
        "explanation": "🔍 git merge — объединяет изменения из одной ветки в другую\n\n📦 Примеры:\n    git merge feature — влить feature в текущую\n    git merge --no-ff feature — с коммитом слияния\n\n🛠️ Конфликты:\n    Возникают при изменении одних строк\n    Решаются вручную в файле\n    Затем: git add, git commit\n\n🔄 Альтернатива:\n    git rebase — переписать историю",
        "difficulty": "junior",
        "answers": [
            {"text": "Объединяет изменения из одной ветки в другую", "is_correct": True},
            {"text": "Создаёт новую ветку", "is_correct": False},
            {"text": "Удаляет ветку", "is_correct": False},
            {"text": "Показывает различия между ветками", "is_correct": False},
        ]
    },
    {
        "text": "Что такое ConfigMap в Kubernetes?",
        "explanation": "🔍 ConfigMap — хранение конфигурационных данных\n\n📦 Что хранит:\n    • Переменные окружения\n    • Конфигурационные файлы\n    • Command-line аргументы\n\n🛠️ Создание:\n    kubectl create cm name --from-literal=key=value\n    kubectl create cm name --from-file=config.yaml\n\n📦 Использование:\n    envFrom:\n      configMapRef:\n        name: my-config",
        "difficulty": "junior",
        "answers": [
            {"text": "Объект для хранения не-секретных конфигурационных данных", "is_correct": True},
            {"text": "Тип хранилища для баз данных", "is_correct": False},
            {"text": "Сервис для шифрования секретов", "is_correct": False},
            {"text": "Инструмент развёртывания", "is_correct": False},
        ]
    },
    {
        "text": "Какая команда используется для входа в контейнер?",
        "explanation": "🔍 docker exec — выполнение команд в контейнере\n\n📦 Примеры:\n    docker exec -it container /bin/bash\n    docker exec -it container sh\n    docker exec container ls /app\n\n🛠️ Опции:\n    -it — интерактивный режим\n    -e VAR=value — переменная окружения\n    -u user — от имени пользователя\n\n📦 Для Kubernetes:\n    kubectl exec -it pod -- /bin/bash",
        "difficulty": "junior",
        "answers": [
            {"text": "docker exec -it", "is_correct": True},
            {"text": "docker run", "is_correct": False},
            {"text": "docker attach", "is_correct": False},
            {"text": "docker login", "is_correct": False},
        ]
    },
    {
        "text": "Что такое `.dockerignore`?",
        "explanation": "🔍 .dockerignore — файлы, которые не копируются в образ\n\n📦 Примеры:\n    node_modules/\n    .git/\n    .env\n    *.log\n    .DS_Store\n    __pycache__/\n\n🛠️ Преимущества:\n    • Меньший размер образа\n    • Быстрее сборка\n    • Нет секретов в образе\n\n📦 Похож на .gitignore но для Docker",
        "difficulty": "junior",
        "answers": [
            {"text": "Файл с исключениями для копирования в Docker образ", "is_correct": True},
            {"text": "Конфигурация Docker daemon", "is_correct": False},
            {"text": "Лог игнорируемых событий", "is_correct": False},
            {"text": "Шаблон для Dockerfile", "is_correct": False},
        ]
    },
    {
        "text": "Что делает команда `kubectl apply -f`?",
        "explanation": "🔍 kubectl apply -f — создаёт/обновляет ресурсы из YAML\n\n📦 Примеры:\n    kubectl apply -f deployment.yaml\n    kubectl apply -f ./manifests/ — рекурсивно\n    kubectl apply -f https://url/file.yaml\n\n🛠️ Отличие от create:\n    apply — декларативно (создаёт или обновляет)\n    create — только создание\n\n🔄 Управление:\n    kubectl delete -f file.yaml — удалить",
        "difficulty": "junior",
        "answers": [
            {"text": "Применяет конфигурацию из YAML файла к кластеру", "is_correct": True},
            {"text": "Создаёт резервную копию конфигурации", "is_correct": False},
            {"text": "Показывает текущую конфигурацию", "is_correct": False},
            {"text": "Редактирует конфигурацию", "is_correct": False},
        ]
    },
    {
        "text": "Что такое Docker Network?",
        "explanation": "🔍 Docker Network — виртуальная сеть для контейнеров\n\n📦 Типы:\n    bridge — сеть по умолчанию\n    host — без изоляции сети\n    none — без сети\n    overlay — для multi-host\n\n🛠️ Команды:\n    docker network create name\n    docker network ls\n    docker run --network name image\n\n📦 Пример:\n    docker network create mynet\n    docker run --network mynet nginx",
        "difficulty": "junior",
        "answers": [
            {"text": "Виртуальная сеть для коммуникации между контейнерами", "is_correct": True},
            {"text": "Физический сетевой кабель", "is_correct": False},
            {"text": "Настройка DNS сервера", "is_correct": False},
            {"text": "Брандмауэр для контейнеров", "is_correct": False},
        ]
    },
    {
        "text": "Какая команда показывает историю коммитов в Git?",
        "explanation": "🔍 git log — история коммитов\n\n📦 Примеры:\n    git log — полная история\n    git log --oneline — компактно\n    git log -5 — последние 5\n    git log --graph — с графом веток\n\n🛠️ Опции:\n    --oneline, --graph, --all,\n    --since, --until, --author",
        "difficulty": "junior",
        "answers": [
            {"text": "git log", "is_correct": True},
            {"text": "git history", "is_correct": False},
            {"text": "git show", "is_correct": False},
            {"text": "git status", "is_correct": False},
        ]
    },
    {
        "text": "Что такое Secret в Kubernetes?",
        "explanation": "🔍 Secret — хранение чувствительных данных\n\n📦 Что хранит:\n    • Пароли\n    • API ключи\n    • TLS сертификаты\n    • Токены\n\n🛠️ Создание:\n    kubectl create secret generic name \\\n      --from-literal=password=secret\n\n📦 Использование:\n    env:\n      - name: DB_PASSWORD\n        valueFrom:\n          secretKeyRef:\n            name: my-secret\n            key: password",
        "difficulty": "junior",
        "answers": [
            {"text": "Объект для хранения конфиденциальных данных (пароли, ключи)", "is_correct": True},
            {"text": "Тип шифрования трафика", "is_correct": False},
            {"text": "Сервис аутентификации", "is_correct": False},
            {"text": "Инструмент для шифрования дисков", "is_correct": False},
        ]
    },
]


async def main():
    async with async_session_maker() as session:
        # Найти профессию DevOps
        result = await session.execute(
            select(Profession).where(Profession.slug == 'devops')
        )
        profession = result.scalar_one_or_none()
        
        if not profession:
            print('❌ Профессия DevOps не найдена!')
            return
        
        # Найти тип вопроса multiple_choice
        result = await session.execute(
            select(QuestionType).where(QuestionType.code == 'multiple_choice')
        )
        question_type = result.scalar_one_or_none()
        
        if not question_type:
            print('❌ Тип вопроса multiple_choice не найден!')
            return
        
        print(f'➕ Добавление вопросов для DevOps (ID={profession.id})...')
        
        # Добавить Intern вопросы
        added_intern = 0
        for q_data in intern_questions:
            question = Question(
                profession_id=profession.id,
                question_type_id=question_type.id,
                text=q_data['text'],
                explanation=q_data['explanation'],
                difficulty=q_data['difficulty'],
            )
            session.add(question)
            await session.flush()
            
            # Добавить ответы
            for i, answer_data in enumerate(q_data['answers']):
                answer = Answer(
                    question_id=question.id,
                    text=answer_data['text'],
                    is_correct=answer_data['is_correct'],
                    display_order=i + 1,
                )
                session.add(answer)
            
            added_intern += 1
        
        # Добавить Junior вопросы
        added_junior = 0
        for q_data in junior_questions:
            question = Question(
                profession_id=profession.id,
                question_type_id=question_type.id,
                text=q_data['text'],
                explanation=q_data['explanation'],
                difficulty=q_data['difficulty'],
            )
            session.add(question)
            await session.flush()
            
            # Добавить ответы
            for i, answer_data in enumerate(q_data['answers']):
                answer = Answer(
                    question_id=question.id,
                    text=answer_data['text'],
                    is_correct=answer_data['is_correct'],
                    display_order=i + 1,
                )
                session.add(answer)
            
            added_junior += 1
        
        await session.commit()
        
        print(f'✅ Добавлено вопросов:')
        print(f'   🌱 Intern: {added_intern}')
        print(f'   🚀 Junior: {added_junior}')
        print(f'   📊 Всего: {added_intern + added_junior}')


if __name__ == '__main__':
    asyncio.run(main())
