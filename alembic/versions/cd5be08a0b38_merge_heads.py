"""merge heads

Revision ID: cd5be08a0b38
Revises: 8a5854a8cd30, 658c4b856051
Create Date: 2026-06-17 17:38:20.194212

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cd5be08a0b38'
down_revision: Union[str, Sequence[str], None] = ('8a5854a8cd30', '658c4b856051')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
