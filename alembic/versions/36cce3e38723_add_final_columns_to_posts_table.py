"""add final columns to posts table

Revision ID: 36cce3e38723
Revises: 6e78dba38353
Create Date: 2025-01-12 21:08:35.688652

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '36cce3e38723'
down_revision: Union[str, None] = '6e78dba38353'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('published',sa.Boolean(),nullable=False,server_default = "TRUE"))
    op.add_column('posts',sa.Column('created_at',sa.TIMESTAMP(timezone=True), server_default = sa.text('now()')))
    pass


def downgrade() -> None:
    op.drop_column('posts','created_at')
    op.drop_column('posts','published')
    pass
