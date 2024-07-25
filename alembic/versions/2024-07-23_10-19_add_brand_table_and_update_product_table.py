"""Add brand table and update product table

Revision ID: 20c20348eadf
Revises: a044842c7fba
Create Date: 2024-07-23 10:19:27.699205

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session


# revision identifiers, used by Alembic.
revision: str = '20c20348eadf'
down_revision: Union[str, None] = 'a044842c7fba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade():
    # Create brand table
    op.create_table(
        'brand',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, unique=True)
    )
    # Create category_brand table
    op.create_table(
        'category_brand',
        sa.Column('category_id', sa.Integer, sa.ForeignKey('category.id', ondelete='CASCADE'), primary_key=True),
        sa.Column('brand_id', sa.Integer, sa.ForeignKey('brand.id', ondelete='CASCADE'), primary_key=True)
    )

    # Add brand_id column to product table
    op.add_column('product', sa.Column('brand_id', sa.Integer, sa.ForeignKey('brand.id', ondelete='CASCADE')))

    # Migrate existing data from product.brand to brand table and update product.brand_id
    bind = op.get_bind()
    session = Session(bind=bind)

    # Define the brand table explicitly
    brand_table = sa.Table(
        'brand', 
        sa.MetaData(),
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, unique=True)
    )


    op.drop_column('product', 'brand')

def downgrade():
    # Revert the changes made in the upgrade
    op.add_column('product', sa.Column('brand', sa.String))
    
    # Remove the brand_id column
    op.drop_column('product', 'brand_id')

    # Drop the category_brand table
    op.drop_table('category_brand')

    # Drop the brand table
    op.drop_table('brand')