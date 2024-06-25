"""add content column in table posts

Revision ID: 3c8fa2602c7b
Revises: d7f31d85b9f8
Create Date: 2024-06-24 18:16:44.585929

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3c8fa2602c7b'
down_revision: Union[str, None] = 'd7f31d85b9f8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade():
    op.drop_column('posts','content')
    pass
