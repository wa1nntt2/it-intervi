# 🛡 Защита вопросов от потери - Чек-лист

## ✅ Сделано для защиты

| Что сделано | Статус | Описание |
|-------------|--------|----------|
| Seed данные обновлены | ✅ | В `backend/app/database/seed.py` добавлены DevOps вопросы |
| Скрипт импорта | ✅ | `scripts/import_all_devops_questions.py` - 129 вопросов |
| Alembic миграции | ✅ | Управление схемой БД через миграции |
| Экспорт в JSON | ✅ | `scripts/export_questions.py` - выгрузка всех вопросов |
| Импорт из JSON | ✅ | `scripts/import_questions_from_json.py` - восстановление |
| Авто-бэкап | ✅ | `scripts/backup_questions.sh` - ежедневный бэкап |
| Документация | ✅ | `docs/QUESTIONS_MANAGEMENT.md` - полная инструкция |

---

## 📍 Где теперь вопросы

**Основная БД:** `backend/interview_trainer.db` (141 вопрос)

**Бэкапы:**
- `scripts/questions_backup.json` - ручной бэкап
- `backups/questions_latest.json` - последний авто-бэкап
- `backups/questions_*.json` - история бэкапов

---

## 🎯 Что нужно делать регулярно

### Ежедневно (автоматически)
```bash
# Cron запускает бэкап в 2:00 ночи
0 2 * * * /home/vboxuser/it_interVI.it-interview-trainer/scripts/backup_questions.sh
```

### Перед любыми изменениями
```bash
cd backend
source venv/bin/activate
python3 ../scripts/export_questions.py > ../scripts/questions_backup_manual.json
```

### Для добавления вопросов
1. Создайте скрипт по аналогии с `scripts/import_all_devops_questions.py`
2. Запустите: `python3 scripts/your_script.py`
3. Проверьте: `curl http://localhost:8000/api/questions/`

---

## ⚠️ Если вопросы пропали - план действий

```bash
# 1. Проверьте БД напрямую
cd backend && source venv/bin/activate
python3 -c "from sqlalchemy import create_engine, text; e=create_engine('sqlite:///./interview_trainer.db'); print('Вопросов:', e.connect().execute(text('SELECT COUNT(*) FROM questions')).scalar())"

# 2. Если 0 - восстановите из бэкапа
python3 ../scripts/import_questions_from_json.py ../backups/questions_latest.json

# 3. Перезапустите backend
sudo pkill -f "uvicorn app.main:app"
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 📊 Текущая статистика

```
Frontend:  6 вопросов
Backend:   4 вопросов
Fullstack: 2 вопросов
DevOps:    129 вопросов
═════════════════════════
Итого:     141 вопросов
```

---

## 🔧 Быстрые команды

```bash
# Проверить количество вопросов
curl http://localhost:8000/api/questions/?profession_id=4 | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'DevOps: {d[\"meta\"][\"total\"]}')"

# Сделать бэкап
./scripts/backup_questions.sh

# Восстановить из бэкапа
cd backend && source venv/bin/activate && python3 ../scripts/import_questions_from_json.py ../backups/questions_latest.json
```

---

**🎉 Теперь вопросы под защитой!**
