"""change_length_hashed_password

Revision ID: 6006260bed1c
Revises: aafef00490e9
Create Date: 2026-09-08 23:02:08.159573

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6006260bed1c'
down_revision: Union[str, Sequence[str], None] = 'aafef00490e9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column('users', 'hashed_password',
               existing_type=sa.String(length=50),
               type_=sa.String(length=150),
               existing_nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    # Откат изменений к первоначальному состоянию
    op.alter_column('users', 'hashed_password',
               existing_type=sa.String(length=150),
               type_=sa.String(length=50),
               existing_nullable=False)

