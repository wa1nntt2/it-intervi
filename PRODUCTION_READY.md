# 🚀 Production Подготовка

## ✅ Чек-лист для Production

### 1. Очистка тестовых данных

```bash
cd backend
source venv/bin/activate

# Удаляем все вопросы (оставляем только профессии)
python3 -c "
from app.database.engine import SessionLocal
from app.models.question import Question
from app.models.answer import Answer
db = SessionLocal()
db.query(Answer).delete()
db.query(Question).delete()
db.commit()
db.close()
"
```

### 2. Production инициализация

```bash
# Создаём БД с профессиями (без вопросов!)
python3 ../scripts/init_production.py
```

### 3. Делаем бэкап чистой БД

```bash
./scripts/backup_db.sh
```

### 4. Добавляем вопросы

**Через админку:**
```
http://localhost:3000/admin → Вопросы → Добавить
```

**Или импортом:**
```bash
python3 ../scripts/import_questions_from_json.py <файл-с-вопросами.json>
```

### 5. Финальный бэкап

```bash
./scripts/backup_db.sh
```

---

## 📁 Production файлы

| Файл | Назначение |
|------|------------|
| `scripts/init_production.py` | Инициализация БД (без вопросов) |
| `scripts/backup_db.sh` | Бэкап БД |
| `scripts/import_questions_from_json.py` | Импорт вопросов |
| `scripts/export_questions.py` | Экспорт вопросов |
| `backend/interview_trainer.db` | Production БД |

---

## 🔐 Production настройки

### .env.production

```bash
# Database
DATABASE_URL=sqlite:///./interview_trainer.db

# Security - ОБЯЗАТЕЛЬНО измените!
SECRET_KEY=<сгенерируйте: openssl rand -hex 32>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
CORS_ORIGINS=https://yourdomain.com
CORS_ALLOW_CREDENTIALS=true

# Production
DEBUG=false
```

### Docker Compose (production)

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    volumes:
      - backend_data:/app/data
    environment:
      - DATABASE_URL=sqlite:///./data/interview_trainer.db
      - SECRET_KEY=${SECRET_KEY}
      - DEBUG=false
    restart: always

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: always

volumes:
  backend_data:
```

---

## 🛡 Безопасность

### Обязательно:

1. **Смените SECRET_KEY**
   ```bash
   openssl rand -hex 32
   ```

2. **Смените пароль админа**
   ```
   http://localhost:3000/admin
   ```

3. **Установите DEBUG=false**

4. **Настройте HTTPS**

5. **Регулярные бэкапы**
   ```bash
   # Добавьте в crontab
   0 2 * * * /path/to/scripts/backup_db.sh
   ```

---

## 📊 Monitoring

### Проверка здоровья:

```bash
curl http://localhost:8000/health
# {"status":"healthy"}
```

### Статистика:

```bash
curl http://localhost:8000/api/sessions/stats
```

---

## 🎯 Итог

**Production БД должна содержать:**
- ✅ Пользователи (admin и другие)
- ✅ Профессии (4 штуки)
- ✅ Достижения (8 штук)
- ✅ Вопросы (те которые вы добавили)
- ✅ Сессии (пользователей)

**НЕ должна:**
- ❌ Пустых таблиц
- ❌ Тестовых данных
- ❌ Дефолтных паролей (кроме первого админа)

---

**🚀 Готово к production!**
