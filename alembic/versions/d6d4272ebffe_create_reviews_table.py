"""Create reviews table

Revision ID: d6d4272ebffe
Revises: 
Create Date: 2024-02-12 10:55:38.194992

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd6d4272ebffe'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'reviews',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('star_rating', sa.Integer),
        sa.Column('restaurant_id', sa.Integer, sa.ForeignKey('restaurants.id')),
        sa.Column('customer_id', sa.Integer, sa.ForeignKey('customers.id'))
    )

# Define the downgrade function
def downgrade():
    op.drop_table('reviews')