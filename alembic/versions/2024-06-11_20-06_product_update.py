"""product update

Revision ID: 65e2eaff6a91
Revises: ddcc7d9d096d
Create Date: 2024-06-11 20:06:12.782795

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '65e2eaff6a91'
down_revision: Union[str, None] = 'ddcc7d9d096d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_product_info_id', table_name='product_info')
    op.drop_table('product_info')
    op.add_column('product', sa.Column('description', sa.String(), nullable=False))
    op.add_column('product', sa.Column('product_id', sa.Integer(), nullable=False))
    op.add_column('product', sa.Column('article', sa.String(), nullable=False))
    op.create_foreign_key(None, 'product', 'product', ['product_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'product', type_='foreignkey')
    op.drop_column('product', 'article')
    op.drop_column('product', 'product_id')
    op.drop_column('product', 'description')
    op.create_table('product_info',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('product_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('article', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], name='product_info_product_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='product_info_pkey')
    )
    op.create_index('ix_product_info_id', 'product_info', ['id'], unique=False)
    # ### end Alembic commands ###
