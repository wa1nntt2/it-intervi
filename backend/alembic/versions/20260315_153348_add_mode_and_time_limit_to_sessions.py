"""add mode and time_limit to sessions

Revision ID: {timestamp}
Revises: 006_make_session_id_nullable
Create Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '{timestamp}'
down_revision: Union[str, None] = '006_make_session_id_nullable'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add mode column with default value 'practice'
    op.add_column('sessions', sa.Column('mode', sa.String(), nullable=True, server_default='practice'))
    
    # Add time_limit column for timed mode
    op.add_column('sessions', sa.Column('time_limit', sa.Integer(), nullable=True))
    
    # Set default value for existing rows
    op.execute("UPDATE sessions SET mode = 'practice' WHERE mode IS NULL")


def downgrade() -> None:
    op.drop_column('sessions', 'time_limit')
    op.drop_column('sessions', 'mode')
