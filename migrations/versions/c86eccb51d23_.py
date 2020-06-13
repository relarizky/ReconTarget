"""empty message

Revision ID: c86eccb51d23
Revises: b4eba20b659c
Create Date: 2020-06-13 10:07:46.718920

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c86eccb51d23'
down_revision = 'b4eba20b659c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tb_wpuser',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_target', sa.Integer(), nullable=True),
    sa.Column('list_username', mysql.JSON(), nullable=True),
    sa.ForeignKeyConstraint(['id_target'], ['tb_target.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tb_wpuser')
    # ### end Alembic commands ###
