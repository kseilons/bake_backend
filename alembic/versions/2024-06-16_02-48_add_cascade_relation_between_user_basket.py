"""add cascade relation between user, basket

Revision ID: a18d35e1241c
Revises: feb3b3c92573
Create Date: 2024-06-16 02:48:28.759747

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a18d35e1241c'
down_revision: Union[str, None] = 'feb3b3c92573'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('basket_user_id_fkey', 'basket', type_='foreignkey')
    op.create_foreign_key(None, 'basket', 'user', ['user_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'basket', type_='foreignkey')
    op.create_foreign_key('basket_user_id_fkey', 'basket', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###
