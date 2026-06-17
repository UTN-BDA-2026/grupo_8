"""merge heads

Revision ID: f95185d6bccf
Revises: 5e4b6a839023, ec746454cf50
Create Date: 2026-06-15 12:10:45.390934

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f95185d6bccf'
down_revision: Union[str, Sequence[str], None] = ('5e4b6a839023', 'ec746454cf50')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
