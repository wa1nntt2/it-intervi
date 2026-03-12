#!/bin/bash

set -e

echo "🚀 Установка зависимостей IT Interview Trainer..."

# Backend
echo "📦 Установка backend зависимостей..."
cd backend
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt
cd ..

# Frontend
echo "📦 Установка frontend зависимостей..."
cd frontend
npm install
cd ..

echo "✅ Установка завершена!"
echo ""
echo "Для запуска backend:"
echo "  cd backend && source venv/bin/activate && uvicorn app.main:app --reload"
echo ""
echo "Для запуска frontend:"
echo "  cd frontend && npm run dev"
