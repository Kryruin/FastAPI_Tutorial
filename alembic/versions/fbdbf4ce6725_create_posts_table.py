"""create posts table

Revision ID: fbdbf4ce6725
Revises: 
Create Date: 2025-01-12 17:16:37.387455

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fbdbf4ce6725'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("posts", sa.Column('id',sa.Integer(), nullable = False, primary_key= True),sa.Column('Title',sa.String(), nullable = False))
    pass


def downgrade() -> None:
    op.drop_table("posts")
    pass
