# 📚 Управление вопросами в IT Interview Trainer

## 📍 Где хранятся вопросы

**Основная база данных:**
```
backend/interview_trainer.db
```

Это SQLite файл, который содержит ВСЕ данные:
- Вопросы (таблица `questions`)
- Профессии (таблица `professions`)
- Пользователи (таблица `users`)
- Сессии (таблица `sessions`)
- Достижения (таблица `achievements`)

---

## ⚠️ Почему вопросы могут "пропасть"

### Причина 1: Seed данные не обновляются
В `backend/app/database/seed.py` стоит проверка:
```python
if not db.query(Question).filter(...).first():
    # Вопросы создаются ТОЛЬКО если их нет
```

**Вывод:** Если вопросы уже есть в БД, новые НЕ добавятся автоматически.

### Причина 2: Несколько файлов БД
- `backend/interview_trainer.db` ← **основная**
- `backend/data/interview_trainer.db` ← для Docker
- `interview_trainer.db` ← в корне (не используется)

**Вывод:** При запуске из разных директорий может создаться новая пустая БД.

### Причина 3: Ручное удаление БД
```bash
# ❌ НЕ ДЕЛАЙТЕ ТАК:
rm backend/interview_trainer.db
```

**Вывод:** Все вопросы будут потеряны!

---

## ✅ Как правильно управлять вопросами

### 1. Экспорт вопросов (БЭКАП)

**Перед любыми изменениями делайте бэкап!**

```bash
cd backend
source venv/bin/activate
python3 ../scripts/export_questions.py > ../scripts/questions_backup.json
```

Проверка бэкапа:
```bash
python3 -c "import json; d=json.load(open('scripts/questions_backup.json')); print(f'Вопросов: {d[\"total\"]}')"
```

### 2. Импорт вопросов

Если нужно восстановить вопросы из бэкапа:

```bash
cd backend
source venv/bin/activate
python3 ../scripts/import_questions_from_json.py ../scripts/questions_backup.json
```

### 3. Добавление новых вопросов

#### Вариант А: Через скрипт (рекомендуется)

Создайте скрипт по аналогии с `scripts/import_all_devops_questions.py`:

```python
#!/usr/bin/env python3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.profession import Profession
from app.models.question import Question

engine = create_engine('sqlite:///./interview_trainer.db')
db = SessionLocal()

# Новые вопросы
new_questions = [
    {
        "text": "Ваш вопрос?",
        "profession_name": "DevOps Engineer",
        "difficulty": "intern",
        "options": ["Ответ 1", "Ответ 2", "Ответ 3", "Ответ 4"],
        "correct_option": 0,
        "explanation": "Пояснение к ответу"
    },
    # ... больше вопросов
]

# Кэш профессий
professions_cache = {p.name: p.id for p in db.query(Profession).all()}

for q_data in new_questions:
    profession_id = professions_cache.get(q_data["profession_name"])
    if not profession_id:
        print(f"Профессия не найдена: {q_data['profession_name']}")
        continue
    
    question = Question(
        text=q_data["text"],
        question_type="mcq",
        profession_id=profession_id,
        difficulty=q_data["difficulty"],
        options=q_data["options"],
        correct_option=q_data["correct_option"],
        explanation=q_data.get("explanation", "")
    )
    db.add(question)

db.commit()
db.close()
```

#### Вариант Б: Через админ-панель

Используйте веб-интерфейс: `http://localhost:3000/admin`

### 4. Проверка количества вопросов

```bash
# Через API
curl http://localhost:8000/api/questions/?profession_id=4 | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'DevOps: {d[\"meta\"][\"total\"]}')"

# profession_id: 1=Frontend, 2=Backend, 3=Fullstack, 4=DevOps
```

Или через SQL:
```bash
cd backend
source venv/bin/activate
python3 -c "
from sqlalchemy import create_engine, text
engine = create_engine('sqlite:///./interview_trainer.db')
with engine.connect() as conn:
    result = conn.execute(text('SELECT p.name, COUNT(q.id) FROM professions p LEFT JOIN questions q ON p.id = q.profession_id GROUP BY p.name'))
    for row in result:
        print(f'{row[0]}: {row[1]} вопросов')
"
```

---

## 📋 Чек-лист перед запуском

1. **Проверьте что запускаетесь из правильной директории:**
   ```bash
   pwd  # Должно быть: /home/vboxuser/it_interVI.it-interview-trainer/backend
   ```

2. **Активируйте venv:**
   ```bash
   source venv/bin/activate
   ```

3. **Проверьте БД:**
   ```bash
   ls -la interview_trainer.db  # Файл должен существовать
   ```

4. **Сделайте бэкап перед изменениями:**
   ```bash
   python3 ../scripts/export_questions.py > ../scripts/questions_backup_$(date +%Y%m%d).json
   ```

---

## 🔄 Если вопросы пропали

### Шаг 1: Проверьте БД
```bash
cd backend
source venv/bin/activate
python3 -c "
from sqlalchemy import create_engine, text
engine = create_engine('sqlite:///./interview_trainer.db')
with engine.connect() as conn:
    result = conn.execute(text('SELECT COUNT(*) FROM questions'))
    print(f'Вопросов в БД: {result.scalar()}')
"
```

### Шаг 2: Проверьте API
```bash
curl http://localhost:8000/api/questions/ | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'Вопросов через API: {d[\"meta\"][\"total\"]}')"
```

### Шаг 3: Восстановите из бэкапа
```bash
python3 ../scripts/import_questions_from_json.py ../scripts/questions_backup.json
```

### Шаг 4: Перезапустите backend
```bash
# Найдите PID
ps aux | grep uvicorn | grep -v grep

# Остановите (нужен sudo если процесс от root)
sudo pkill -f "uvicorn app.main:app"

# Запустите заново
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 📊 Текущая статистика вопросов

| Профессия | ID | Вопросов |
|-----------|----|----------|
| Frontend | 1 | 6 |
| Backend | 2 | 4 |
| Fullstack | 3 | 2 |
| DevOps | 4 | **129** |
| **Итого** | | **141** |

---

## 🛡 Профилактика проблем

### ✅ ДЕЛАЙТЕ:
1. Регулярный бэкап: `python3 ../scripts/export_questions.py > backup.json`
2. Запускайте backend из `backend/` директории
3. Используйте `venv` для Python
4. Проверяйте количество вопросов после изменений

### ❌ НЕ ДЕЛАЙТЕ:
1. Не удаляйте `backend/interview_trainer.db` вручную
2. Не запускайте backend из корневой директории проекта
3. Не редактируйте БД напрямую без бэкапа
4. Не полагайтесь только на seed данные

---

## 📞 Если что-то пошло не так

1. Проверьте логи backend
2. Проверьте что backend использует правильную БД:
   ```bash
   curl http://localhost:8000/health
   ```
3. Восстановите из бэкапа
4. Перезапустите backend

**Бэкап вопросов:** `scripts/questions_backup.json` (141 вопрос)
