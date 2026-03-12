#!/bin/bash
# Перезапуск backend с очисткой кэша

echo "🔄 Остановка старых процессов uvicorn..."
sudo pkill -9 -f "uvicorn app.main:app"

sleep 2

echo "🔄 Запуск backend..."
cd /home/vboxuser/it_interVI.it-interview-trainer/backend
source venv/bin/activate

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &

sleep 3

echo "✅ Backend запущен!"
echo "📊 Проверка: curl http://localhost:8000/api/questions/ | jq '.meta.total'"
