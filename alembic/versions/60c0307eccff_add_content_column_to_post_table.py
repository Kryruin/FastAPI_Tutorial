"""add content column to post table

Revision ID: 60c0307eccff
Revises: fbdbf4ce6725
Create Date: 2025-01-12 17:48:12.069752

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '60c0307eccff'
down_revision: Union[str, None] = 'fbdbf4ce6725'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column("content",sa.String(),nullable = False))
    pass


def downgrade() -> None:
    op.drop_column('posts',"content")
    pass
