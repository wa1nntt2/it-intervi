# 🎯 Простое управление данными в IT Interview Trainer

## ✅ Теперь ВСЁ в базе данных!

Все данные хранятся в одном файле:
```
backend/interview_trainer.db
```

---

## 🚀 Быстрый старт

### Первый запуск (пустая БД)

```bash
# 1. Применяем миграции (создаём таблицы)
cd backend
source venv/bin/activate
python migrate.py upgrade

# 2. Инициализируем данные (ОДИН РАЗ!)
python3 ../scripts/init_database.py

# 3. Запускаем backend
uvicorn app.main:app --reload
```

**Готово!** После этого:
- ✅ Администратор создан (admin@example.com / admin123)
- ✅ 4 профессии создано
- ✅ Начальные вопросы добавлены
- ✅ Достижения созданы

---

## 📊 Что хранится в БД

| Таблица | Данные |
|---------|--------|
| `users` | Пользователи (admin и другие) |
| `professions` | Профессии (Frontend, Backend, etc.) |
| `questions` | Вопросы для собеседований |
| `achievements` | Достижения |
| `sessions` | Сессии тестирования |
| `answers` | Ответы пользователей |

---

## 🛡 Бэкап (очень просто!)

### Быстрый бэкап

```bash
./scripts/backup_db.sh
```

**Что делает:**
- Копирует `backend/interview_trainer.db` в `backups/`
- Создает ссылку `backups/interview_trainer_latest.db`
- Хранит последние 10 бэкапов

### Ручной бэкап

```bash
# Просто скопируйте файл!
cp backend/interview_trainer.db backup.db
cp backend/interview_trainer.db backup_$(date +%Y%m%d).db
```

---

## ➕ Добавление вопросов

### Способ 1: Через админку (рекомендуется)

```
http://localhost:3000/admin
→ Вопросы → Добавить вопрос
```

**После добавления сделайте бэкап:**
```bash
./scripts/backup_db.sh
```

### Способ 2: Через скрипт импорта

```bash
cd backend
source venv/bin/activate
python3 ../scripts/import_questions_from_json.py ../scripts/questions_full_backup.json
```

---

## 🔄 Восстановление из бэкапа

### Если БД повреждена или удалена

```bash
# 1. Остановите backend
pkill -f "uvicorn app.main:app"

# 2. Восстановите из бэкапа
cp backups/interview_trainer_latest.db backend/interview_trainer.db

# 3. Запустите backend
cd backend && source venv/bin/activate
uvicorn app.main:app --reload
```

---

## 📋 Чек-лист

### ✅ При каждом запуске

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

### ✅ Перед изменениями

```bash
./scripts/backup_db.sh
```

### ✅ После добавления вопросов через админку

```bash
./scripts/backup_db.sh
```

### ✅ Если вопросы пропали

```bash
# Проверьте БД
cd backend && source venv/bin/activate
python3 -c "from sqlalchemy import create_engine, text; e=create_engine('sqlite:///./interview_trainer.db'); print('Вопросов:', e.connect().execute(text('SELECT COUNT(*) FROM questions')).scalar())"

# Если 0 - восстановите из бэкапа
cp ../backups/interview_trainer_latest.db interview_trainer.db
```

---

## 📁 Структура скриптов

```
scripts/
├── init_database.py          # Первичная инициализация (1 раз)
├── backup_db.sh              # Быстрый бэкап БД
├── export_questions.py       # Экспорт вопросов в JSON
├── import_questions_from_json.py  # Импорт вопросов из JSON
└── questions_full_backup.json     # Бэкап вопросов (JSON)
```

---

## 🔐 Данные по умолчанию

### Администратор
- **Email:** admin@example.com
- **Пароль:** admin123

### Профессии
1. Frontend Developer
2. Backend Developer
3. Fullstack Developer
4. DevOps Engineer

---

## ⚠️ Важно!

### ✅ ДЕЛАЙТЕ:
- Бэкап перед любыми изменениями
- Бэкап после добавления вопросов через админку
- Запускайте backend из директории `backend/`
- Используйте `venv`

### ❌ НЕ ДЕЛАЙТЕ:
- Не удаляйте `backend/interview_trainer.db` вручную
- Не редактируйте БД напрямую без бэкапа
- Не запускайте backend из корневой директории

---

## 🎉 Готово!

Теперь все данные в БД и управляются просто!

**Бэкап = копия файла БД** 🎉
