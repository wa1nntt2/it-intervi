# 📚 Добавление вопросов — Быстрый старт

## 🎯 Быстрое добавление вопросов

### 1️⃣ Используйте шаблон

Шаблон находится в: `docs/questions_template.json`

```bash
# Скопируйте шаблон
cp docs/questions_template.json my_questions.json
```

### 2️⃣ Заполните вопросы

Откройте `my_questions.json` и добавьте свои вопросы:

```json
{
  "questions": [
    {
      "text": "Ваш вопрос?",
      "question_type": "mcq",
      "difficulty": "intern",
      "options": ["Ответ 1", "Ответ 2", "Ответ 3", "Ответ 4"],
      "correct_option": 0,
      "explanation": "Пояснение",
      "profession_name": "Frontend Developer"
    }
  ]
}
```

### 3️⃣ Импортируйте

```bash
cd backend
source venv/bin/activate
python3 ../scripts/import_questions_from_json.py ../my_questions.json
```

---

## 📁 Файлы

| Файл | Описание |
|------|----------|
| [`docs/questions_template.json`](./questions_template.json) | Пустой шаблон с примерами |
| [`docs/QUESTIONS_TEMPLATE.md`](./QUESTIONS_TEMPLATE.md) | Полная документация формата |
| [`docs/linux_questions.json`](./linux_questions.json) | 60 вопросов по Linux (Intern/Junior/Middle) |
| [`scripts/import_questions_from_json.py`](../scripts/import_questions_from_json.py) | Скрипт импорта (SQLite) |
| [`scripts/import_questions_from_json_pg.py`](../scripts/import_questions_from_json_pg.py) | Скрипт импорта (PostgreSQL) |
| [`scripts/export_questions.py`](../scripts/export_questions.py) | Скрипт экспорта (бэкап) |

---

## 🔧 Команды

```bash
# Импортировать вопросы
python3 scripts/import_questions_from_json.py my_questions.json

# Экспортировать (бэкап)
python3 scripts/export_questions.py > backup.json

# Проверить количество вопросов
curl http://localhost:8000/api/questions/ | jq '.meta.total'
```

---

## 📝 Примеры вопросов

### Frontend Developer

```json
{
  "text": "Что такое JSX в React?",
  "question_type": "mcq",
  "difficulty": "junior",
  "options": [
    "Язык программирования",
    "Расширение JavaScript для добавления HTML в код",
    "Библиотека стилей",
    "Фреймворк"
  ],
  "correct_option": 1,
  "explanation": "JSX — синтаксический сахар для расширения JavaScript, позволяющий писать HTML-подобный код в React.",
  "profession_name": "Frontend Developer"
}
```

### Backend Developer

```json
{
  "text": "Что такое индекс в базе данных?",
  "question_type": "mcq",
  "difficulty": "junior",
  "options": [
    "Способ хранения данных",
    "Структура для ускорения поиска",
    "Тип запроса",
    "Язык программирования"
  ],
  "correct_option": 1,
  "explanation": "Индекс — структура данных для ускорения операций поиска в таблице.",
  "profession_name": "Backend Developer"
}
```

### DevOps Engineer

```json
{
  "text": "Что такое Docker Compose?",
  "question_type": "mcq",
  "difficulty": "junior",
  "options": [
    "Язык программирования",
    "Инструмент для оркестрации контейнеров",
    "Инструмент для определения и запуска многоконтейнерных приложений Docker",
    "Редактор кода"
  ],
  "correct_option": 2,
  "explanation": "Docker Compose — инструмент для определения и запуска многоконтейнерных приложений Docker с помощью YAML файлов.",
  "profession_name": "DevOps Engineer"
}
```

---

## ⚠️ Важно

1. **Сделайте бэкап перед импортом:**
   ```bash
   python3 scripts/export_questions.py > backup_$(date +%Y%m%d).json
   ```

2. **Проверьте JSON на валидность:**
   ```bash
   python3 -c "import json; json.load(open('my_questions.json'))"
   ```

3. **Вопросы с одинаковым текстом не дублируются**

---

## 🆘 Если что-то пошло не так

```bash
# Проверьте логи
docker logs it-interview-backend | tail -50

# Проверьте количество вопросов
docker exec it-interview-postgres psql -U postgres interview_trainer -c "SELECT COUNT(*) FROM questions;"

# Восстановите из бэкапа
python3 scripts/import_questions_from_json.py backup.json
```
