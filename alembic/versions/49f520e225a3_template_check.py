"""template check

Revision ID: 49f520e225a3
Revises: 20407b24166b
Create Date: 2025-08-12 12:57:56.206286

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import aqlmodel


# revision identifiers, used by Alembic.
revision: str = '49f520e225a3'
down_revision: Union[str, Sequence[str], None] = '20407b24166b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
