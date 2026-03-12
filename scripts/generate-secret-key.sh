#!/bin/bash

# Скрипт генерации SECRET_KEY и создания .env файла

set -e

echo "🔑 Генерация SECRET_KEY..."

# Генерируем случайный ключ
SECRET_KEY=$(openssl rand -hex 32)

# Создаем .env файл из .env.example
cp .env.example .env

# Заменяем пустой SECRET_KEY на сгенерированный
sed -i "s/^SECRET_KEY=.*/SECRET_KEY=${SECRET_KEY}/" .env

echo "✅ .env файл создан!"
echo ""
echo "Ваш SECRET_KEY: ${SECRET_KEY}"
echo ""
echo "Храните этот ключ в безопасном месте!"
echo "Для production используйте уникальный ключ для каждого сервера."
