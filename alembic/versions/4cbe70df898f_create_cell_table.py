"""create cell table

Revision ID: 4cbe70df898f
Revises: 
Create Date: 2017-09-17 12:02:30.316266

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4cbe70df898f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
  op.create_table(
    'cell',
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('variety', sa.String(10), nullable=False),
    sa.Column('number', sa.String(10), nullable=False),
    sa.Column('content', sa.String(1), nullable=False),
    sa.Column('answer', sa.String(1), nullable=False),
    sa.Column('circled', sa.Boolean(), nullable=False),
  )


def downgrade():
  op.drop_table('cell')
