"""Add created_at to answers table

Revision ID: 005_add_created_at_to_answers
Revises: 004_add_selected_option_to_answers
Create Date: 2026-03-14 20:15:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '005_add_created_at_to_answers'
down_revision: Union[str, None] = '004_add_selected_option_to_answers'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Добавляем created_at в таблицу answers (batch mode для SQLite)
    with op.batch_alter_table('answers', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_at', sa.DateTime(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP')))


def downgrade() -> None:
    # Откатываем изменения
    with op.batch_alter_table('answers', schema=None) as batch_op:
        batch_op.drop_column('created_at')
