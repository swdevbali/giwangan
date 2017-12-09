"""Add pageviews for page

Revision ID: 4ecd65e5e833
Revises: 02a04bf8bd66
Create Date: 2017-12-09 00:29:23.492646

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4ecd65e5e833'
down_revision = '02a04bf8bd66'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('page', sa.Column('pageviews', sa.Integer(), nullable=True))
    op.execute("update page set pageviews=0")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('page', 'pageviews')
    # ### end Alembic commands ###