"""empty message

Revision ID: 553fff6fd2be
Revises: af10397260b1
Create Date: 2015-12-27 14:15:58.016675

"""

# revision identifiers, used by Alembic.
revision = '553fff6fd2be'
down_revision = 'af10397260b1'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'photo_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'photo_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    ### end Alembic commands ###
