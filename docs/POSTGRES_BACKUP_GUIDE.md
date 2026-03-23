# 🛡️ Руководство по бэкапу PostgreSQL

## 📋 Оглавление

1. [Быстрый старт](#быстрый-старт)
2. [Создание бэкапа](#создание-бэкапа)
3. [Восстановление из бэкапа](#восстановление-из-бэкапа)
4. [Автоматизация](#автоматизация)
5. [Стратегия бэкапирования](#стратегия-бэкапирования)
6. [Troubleshooting](#troubleshooting)

---

## 🚀 Быстрый старт

### Создание бэкапа

```bash
# Простой бэкап (автоматически определит режим)
cd /home/vboxuser/it_interVI.it-interview-trainer
./scripts/backup_postgres.sh

# Бэкап через Docker Compose
./scripts/backup_postgres.sh --docker

# Бэкап в кастомный путь
./scripts/backup_postgres.sh --custom /mnt/backup/my_backup.sql.gz
```

### Восстановление из бэкапа

```bash
# Восстановить последний бэкап
./scripts/restore_postgres.sh --latest

# Восстановить конкретный файл
./scripts/restore_postgres.sh backups/postgresql/daily/interview_trainer_20260319_120000.sql.gz

# Через Docker
./scripts/restore_postgres.sh --docker --latest
```

---

## 📦 Создание бэкапа

### Режимы работы

| Режим | Описание | Когда использовать |
|-------|----------|-------------------|
| **standard** | Прямое подключение к PostgreSQL | Локальная БД |
| **--docker** | Через Docker Compose | Контейнеризированная БД |
| **--custom** | В свой путь | Внешнее хранилище |

### Примеры использования

```bash
# Стандартный бэкап
./scripts/backup_postgres.sh

# Бэкап через Docker (рекомендуется)
./scripts/backup_postgres.sh --docker

# Без сжатия (быстрее, но больше места)
./scripts/backup_postgres.sh --no-compress

# Подробный вывод
./scripts/backup_postgres.sh --verbose

# Бэкап в другую директорию
./scripts/backup_postgres.sh --custom /mnt/backup/pg_backup.sql.gz
```

### Переменные окружения

Создайте `.env` файл или установите переменные:

```bash
# PostgreSQL настройки
export PG_HOST=localhost
export PG_PORT=5433
export PG_USER=interview_admin
export PG_PASSWORD=ваш_пароль
export PG_DB=interview_trainer

# Или для Docker Compose
export POSTGRES_HOST=postgres
export POSTGRES_PORT=5432
export POSTGRES_USER=interview_admin
export POSTGRES_PASSWORD=ваш_пароль
export POSTGRES_DB=interview_trainer
```

### Структура бэкапов

```
backups/postgresql/
├── daily/           # Ежедневные бэкапы
│   ├── interview_trainer_20260319_020000.sql.gz
│   ├── interview_trainer_20260320_020000.sql.gz
│   └── ...
├── weekly/          # Недельные бэкапы (каждую пятницу)
│   ├── interview_trainer_week_12.sql.gz
│   └── ...
├── monthly/         # Месячные бэкапы (1-го числа)
│   ├── interview_trainer_202603.sql.gz
│   └── ...
└── latest.sql.gz    # Ссылка на последний бэкап
```

### Хранение бэкапов

По умолчанию хранятся:
- **Ежедневные**: 30 дней
- **Недельные**: 8 недель
- **Месячные**: 12 месяцев

Старые бэкапы удаляются автоматически.

---

## ♻️ Восстановление из бэкапа

### Просмотр доступных бэкапов

```bash
# Показать все доступные бэкапы
./scripts/restore_postgres.sh --list
```

Пример вывода:
```
=============================================================================
📦 Доступные бэкапы
=============================================================================

ℹ️  Последние бэкапы:

  📁 daily/ (ежедневные):
     interview_trainer_20260319_140000.sql.gz (2.4M, мар 19 14:00)
     interview_trainer_20260319_020000.sql.gz (2.3M, мар 19 02:00)
     ...

  📁 weekly/ (недельные):
     interview_trainer_week_12.sql.gz (2.5M, мар 15 02:00)
     ...

  📁 monthly/ (месячные):
     interview_trainer_202603.sql.gz (10M, мар 1 02:00)
     ...

  🔗 latest.sql.gz -> interview_trainer_20260319_140000.sql.gz
```

### Восстановление

```bash
# ⚠️  Внимание: Восстановление заменит все данные!

# Восстановить последний бэкап
./scripts/restore_postgres.sh --latest

# Восстановить конкретный файл
./scripts/restore_postgres.sh backups/postgresql/daily/interview_trainer_20260319_120000.sql.gz

# Через Docker
./scripts/restore_postgres.sh --docker --latest

# Тестовый запуск (без изменений)
./scripts/restore_postgres.sh --latest --dry-run

# Без подтверждения (для скриптов)
./scripts/restore_postgres.sh --latest --force
```

### Проверка после восстановления

```bash
# Подключиться к БД и проверить данные
docker-compose -f docker-compose.postgres.yml exec postgres \
  psql -U interview_admin -d interview_trainer -c "SELECT COUNT(*) FROM users;"

# Или напрямую
psql -h localhost -p 5433 -U interview_admin -d interview_trainer -c "SELECT COUNT(*) FROM users;"
```

---

## ⏰ Автоматизация

### Настройка cron для ежедневного бэкапа

```bash
# Открываем crontab
crontab -e

# Добавляем ежедневный бэкап в 2:00
0 2 * * * /home/vboxuser/it_interVI.it-interview-trainer/scripts/backup_postgres.sh --docker >> /var/log/pg_backup.log 2>&1

# Еженедельный бэкап в пятницу в 3:00
0 3 * * 5 /home/vboxuser/it_interVI.it-interview-trainer/scripts/backup_postgres.sh --docker --custom /mnt/backup/weekly_backup.sql.gz

# Ежемесячный бэкап 1-го числа в 4:00
0 4 1 * * /home/vboxuser/it_interVI.it-interview-trainer/scripts/backup_postgres.sh --docker --custom /mnt/backup/monthly_backup.sql.gz
```

### Systemd timer (альтернатива cron)

Создайте сервис:

```ini
# /etc/systemd/system/pg-backup.service
[Unit]
Description=PostgreSQL Backup for IT Interview Trainer
After=docker.service

[Service]
Type=oneshot
User=vboxuser
WorkingDirectory=/home/vboxuser/it_interVI.it-interview-trainer
ExecStart=/home/vboxuser/it_interVI.it-interview-trainer/scripts/backup_postgres.sh --docker
Environment="PATH=/usr/bin:/usr/local/bin"
```

Создайте таймер:

```ini
# /etc/systemd/system/pg-backup.timer
[Unit]
Description=Run PostgreSQL Backup daily at 2:00

[Timer]
OnCalendar=*-*-* 02:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

Активируйте:

```bash
sudo systemctl daemon-reload
sudo systemctl enable pg-backup.timer
sudo systemctl start pg-backup.timer
sudo systemctl list-timers  # Проверка
```

---

## 📊 Стратегия бэкапирования

### Правило 3-2-1

✅ **3** копии данных (оригинал + 2 бэкапа)  
✅ **2** разных типа носителей (диск + облако)  
✅ **1** копия вне площадки (offsite)

### Рекомендуемая стратегия

| Частота | Тип | Хранение |Retention |
|---------|-----|----------|----------|
| **Ежедневно** | Полный | Локально | 30 дней |
| **Еженедельно** | Полный | Внешний диск | 8 недель |
| **Ежемесячно** | Полный | Облако | 12 месяцев |

### Внешние хранилища

#### 1. Внешний USB диск

```bash
# Смонтируйте диск в /mnt/backup
# Добавьте в /etc/fstab для авто-монтирования
UUID=xxxx-xxxx /mnt/backup ext4 defaults,noatime 0 2

# Бэкап на внешний диск
./scripts/backup_postgres.sh --custom /mnt/backup/pg_backup_$(date +%Y%m%d).sql.gz
```

#### 2. Облачное хранилище (S3)

```bash
# Установите AWS CLI
pip install awscli

# Бэкап в S3
./scripts/backup_postgres.sh --custom /tmp/backup.sql.gz
aws s3 cp /tmp/backup.sql.gz s3://your-bucket/pg-backups/backup_$(date +%Y%m%d).sql.gz
```

#### 3. Удаленный сервер (rsync + SSH)

```bash
# Бэкап локально
./scripts/backup_postgres.sh

# Синхронизация с удаленным сервером
rsync -avz -e ssh backups/postgresql/ user@remote-server:/backups/pg/
```

---

## 🔧 Troubleshooting

### Ошибка: "pg_dump: command not found"

**Решение:**
```bash
# Установите PostgreSQL клиент
sudo apt-get install postgresql-client

# Или используйте Docker режим
./scripts/backup_postgres.sh --docker
```

### Ошибка: "password authentication failed"

**Решение:**
```bash
# Проверьте пароль в .env
cat .env | grep POSTGRES_PASSWORD

# Установите правильный пароль
export POSTGRES_PASSWORD=ваш_пароль
```

### Ошибка: "connection refused"

**Решение:**
```bash
# Проверьте что PostgreSQL запущен
docker-compose -f docker-compose.postgres.yml ps

# Или для локальной БД
sudo systemctl status postgresql

# Проверьте порт
netstat -tlnp | grep 5432
```

### Бэкап слишком большой

**Решение:**
```bash
# Используйте сжатие (по умолчанию включено)
./scripts/backup_postgres.sh

# Исключите большие таблицы
pg_dump -h localhost -U user -d dbname --exclude-table=large_table > backup.sql
```

### Восстановление не работает

**Решение:**
```bash
# Проверьте целостность бэкапа
gzip -t backup.sql.gz

# Проверьте логи
docker-compose -f docker-compose.postgres.yml logs postgres

# Попробуйте восстановить в тестовую БД
createdb test_restore
./scripts/restore_postgres.sh --latest --force
```

---

## 📈 Мониторинг бэкапов

### Проверка последних бэкапов

```bash
# Показать последние 5 бэкапов
ls -lht backups/postgresql/daily/ | head -5

# Проверить размер последнего бэкапа
du -h backups/postgresql/latest.sql.gz

# Проверить дату последнего бэкапа
stat backups/postgresql/latest.sql.gz | grep Modify
```

### Alert если бэкап не создан

```bash
#!/bin/bash
# check_backup.sh

BACKUP_DIR="backups/postgresql/daily"
MAX_AGE_HOURS=25

# Найти последний бэкап
LATEST=$(ls -t "$BACKUP_DIR"/*.sql.gz 2>/dev/null | head -1)

if [ -z "$LATEST" ]; then
    echo "❌ Бэкапы не найдены!"
    exit 1
fi

# Проверить возраст
FILE_AGE=$(find "$LATEST" -mmin -$((MAX_AGE_HOURS * 60)))

if [ -z "$FILE_AGE" ]; then
    echo "❌ Последний бэкап старше $MAX_AGE_HOURS часов!"
    exit 1
fi

echo "✅ Бэкап актуален: $LATEST"
exit 0
```

Добавьте в cron для ежедневной проверки:

```bash
0 8 * * * /home/vboxuser/it_interVI.it-interview-trainer/scripts/check_backup.sh
```

---

## 🔐 Безопасность бэкапов

### Шифрование бэкапов

```bash
# Генерация GPG ключа
gpg --gen-key

# Шифрование бэкапа
./scripts/backup_postgres.sh --encrypt

# Расшифровка
gpg --decrypt backup.sql.gz.gpg > backup.sql.gz
```

### Защита файлов бэкапов

```bash
# Установите правильные права
chmod 600 backups/postgresql/**/*.sql.gz
chown vboxuser:vboxuser backups/postgresql/

# Для директории
chmod 700 backups/postgresql/
```

### Удаление старых бэкапов

```bash
# Безопасное удаление (затирание)
shred -u backup.sql.gz

# Или для всей директории
find backups/postgresql/daily/ -name "*.sql.gz" -mtime +30 -exec shred -u {} \;
```

---

## 📚 Дополнительные ресурсы

- [PostgreSQL Backup](https://www.postgresql.org/docs/backup.html)
- [pg_dump документация](https://www.postgresql.org/docs/current/app-pgdump.html)
- [pgBackRest](https://pgbackrest.org/) - продвинутая система бэкапов
- [Barman](https://www.pgbarman.org/) - enterprise бэкапирование

---

**✅ Готово!** Теперь вы можете надежно бэкапить и восстанавливать вашу базу данных!
