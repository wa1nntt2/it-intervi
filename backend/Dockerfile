FROM python:3.11-slim

WORKDIR /app

# Копируем требования сначала для кэширования слоев
COPY requirements*.txt ./

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY . .

# Создаем директорию для БД
RUN mkdir -p /app/data

# Переменная окружения для миграций
ENV SKIP_MIGRATIONS=false

# Health check для проверки работоспособности
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Открываем порт
EXPOSE 8000

# Запускаем приложение
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
