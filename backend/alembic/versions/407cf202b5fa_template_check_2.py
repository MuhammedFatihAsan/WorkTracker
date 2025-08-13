"""template check 2

Revision ID: 407cf202b5fa
Revises: cd923842990f
Create Date: 2025-08-12 13:02:00.213984

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '407cf202b5fa'
down_revision: Union[str, Sequence[str], None] = 'cd923842990f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
