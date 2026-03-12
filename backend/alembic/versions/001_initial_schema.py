"""Initial schema - создание всех таблиц

Revision ID: 001_initial_schema
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '001_initial_schema'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # === Таблица пользователей ===
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('is_admin', sa.Boolean(), nullable=True, default=False),
        sa.Column('created_at', sa.DateTime(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)

    # === Таблица профессий ===
    op.create_table('professions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_professions_id'), 'professions', ['id'], unique=False)

    # === Таблица вопросов ===
    op.create_table('questions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('profession_id', sa.Integer(), nullable=False),
        sa.Column('text', sa.String(), nullable=False),
        sa.Column('question_type', sa.String(), nullable=False),
        sa.Column('difficulty', sa.String(), nullable=True, default='junior'),
        sa.Column('options', sa.JSON(), nullable=False),
        sa.Column('correct_option', sa.Integer(), nullable=True),
        sa.Column('correct_order', sa.JSON(), nullable=True),
        sa.Column('explanation', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['profession_id'], ['professions.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_questions_difficulty'), 'questions', ['difficulty'], unique=False)
    op.create_index(op.f('ix_questions_id'), 'questions', ['id'], unique=False)
    op.create_index(op.f('ix_questions_profession_id'), 'questions', ['profession_id'], unique=False)
    op.create_index(op.f('ix_questions_question_type'), 'questions', ['question_type'], unique=False)

    # === Таблица ответов ===
    op.create_table('answers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('session_id', sa.Integer(), nullable=False),
        sa.Column('question_id', sa.Integer(), nullable=False),
        sa.Column('user_answer', sa.JSON(), nullable=True),
        sa.Column('is_correct', sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(['question_id'], ['questions.id'], ),
        sa.ForeignKeyConstraint(['session_id'], ['sessions.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_answers_id'), 'answers', ['id'], unique=False)
    op.create_index(op.f('ix_answers_question_id'), 'answers', ['question_id'], unique=False)
    op.create_index(op.f('ix_answers_session_id'), 'answers', ['session_id'], unique=False)

    # === Таблица сессий ===
    op.create_table('sessions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('profession_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('question_ids', sa.JSON(), nullable=False),
        sa.Column('status', sa.String(), nullable=True, default='active'),
        sa.Column('score', sa.Integer(), nullable=True, default=0),
        sa.Column('created_at', sa.DateTime(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['profession_id'], ['professions.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_sessions_completed_at'), 'sessions', ['completed_at'], unique=False)
    op.create_index(op.f('ix_sessions_created_at'), 'sessions', ['created_at'], unique=False)
    op.create_index(op.f('ix_sessions_id'), 'sessions', ['id'], unique=False)
    op.create_index(op.f('ix_sessions_profession_id'), 'sessions', ['profession_id'], unique=False)
    op.create_index(op.f('ix_sessions_status'), 'sessions', ['status'], unique=False)
    op.create_index(op.f('ix_sessions_user_id'), 'sessions', ['user_id'], unique=False)

    # === Таблица прогресса пользователя ===
    op.create_table('user_progress',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('xp', sa.Integer(), nullable=True, default=0),
        sa.Column('level', sa.Integer(), nullable=True, default=1),
        sa.Column('total_sessions', sa.Integer(), nullable=True, default=0),
        sa.Column('completed_sessions', sa.Integer(), nullable=True, default=0),
        sa.Column('total_correct_answers', sa.Integer(), nullable=True, default=0),
        sa.Column('total_questions_answered', sa.Integer(), nullable=True, default=0),
        sa.Column('best_streak', sa.Integer(), nullable=True, default=0),
        sa.Column('current_streak', sa.Integer(), nullable=True, default=0),
        sa.Column('title', sa.String(), nullable=True, default='Новичок'),
        sa.Column('badges', sa.JSON(), nullable=True, default=list),
        sa.Column('created_at', sa.DateTime(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('last_session_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_progress_current_streak'), 'user_progress', ['current_streak'], unique=False)
    op.create_index(op.f('ix_user_progress_id'), 'user_progress', ['id'], unique=False)
    op.create_index(op.f('ix_user_progress_level'), 'user_progress', ['level'], unique=False)
    op.create_index(op.f('ix_user_progress_user_id'), 'user_progress', ['user_id'], unique=True)
    op.create_index(op.f('ix_user_progress_xp'), 'user_progress', ['xp'], unique=False)

    # === Таблица достижений ===
    op.create_table('achievements',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=False),
        sa.Column('icon', sa.String(), nullable=False),
        sa.Column('xp_reward', sa.Integer(), nullable=True, default=0),
        sa.Column('requirement_type', sa.String(), nullable=False),
        sa.Column('requirement_value', sa.Integer(), nullable=False),
        sa.Column('category', sa.String(), nullable=True, default='general'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_achievements_id'), 'achievements', ['id'], unique=False)

    # === Таблица разблокированных достижений ===
    op.create_table('user_achievements',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('achievement_id', sa.Integer(), nullable=False),
        sa.Column('unlocked_at', sa.DateTime(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['achievement_id'], ['achievements.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_achievements_achievement_id'), 'user_achievements', ['achievement_id'], unique=False)
    op.create_index(op.f('ix_user_achievements_id'), 'user_achievements', ['id'], unique=False)
    op.create_index(op.f('ix_user_achievements_user_id'), 'user_achievements', ['user_id'], unique=False)

    # === Таблица ordering items (для вопросов на упорядочивание) ===
    op.create_table('ordering_items',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('question_id', sa.Integer(), nullable=False),
        sa.Column('text', sa.String(), nullable=False),
        sa.Column('order_index', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['question_id'], ['questions.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ordering_items_id'), 'ordering_items', ['id'], unique=False)
    op.create_index(op.f('ix_ordering_items_question_id'), 'ordering_items', ['question_id'], unique=False)


def downgrade() -> None:
    # Удаляем таблицы в обратном порядке (сначала зависимые)
    op.drop_table('ordering_items')
    op.drop_table('user_achievements')
    op.drop_table('achievements')
    op.drop_table('user_progress')
    op.drop_table('sessions')
    op.drop_table('answers')
    op.drop_table('questions')
    op.drop_table('professions')
    op.drop_table('users')
