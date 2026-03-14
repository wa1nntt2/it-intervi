"""Add user_id to answers table

Revision ID: 003_add_user_id_to_answers
Revises: 002_add_categories_interview_configs
Create Date: 2026-03-14 20:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '003_add_user_id_to_answers'
down_revision: Union[str, None] = '002_add_categories_interview_configs'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Добавляем user_id в таблицу answers (batch mode для SQLite)
    with op.batch_alter_table('answers', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_answers_user_id', 'users', ['user_id'], ['id'])


def downgrade() -> None:
    # Откатываем изменения
    with op.batch_alter_table('answers', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_index('ix_answers_user_id')
        batch_op.drop_column('user_id')
