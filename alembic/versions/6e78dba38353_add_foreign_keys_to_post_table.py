"""Add foreign keys to post table

Revision ID: 6e78dba38353
Revises: 10a7237e9d8c
Create Date: 2025-01-12 20:49:54.145314

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6e78dba38353'
down_revision: Union[str, None] = '10a7237e9d8c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column("user_id",sa.Integer(),nullable = False))
    #local_cols is the col that will be the fk
    #remote_cols is the column being reference in the referent table(users table)
    op.create_foreign_key("posts_users_fk", source_table="posts", referent_table="users",
                          local_cols=['user_id'],remote_cols=['id'],ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint("posts_users_fk",table_name = "posts")
    op.drop_column('posts',  'user_id')
    pass
