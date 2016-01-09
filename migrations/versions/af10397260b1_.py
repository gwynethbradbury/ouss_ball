"""empty message

Revision ID: af10397260b1
Revises: None
Create Date: 2015-12-24 22:44:14.650766

"""

# revision identifiers, used by Alembic.
revision = 'af10397260b1'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('affiliation',
    sa.Column('object_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Unicode(length=25), nullable=False),
    sa.PrimaryKeyConstraint('object_id')
    )
    op.create_table('battels',
    sa.Column('object_id', sa.Integer(), nullable=False),
    sa.Column('battelsid', sa.Unicode(length=6), nullable=True),
    sa.Column('email', sa.Unicode(length=120), nullable=True),
    sa.Column('title', sa.Unicode(length=10), nullable=True),
    sa.Column('surname', sa.Unicode(length=60), nullable=True),
    sa.Column('forenames', sa.Unicode(length=60), nullable=True),
    sa.Column('michaelmas_charge', sa.Integer(), nullable=False),
    sa.Column('hilary_charge', sa.Integer(), nullable=False),
    sa.Column('manual', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('object_id'),
    sa.UniqueConstraint('battelsid'),
    sa.UniqueConstraint('email')
    )
    op.create_table('college',
    sa.Column('object_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Unicode(length=50), nullable=False),
    sa.PrimaryKeyConstraint('object_id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('photo',
    sa.Column('object_id', sa.Integer(), nullable=False),
    sa.Column('filename', sa.Unicode(length=50), nullable=False),
    sa.Column('full_url', sa.Unicode(length=250), nullable=False),
    sa.Column('thumb_url', sa.Unicode(length=250), nullable=False),
    sa.PrimaryKeyConstraint('object_id')
    )
    op.create_table('statistic',
    sa.Column('object_id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('group', sa.Enum(u'Colleges', u'Payments', u'Sales'), nullable=False),
    sa.Column('statistic', sa.Unicode(length=25), nullable=False),
    sa.Column('value', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('object_id')
    )
    op.create_table('user',
    sa.Column('object_id', sa.Integer(), nullable=False),
    sa.Column('email', sa.Unicode(length=120), nullable=False),
    sa.Column('new_email', sa.Unicode(length=120), nullable=True),
    sa.Column('password_hash', sa.BINARY(length=60), nullable=False),
    sa.Column('forenames', sa.Unicode(length=120), nullable=False),
    sa.Column('surname', sa.Unicode(length=120), nullable=False),
    sa.Column('phone', sa.Unicode(length=20), nullable=False),
    sa.Column('secret_key', sa.Unicode(length=64), nullable=True),
    sa.Column('secret_key_expiry', sa.DateTime(), nullable=True),
    sa.Column('verified', sa.Boolean(), nullable=False),
    sa.Column('deleted', sa.Boolean(), nullable=False),
    sa.Column('note', sa.UnicodeText(), nullable=True),
    sa.Column('role', sa.Enum(u'User', u'Admin'), nullable=False),
    sa.Column('college_id', sa.Integer(), nullable=False),
    sa.Column('affiliation_id', sa.Integer(), nullable=False),
    sa.Column('battels_id', sa.Integer(), nullable=True),
    sa.Column('affiliation_verified', sa.Boolean(), nullable=True),
    sa.Column('photo_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['affiliation_id'], [u'affiliation.object_id'], ),
    sa.ForeignKeyConstraint(['battels_id'], [u'battels.object_id'], ),
    sa.ForeignKeyConstraint(['college_id'], [u'college.object_id'], ),
    sa.ForeignKeyConstraint(['photo_id'], [u'photo.object_id'], ),
    sa.PrimaryKeyConstraint('object_id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('new_email')
    )
    op.create_table('announcement',
    sa.Column('object_id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('content', sa.UnicodeText(length=65536), nullable=False),
    sa.Column('subject', sa.UnicodeText(length=256), nullable=False),
    sa.Column('send_email', sa.Boolean(), nullable=False),
    sa.Column('email_sent', sa.Boolean(), nullable=False),
    sa.Column('sender_id', sa.Integer(), nullable=False),
    sa.Column('college_id', sa.Integer(), nullable=True),
    sa.Column('affiliation_id', sa.Integer(), nullable=True),
    sa.Column('is_waiting', sa.Boolean(), nullable=True),
    sa.Column('has_tickets', sa.Boolean(), nullable=True),
    sa.Column('has_collected', sa.Boolean(), nullable=True),
    sa.Column('has_uncollected', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['affiliation_id'], [u'affiliation.object_id'], ),
    sa.ForeignKeyConstraint(['college_id'], [u'college.object_id'], ),
    sa.ForeignKeyConstraint(['sender_id'], [u'user.object_id'], ),
    sa.PrimaryKeyConstraint('object_id')
    )
    op.create_table('card_transaction',
    sa.Column('object_id', sa.Integer(), nullable=False),
    sa.Column('commenced', sa.DateTime(), nullable=False),
    sa.Column('completed', sa.DateTime(), nullable=True),
    sa.Column('access_code', sa.Unicode(length=200), nullable=True),
    sa.Column('result_code', sa.Unicode(length=2), nullable=True),
    sa.Column('eway_id', sa.Integer(), nullable=True),
    sa.Column('refunded', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], [u'user.object_id'], ),
    sa.PrimaryKeyConstraint('object_id')
    )
    op.create_table('ticket',
    sa.Column('object_id', sa.Integer(), nullable=False),
    sa.Column('ticket_type', sa.Unicode(length=50), nullable=False),
    sa.Column('paid', sa.Boolean(), nullable=False),
    sa.Column('collected', sa.Boolean(), nullable=False),
    sa.Column('entered', sa.Boolean(), nullable=False),
    sa.Column('cancelled', sa.Boolean(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('name', sa.Unicode(length=120), nullable=True),
    sa.Column('note', sa.UnicodeText(), nullable=True),
    sa.Column('expires', sa.DateTime(), nullable=True),
    sa.Column('barcode', sa.Unicode(length=20), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['owner_id'], [u'user.object_id'], ),
    sa.PrimaryKeyConstraint('object_id'),
    sa.UniqueConstraint('barcode')
    )
    op.create_table('voucher',
    sa.Column('object_id', sa.Integer(), nullable=False),
    sa.Column('code', sa.Unicode(length=30), nullable=False),
    sa.Column('expires', sa.DateTime(), nullable=True),
    sa.Column('discount_type', sa.Enum(u'Fixed Price', u'Fixed Discount', u'Percentage Discount'), nullable=False),
    sa.Column('discount_value', sa.Integer(), nullable=False),
    sa.Column('applies_to', sa.Enum(u'Ticket', u'Transaction'), nullable=False),
    sa.Column('single_use', sa.Boolean(), nullable=False),
    sa.Column('used', sa.Boolean(), nullable=True),
    sa.Column('used_by_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['used_by_id'], [u'user.object_id'], ),
    sa.PrimaryKeyConstraint('object_id')
    )
    op.create_table('waiting',
    sa.Column('object_id', sa.Integer(), nullable=False),
    sa.Column('waiting_since', sa.DateTime(), nullable=False),
    sa.Column('waiting_for', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], [u'user.object_id'], ),
    sa.PrimaryKeyConstraint('object_id')
    )
    op.create_table('email_announce_link',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('announcement_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['announcement_id'], [u'announcement.object_id'], ),
    sa.ForeignKeyConstraint(['user_id'], [u'user.object_id'], )
    )
    op.create_table('log',
    sa.Column('object_id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('ip_address', sa.Unicode(length=45), nullable=False),
    sa.Column('action', sa.UnicodeText(), nullable=True),
    sa.Column('actor_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('card_transaction_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['actor_id'], [u'user.object_id'], ),
    sa.ForeignKeyConstraint(['card_transaction_id'], [u'card_transaction.object_id'], ),
    sa.ForeignKeyConstraint(['user_id'], [u'user.object_id'], ),
    sa.PrimaryKeyConstraint('object_id')
    )
    op.create_table('transaction',
    sa.Column('object_id', sa.Integer(), nullable=False),
    sa.Column('paid', sa.Boolean(), nullable=False),
    sa.Column('completed', sa.Boolean(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('battels_term', sa.Unicode(length=4), nullable=True),
    sa.Column('card_transaction_id', sa.Integer(), nullable=True),
    sa.Column('address', sa.Unicode(length=200), nullable=True),
    sa.ForeignKeyConstraint(['card_transaction_id'], [u'card_transaction.object_id'], ),
    sa.ForeignKeyConstraint(['user_id'], [u'user.object_id'], ),
    sa.PrimaryKeyConstraint('object_id')
    )
    op.create_table('user_announce_link',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('announcement_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['announcement_id'], [u'announcement.object_id'], ),
    sa.ForeignKeyConstraint(['user_id'], [u'user.object_id'], )
    )
    op.create_table('log_ticket_link',
    sa.Column('log_id', sa.Integer(), nullable=True),
    sa.Column('ticket_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['log_id'], [u'log.object_id'], ),
    sa.ForeignKeyConstraint(['ticket_id'], [u'ticket.object_id'], )
    )
    op.create_table('transaction_item',
    sa.Column('object_id', sa.Integer(), nullable=False),
    sa.Column('item_type', sa.Enum(u'Ticket', u'Ticket Refund', u'Administration Fee', u'Postage'), nullable=False),
    sa.Column('_value', sa.Integer(), nullable=True),
    sa.Column('_description', sa.Unicode(length=100), nullable=True),
    sa.Column('transaction_id', sa.Integer(), nullable=False),
    sa.Column('ticket_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['ticket_id'], [u'ticket.object_id'], ),
    sa.ForeignKeyConstraint(['transaction_id'], [u'transaction.object_id'], ),
    sa.PrimaryKeyConstraint('object_id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('transaction_item')
    op.drop_table('log_ticket_link')
    op.drop_table('user_announce_link')
    op.drop_table('transaction')
    op.drop_table('log')
    op.drop_table('email_announce_link')
    op.drop_table('waiting')
    op.drop_table('voucher')
    op.drop_table('ticket')
    op.drop_table('card_transaction')
    op.drop_table('announcement')
    op.drop_table('user')
    op.drop_table('statistic')
    op.drop_table('photo')
    op.drop_table('college')
    op.drop_table('battels')
    op.drop_table('affiliation')
    ### end Alembic commands ###