"""Add love_count

Revision ID: 56e40c9deb67
Revises: ab2ed7a65f7c
Create Date: 2017-12-10 01:40:29.292796

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '56e40c9deb67'
down_revision = 'ab2ed7a65f7c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('page', sa.Column('love_count', sa.Integer(), nullable=True))
    op.execute('update page set love_count=0')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('page', 'love_count')
    # ### end Alembic commands ###