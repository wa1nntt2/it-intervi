-- Инициализация PostgreSQL для IT Interview Trainer
-- Этот скрипт выполняется при первом запуске контейнера

-- Включаем расширение для UUID (если понадобится в будущем)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Создаем пользователя для приложения (если не создан через env variables)
-- Внимание: в production используйте сложные пароли!
-- DO $$
-- BEGIN
--   IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'interview_admin') THEN
--     CREATE ROLE interview_admin WITH LOGIN PASSWORD 'change_this_password_in_production';
--   END IF;
-- END
-- $$;

-- Предоставляем права на базу данных
-- GRANT ALL PRIVILEGES ON DATABASE interview_trainer TO interview_admin;

-- Настройка search_path для приложения
-- ALTER ROLE interview_admin SET search_path TO public;

-- Логирование медленных запросов (для отладки)
ALTER SYSTEM SET log_min_duration_statement = 1000;  -- Логировать запросы > 1 секунды

-- Настройка соединений
ALTER SYSTEM SET max_connections = 100;

-- Настройка работы с памятью
ALTER SYSTEM SET shared_buffers = '256MB';  -- 25% от доступной памяти (для контейнера с 1GB)
ALTER SYSTEM SET effective_cache_size = '512MB';  -- 50% от доступной памяти
ALTER SYSTEM SET work_mem = '16MB';  -- Для сортировок и hash таблиц

-- Настройка автовакуума (важно для production)
ALTER SYSTEM SET autovacuum = on;
ALTER SYSTEM SET autovacuum_max_workers = 3;
ALTER SYSTEM SET autovacuum_naptime = 60;  -- Проверять каждые 60 секунд

-- Настройка checkpoint'ов
ALTER SYSTEM SET checkpoint_completion_target = 0.9;
ALTER SYSTEM SET wal_buffers = '16MB';

-- Примечание: Эти настройки применяются после перезагрузки сервера
-- SELECT pg_reload_conf();

-- Создаем схему если не существует (по умолчанию public)
-- CREATE SCHEMA IF NOT EXISTS public;

-- Логирование
DO $$
BEGIN
  RAISE NOTICE '✅ PostgreSQL инициализирован для IT Interview Trainer';
  RAISE NOTICE '📊 База данных: interview_trainer';
  RAISE NOTICE '👤 Пользователь: %', current_user;
END $$;
