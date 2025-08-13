"""template check

Revision ID: cd923842990f
Revises: 20407b24166b
Create Date: 2025-08-12 13:01:33.237476

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'cd923842990f'
down_revision: Union[str, Sequence[str], None] = '20407b24166b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
