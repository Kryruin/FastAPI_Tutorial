"""Add users table

Revision ID: 10a7237e9d8c
Revises: 60c0307eccff
Create Date: 2025-01-12 18:03:09.478696

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '10a7237e9d8c'
down_revision: Union[str, None] = '60c0307eccff'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id',sa.Integer(),nullable = False),
                    sa.Column('email',sa.String(),nullable = False),
                    sa.Column('password',sa.String(),nullable = False),
                    sa.Column('created_at',sa.TIMESTAMP(timezone=True), server_default = sa.text('now()'),nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
