"""merge heads

Revision ID: ab1fdd72105a
Revises: b9317907eeb8, cd5be08a0b38
Create Date: 2026-06-20 22:42:32.587529

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ab1fdd72105a'
down_revision: Union[str, Sequence[str], None] = ('b9317907eeb8', 'cd5be08a0b38')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
