"""access token

Revision ID: 909c8ceac365
Revises: 3645a23d8c5e
Create Date: 2024-05-17 20:27:34.745858

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '909c8ceac365'
down_revision: Union[str, None] = '3645a23d8c5e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tokens', sa.Column('access_token', sa.UUID(as_uuid=False), nullable=True))
    op.drop_index('ix_tokens_token', table_name='tokens')
    op.create_index(op.f('ix_tokens_access_token'), 'tokens', ['access_token'], unique=True)
    op.drop_column('tokens', 'token')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tokens', sa.Column('token', sa.UUID(), autoincrement=False, nullable=False))
    op.drop_index(op.f('ix_tokens_access_token'), table_name='tokens')
    op.create_index('ix_tokens_token', 'tokens', ['token'], unique=True)
    op.drop_column('tokens', 'access_token')
    # ### end Alembic commands ###