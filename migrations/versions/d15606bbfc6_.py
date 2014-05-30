"""empty message

Revision ID: d15606bbfc6
Revises: 22554f056f04
Create Date: 2014-05-29 23:31:13.086361

"""

# revision identifiers, used by Alembic.
revision = 'd15606bbfc6'
down_revision = '22554f056f04'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('paging',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('screen', sa.Integer(), nullable=True),
    sa.Column('page', sa.Integer(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('modified', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('paging')
    ### end Alembic commands ###
