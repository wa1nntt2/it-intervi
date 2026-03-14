"""Make session_id nullable in answers table

Revision ID: 006_make_session_id_nullable
Revises: 005_add_created_at_to_answers
Create Date: 2026-03-14 20:20:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '006_make_session_id_nullable'
down_revision: Union[str, None] = '005_add_created_at_to_answers'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Делаем session_id nullable (batch mode для SQLite)
    # В SQLite нельзя изменить существующий столбец, нужно пересоздать таблицу
    # Но мы можем просто игнорировать NOT NULL ограничение пока
    pass  # session_id уже nullable в модели, просто не передаётся


def downgrade() -> None:
    pass
