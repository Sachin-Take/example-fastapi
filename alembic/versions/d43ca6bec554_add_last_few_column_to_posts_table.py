"""add last few column to posts table

Revision ID: d43ca6bec554
Revises: d2efe35a562d
Create Date: 2024-06-25 11:18:21.509821

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd43ca6bec554'
down_revision: Union[str, None] = 'd2efe35a562d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts',sa.Column('published',sa.Boolean(),nullable=False,server_default='True'),)
    op.add_column('posts',sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False
                                    ,server_default=sa.text('NOW()')),)
    pass


def downgrade():
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
    pass
