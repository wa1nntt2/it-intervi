# 📝 Шаблон для добавления вопросов

## 📁 Файл шаблона

Пустой шаблон для добавления вопросов: [`questions_template.json`](./questions_template.json)

---

## 📋 Структура вопроса

### Обязательные поля

| Поле | Тип | Описание |
|------|-----|----------|
| `text` | string | Текст вопроса |
| `question_type` | string | Тип вопроса: `"mcq"` или `"ordering"` |
| `difficulty` | string | Уровень сложности |
| `options` | array | Варианты ответов (массив строк) |
| `profession_name` | string | Название профессии |

### Поля для MCQ (Multiple Choice)

| Поле | Тип | Описание |
|------|-----|----------|
| `correct_option` | number | Индекс правильного ответа (0-3) |
| `correct_order` | null | Всегда `null` для MCQ |

### Поля для Ordering (упорядочивание)

| Поле | Тип | Описание |
|------|-----|----------|
| `correct_option` | null | Всегда `null` для ordering |
| `correct_order` | array | Правильный порядок индексов (например, `[0, 1, 2, 3]`) |

### Необязательные поля

| Поле | Тип | Описание |
|------|-----|----------|
| `explanation` | string | Пояснение к правильному ответу |

---

## 🎓 Допустимые значения

### question_type
- `"mcq"` — Multiple Choice (один правильный ответ)
- `"ordering"` — Упорядочивание элементов

### difficulty
- `"intern"` — Стажер
- `"junior"` — Джуниор
- `"middle"` — Мидл

### profession_name
- `"Frontend Developer"`
- `"Backend Developer"`
- `"Fullstack Developer"`
- `"DevOps Engineer"`

---

## 📌 Примеры

### Пример 1: MCQ вопрос (Multiple Choice)

```json
{
  "text": "Что такое Virtual DOM в React?",
  "question_type": "mcq",
  "difficulty": "junior",
  "options": [
    "Прямая копия реального DOM",
    "Легковесная копия DOM в памяти, используемая для оптимизации",
    "Способ создания DOM элементов",
    "Библиотека для работы с DOM"
  ],
  "correct_option": 1,
  "correct_order": null,
  "explanation": "Virtual DOM - это легковесная копия реального DOM, которая хранится в памяти и используется React для оптимизации обновлений.",
  "profession_name": "Frontend Developer"
}
```

### Пример 2: Ordering вопрос (упорядочивание)

```json
{
  "text": "Расположите уровни OSI модели (снизу вверх)",
  "question_type": "ordering",
  "difficulty": "junior",
  "options": [
    "Physical",
    "Network",
    "Transport",
    "Application"
  ],
  "correct_option": null,
  "correct_order": [0, 1, 2, 3],
  "explanation": "Уровни OSI: 1. Physical, 2. Data Link, 3. Network, 4. Transport, 5. Session, 6. Presentation, 7. Application.",
  "profession_name": "Backend Developer"
}
```

### Пример 3: Простой MCQ

```json
{
  "text": "Какой метод HTTP используется для получения данных?",
  "question_type": "mcq",
  "difficulty": "intern",
  "options": [
    "POST",
    "GET",
    "PUT",
    "DELETE"
  ],
  "correct_option": 1,
  "correct_order": null,
  "explanation": "GET — метод HTTP для получения данных с сервера.",
  "profession_name": "Backend Developer"
}
```

---

## 🚀 Как добавить вопросы

### Шаг 1: Скопируйте шаблон

```bash
cp docs/questions_template.json my_questions.json
```

### Шаг 2: Заполните вопросы

Отредактируйте `my_questions.json`, добавив свои вопросы в массив `questions`.

### Шаг 3: Проверьте JSON

```bash
python3 -c "import json; json.load(open('my_questions.json'))"
# Если ошибок нет — файл валиден
```

### Шаг 4: Импортируйте вопросы

```bash
cd backend
source venv/bin/activate
python3 ../scripts/import_questions_from_json.py ../my_questions.json
```

---

## ✅ Проверка после импорта

```bash
# Через API
curl http://localhost:8000/api/questions/ | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'Всего вопросов: {d[\"meta\"][\"total\"]}')"

# Через SQL
docker exec it-interview-postgres psql -U postgres interview_trainer -c "SELECT COUNT(*) FROM questions;"
```

---

## ⚠️ Важные замечания

1. **Индексы начинаются с 0**: `correct_option: 0` — это первый вариант в массиве `options`
2. **Для ordering**: `correct_order` должен содержать все индексы от 0 до N-1
3. **Уникальность**: Вопросы с одинаковым текстом не дублируются при импорте
4. **Бэкап**: Перед импортом сделайте бэкап текущих вопросов

---

## 📊 Статистика

| Профессия | ID | Категории |
|-----------|----|-----------|
| Frontend | 1 | HTML & CSS, JavaScript, React, Vue, Angular, TypeScript, CSS Frameworks, Build Tools |
| Backend | 2 | Python, Базы данных, API Design, Архитектура, Безопасность, Кэширование, Микросервисы, Тестирование |
| Fullstack | 3 | Frontend + Backend, Архитектура приложений, Базы данных, DevOps основы, API Integration, Аутентификация, Deployment, Производительность |
| DevOps | 4 | **Linux**, Docker, Kubernetes, CI/CD, Infrastructure as Code, Мониторинг, Сети, Безопасность, Git, Scripting |

**Вопросы по Linux:** 60 вопросов (Intern: 20, Junior: 20, Middle: 20)
