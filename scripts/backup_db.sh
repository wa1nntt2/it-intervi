#!/bin/bash
# Простой бэкап базы данных
# Использование: ./scripts/backup_db.sh

set -e

PROJECT_DIR="/home/vboxuser/it_interVI.it-interview-trainer"
BACKEND_DIR="$PROJECT_DIR/backend"
BACKUP_DIR="$PROJECT_DIR/backups"
DATE=$(date +%Y%m%d_%H%M%S)

# Создаем директорию для бэкапов
mkdir -p "$BACKUP_DIR"

echo "🔄 Бэкап базы данных..."

# Копируем файл БД
cp "$BACKEND_DIR/interview_trainer.db" "$BACKUP_DIR/interview_trainer_$DATE.db"

# Создаем symlink на последний бэкап
ln -sf "interview_trainer_$DATE.db" "$BACKUP_DIR/interview_trainer_latest.db"

# Показываем результат
ls -lh "$BACKUP_DIR/interview_trainer_$DATE.db"

echo "✅ Бэкап создан: $BACKUP_DIR/interview_trainer_$DATE.db"
echo "✅ Ссылка: $BACKUP_DIR/interview_trainer_latest.db"

# Удаляем старые бэкапы (храним последние 10)
cd "$BACKUP_DIR"
ls -t interview_trainer_*.db 2>/dev/null | tail -n +11 | xargs -r rm

echo "🎉 Готово!"
