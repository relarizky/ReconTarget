"""empty message

Revision ID: 0915c7b3c82a
Revises: fdccc3b957a3
Create Date: 2020-06-10 19:47:22.036457

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '0915c7b3c82a'
down_revision = 'fdccc3b957a3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tb_target', sa.Column('target_status_code', sa.String(length=3), nullable=True))
    op.drop_column('tb_target', 'taret_status_code')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tb_target', sa.Column('taret_status_code', mysql.VARCHAR(length=3), nullable=True))
    op.drop_column('tb_target', 'target_status_code')
    # ### end Alembic commands ###
