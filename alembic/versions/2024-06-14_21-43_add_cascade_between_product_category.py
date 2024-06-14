"""Add cascade between product, category

Revision ID: 8a9c0ff04e5d
Revises: 4ada3e404db4
Create Date: 2024-06-14 21:43:02.477849

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8a9c0ff04e5d'
down_revision: Union[str, None] = '4ada3e404db4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('product_category_id_fkey', 'product', type_='foreignkey')
    op.create_foreign_key(None, 'product', 'category', ['category_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'product', type_='foreignkey')
    op.create_foreign_key('product_category_id_fkey', 'product', 'category', ['category_id'], ['id'])
    # ### end Alembic commands ###
