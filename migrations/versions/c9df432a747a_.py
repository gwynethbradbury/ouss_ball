"""empty message

Revision ID: c9df432a747a
Revises: 878385c2bc9b
Create Date: 2017-01-04 17:14:24.445368

"""

# revision identifiers, used by Alembic.
revision = 'c9df432a747a'
down_revision = '878385c2bc9b'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('eway_transaction', 'eway_id',
               existing_type=mysql.INTEGER(display_width=11),
               type_=sa.String(length=50),
               existing_nullable=True)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('eway_transaction', 'eway_id',
               existing_type=sa.String(length=50),
               type_=mysql.INTEGER(display_width=11),
               existing_nullable=True)
    ### end Alembic commands ###
