#!/bin/bash
# Автоматический бэкап вопросов
# Добавить в crontab: 0 2 * * * /home/vboxuser/it_interVI.it-interview-trainer/scripts/backup_questions.sh

set -e

PROJECT_DIR="/home/vboxuser/it_interVI.it-interview-trainer"
BACKEND_DIR="$PROJECT_DIR/backend"
BACKUP_DIR="$PROJECT_DIR/backups"
DATE=$(date +%Y%m%d_%H%M%S)

# Создаем директорию для бэкапов
mkdir -p "$BACKUP_DIR"

echo "🔄 Начало бэкапа вопросов..."

# Активируем venv и экспортируем вопросы
cd "$BACKEND_DIR"
source venv/bin/activate
python3 ../scripts/export_questions.py > "$BACKUP_DIR/questions_$DATE.json"

# Проверяем что бэкап успешен
if [ -f "$BACKUP_DIR/questions_$DATE.json" ]; then
    COUNT=$(python3 -c "import json; print(json.load(open('$BACKUP_DIR/questions_$DATE.json'))['total'])")
    echo "✅ Бэкап создан: $BACKUP_DIR/questions_$DATE.json ($COUNT вопросов)"
    
    # Храним только последние 10 бэкапов
    ls -t "$BACKUP_DIR"/questions_*.json | tail -n +11 | xargs -r rm
    
    # Обновляем symlink на последний бэкап
    ln -sf "questions_$DATE.json" "$BACKUP_DIR/questions_latest.json"
    echo "✅ Ссылка обновлена: $BACKUP_DIR/questions_latest.json"
else
    echo "❌ Ошибка создания бэкапа!"
    exit 1
fi

echo "🎉 Бэкап завершен!"
