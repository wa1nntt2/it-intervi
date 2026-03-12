#!/bin/bash

set -e

cd "$(dirname "$0")/../frontend"

if [ ! -d "node_modules" ]; then
    echo "❌ Node modules not found. Run scripts/setup.sh first."
    exit 1
fi

echo "🚀 Запуск frontend сервера..."
npm run dev
