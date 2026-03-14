"""Add categories and interview configs tables

Revision ID: 002_add_categories_interview_configs
Revises: 001_initial_schema
Create Date: 2026-03-14 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '002_add_categories_interview_configs'
down_revision: Union[str, None] = '001_initial_schema'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # === Таблица категорий ===
    op.create_table('categories',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('profession_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['profession_id'], ['professions.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_categories_id'), 'categories', ['id'], unique=False)
    op.create_index(op.f('ix_categories_profession_id'), 'categories', ['profession_id'], unique=False)

    # === Таблица связи вопросов и категорий (многие-ко-многим) ===
    op.create_table('question_categories',
        sa.Column('question_id', sa.Integer(), nullable=False),
        sa.Column('category_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['question_id'], ['questions.id'], ),
        sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
        sa.PrimaryKeyConstraint('question_id', 'category_id')
    )

    # === Таблица конфигураций собеседований ===
    op.create_table('interview_configs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('profession_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('difficulty', sa.String(), nullable=True, default='junior'),
        sa.Column('category_configs', sa.JSON(), nullable=False, default=list),
        sa.Column('is_public', sa.Boolean(), nullable=True, default=False),
        sa.Column('is_default', sa.Boolean(), nullable=True, default=False),
        sa.Column('created_at', sa.DateTime(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['profession_id'], ['professions.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_interview_configs_id'), 'interview_configs', ['id'], unique=False)
    op.create_index(op.f('ix_interview_configs_profession_id'), 'interview_configs', ['profession_id'], unique=False)
    op.create_index(op.f('ix_interview_configs_user_id'), 'interview_configs', ['user_id'], unique=False)

    # === Добавляем столбец explanation в таблицу questions (если его нет) ===
    # Для SQLite это может не понадобиться, но добавляем для совместимости
    try:
        op.add_column('questions', sa.Column('explanation', sa.String(), nullable=True))
    except Exception:
        pass  # Столбец уже существует


def downgrade() -> None:
    # Откатываем изменения в обратном порядке
    op.drop_table('interview_configs')
    op.drop_table('question_categories')
    op.drop_table('categories')
    
    # Удаляем explanation из questions (если нужно)
    try:
        with op.batch_alter_table('questions', schema=None) as batch_op:
            batch_op.drop_column('explanation')
    except Exception:
        pass  # Для SQLite может не поддерживаться
