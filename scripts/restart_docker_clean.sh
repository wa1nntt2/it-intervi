#!/bin/bash
# Перезапуск Docker контейнеров с очисткой старого volume

set -e

echo "🔄 Остановка контейнеров..."
docker-compose down

echo "🔄 Удаление старого volume с БД..."
docker volume rm it_interVI.it-interview-trainer_backend_data 2>/dev/null || echo "✅ Volume уже удален"

echo "🔄 Запуск контейнеров..."
docker-compose up -d

sleep 5

echo "🔄 Проверка..."
docker-compose ps

echo ""
echo "✅ Контейнеры перезапущены!"
echo ""
echo "📊 Проверка количества вопросов:"
echo "   curl http://localhost:8000/api/questions/ | jq '.meta.total'"
echo ""
echo "📝 Если вопросов > 0, выполните:"
echo "   docker-compose exec backend python -c \""
echo "   from app.database.engine import SessionLocal"
echo "   from app.models.question import Question"
echo "   from app.models.answer import Answer"
echo "   db = SessionLocal()"
echo "   db.query(Answer).delete()"
echo "   db.query(Question).delete()"
echo "   db.commit()"
echo "   print('✅ Вопросы удалены')"
echo "   \""
