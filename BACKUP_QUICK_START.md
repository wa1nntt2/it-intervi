# 🛡️ Бэкап базы данных - Краткое руководство

## SQLite (разработка)

```bash
# Быстрый бэкап
./scripts/backup_db.sh

# Результат в backups/
```

## PostgreSQL (production)

### Создание бэкапа

```bash
# Простой бэкап
./scripts/backup_postgres.sh

# Через Docker Compose (рекомендуется)
./scripts/backup_postgres.sh --docker

# В кастомный путь
./scripts/backup_postgres.sh --custom /mnt/backup/backup.sql.gz
```

### Восстановление

```bash
# Показать доступные бэкапы
./scripts/restore_postgres.sh --list

# Восстановить последний
./scripts/restore_postgres.sh --latest

# Восстановить конкретный файл
./scripts/restore_postgres.sh backups/postgresql/daily/backup_20260319.sql.gz

# Через Docker
./scripts/restore_postgres.sh --docker --latest
```

### Автоматизация

```bash
# Добавить в crontab (ежедневный бэкап в 2:00)
crontab -e
0 2 * * * /home/vboxuser/it_interVI.it-interview-trainer/scripts/backup_postgres.sh --docker
```

## Структура бэкапов

```
backups/
├── postgresql/
│   ├── daily/           # Ежедневные бэкапы
│   ├── weekly/          # Недельные бэкапы
│   ├── monthly/         # Месячные бэкапы
│   └── latest.sql.gz    # Последний бэкап (symlink)
└── interview_trainer_*.db  # SQLite бэкапы
```

## Переменные окружения

Добавьте в `.env`:

```bash
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_USER=interview_admin
POSTGRES_PASSWORD=ваш_пароль
POSTGRES_DB=interview_trainer
```

## 📚 Полная документация

[docs/POSTGRES_BACKUP_GUIDE.md](docs/POSTGRES_BACKUP_GUIDE.md)
