"""empty message

Revision ID: 71a5df6794dc
Revises: 6546791fcdcb
Create Date: 2016-01-21 17:14:22.486865

"""

# revision identifiers, used by Alembic.
revision = '71a5df6794dc'
down_revision = '6546791fcdcb'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('purchase_group',
    sa.Column('object_id', sa.Integer(), nullable=False),
    sa.Column('code', sa.Unicode(length=10), nullable=False),
    sa.Column('leader_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['leader_id'], [u'user.object_id'], ),
    sa.PrimaryKeyConstraint('object_id'),
    sa.UniqueConstraint('code')
    )
    op.create_table('group_purchase_request',
    sa.Column('object_id', sa.Integer(), nullable=False),
    sa.Column('ticket_type_slug', sa.Unicode(length=50), nullable=False),
    sa.Column('number_requested', sa.Integer(), nullable=False),
    sa.Column('purchase_group_id', sa.Integer(), nullable=False),
    sa.Column('requester_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['purchase_group_id'], [u'purchase_group.object_id'], ),
    sa.ForeignKeyConstraint(['requester_id'], [u'user.object_id'], ),
    sa.PrimaryKeyConstraint('object_id')
    )
    op.create_table('purchase_group_member_link',
    sa.Column('group_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['group_id'], [u'purchase_group.object_id'], ),
    sa.ForeignKeyConstraint(['user_id'], [u'user.object_id'], )
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('purchase_group_member_link')
    op.drop_table('group_purchase_request')
    op.drop_table('purchase_group')
    ### end Alembic commands ###
