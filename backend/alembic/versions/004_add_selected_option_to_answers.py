"""Add selected_option to answers table

Revision ID: 004_add_selected_option_to_answers
Revises: 003_add_user_id_to_answers
Create Date: 2026-03-14 20:10:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '004_add_selected_option_to_answers'
down_revision: Union[str, None] = '003_add_user_id_to_answers'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Добавляем selected_option в таблицу answers (batch mode для SQLite)
    with op.batch_alter_table('answers', schema=None) as batch_op:
        batch_op.add_column(sa.Column('selected_option', sa.Integer(), nullable=True))


def downgrade() -> None:
    # Откатываем изменения
    with op.batch_alter_table('answers', schema=None) as batch_op:
        batch_op.drop_column('selected_option')
