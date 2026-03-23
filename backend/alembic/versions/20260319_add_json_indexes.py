"""Add PostgreSQL GIN indexes for JSON fields

Revision ID: 20260319_add_json_indexes
Revises: 20260315_153348
Create Date: 2026-03-19

Добавляет GIN индексы для JSON полей в PostgreSQL для ускорения поиска.
Для SQLite эти индексы игнорируются (не поддерживаются).

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision: str = '20260319_add_json_indexes'
down_revision: Union[str, None] = '20260315_153348'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Добавляет GIN индексы для JSON полей.
    
    GIN (Generalized Inverted Index) - специальный индекс для работы
    с составными значениями (JSON, массивы, full-text search).
    
    Преимущества:
    - Быстрый поиск по ключам и значениям JSON
    - Поддержка операторов @>, ?, ?&, ?|
    - Эффективно для больших объемов данных
    """
    # Получаем тип базы данных
    bind = op.get_bind()
    is_postgresql = bind.dialect.name == 'postgresql'
    
    if not is_postgresql:
        # Для SQLite индексы не поддерживаются, пропускаем
        print("⊘ Пропускаем создание GIN индексов (не SQLite)")
        return
    
    print("📊 Создание GIN индексов для PostgreSQL...")
    
    # GIN индекс для options в questions (быстрый поиск по значениям)
    # Позволяет эффективно искать вопросы с определенными вариантами ответов
    op.execute(text(
        "CREATE INDEX IF NOT EXISTS ix_questions_options_gin "
        "ON questions USING GIN (options jsonb_path_ops)"
    ))
    print("  ✓ ix_questions_options_gin")
    
    # GIN индекс для correct_order в questions
    # Полезен для поиска ordering вопросов по правильному порядку
    op.execute(text(
        "CREATE INDEX IF NOT EXISTS ix_questions_correct_order_gin "
        "ON questions USING GIN (correct_order jsonb_path_ops)"
    ))
    print("  ✓ ix_questions_correct_order_gin")
    
    # GIN индекс для question_ids в sessions
    # Ускоряет поиск сессий по наличию определенных вопросов
    op.execute(text(
        "CREATE INDEX IF NOT EXISTS ix_sessions_question_ids_gin "
        "ON sessions USING GIN (question_ids jsonb_path_ops)"
    ))
    print("  ✓ ix_sessions_question_ids_gin")
    
    # GIN индекс для badges в user_progress
    # Позволяет быстро искать пользователей с определенными значками
    op.execute(text(
        "CREATE INDEX IF NOT EXISTS ix_user_progress_badges_gin "
        "ON user_progress USING GIN (badges jsonb_path_ops)"
    ))
    print("  ✓ ix_user_progress_badges_gin")
    
    print("✅ GIN индексы созданы")


def downgrade() -> None:
    """
    Удаляет GIN индексы.
    """
    bind = op.get_bind()
    is_postgresql = bind.dialect.name == 'postgresql'
    
    if not is_postgresql:
        print("⊘ Пропускаем удаление GIN индексов (не PostgreSQL)")
        return
    
    print("🗑️  Удаление GIN индексов...")
    
    op.execute(text("DROP INDEX IF EXISTS ix_questions_options_gin"))
    op.execute(text("DROP INDEX IF EXISTS ix_questions_correct_order_gin"))
    op.execute(text("DROP INDEX IF EXISTS ix_sessions_question_ids_gin"))
    op.execute(text("DROP INDEX IF EXISTS ix_user_progress_badges_gin"))
    
    print("✅ GIN индексы удалены")
