#!/bin/bash

set -e

# Загружаем .env файл из корня проекта
if [ -f "../.env" ]; then
    echo "Loading environment variables from .env..."
    set -a
    source ../.env
    set +a
elif [ -f ".env" ]; then
    echo "Loading environment variables from .env..."
    set -a
    source .env
    set +a
else
    echo "Warning: .env file not found, using default values"
fi

cd "$(dirname "$0")/../backend"

if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Run scripts/setup.sh first."
    exit 1
fi

source venv/bin/activate

echo "🚀 Запуск backend сервера..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
