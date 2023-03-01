# coding: utf-8
"""Database model for tickets."""

from __future__ import unicode_literals

import datetime
import string

from sqlalchemy.ext import hybrid

from eisitirio import app
from eisitirio.database import db
from eisitirio.helpers import util
import flask
APP = flask.current_app#app.APP#DB = db.DB
from eisitirio.app import eisitiriodb as DB

class Ticket(DB.Model):
    """Model for tickets."""
    __tablename__ = 'ticket'
    object_id = DB.Column(DB.Integer,primary_key=True)

    ticket_type = DB.Column(
        DB.Unicode(50),
        nullable=False
    )

    paid = DB.Column(
        DB.Boolean(),
        default=False,
        nullable=False
    )
    entered = DB.Column(
        DB.Boolean(),
        default=False,
        nullable=False
    )
    cancelled = DB.Column(
        DB.Boolean(),
        default=False,
        nullable=False
    )

    price_ = DB.Column(
        DB.Integer(),
        nullable=False
    )
    note = DB.Column(
        DB.UnicodeText(),
        nullable=True
    )
    expires = DB.Column(
        DB.DateTime(),
        nullable=True
    )
    barcode = DB.Column(
        DB.Unicode(20),
        unique=True,
        nullable=True
    )
    claim_code = DB.Column(
        DB.Unicode(17), # 3 groups of 5 digits separated by dashes
        nullable=True
    )
    claims_made = DB.Column(
        DB.Integer,
        nullable=False,
        default=0
    )
    owner_id = DB.Column(
        DB.Integer,
        DB.ForeignKey('user.object_id'),
        nullable=False
    )
    owner = DB.relationship(
        'User',
        backref=DB.backref(
            'tickets',
            lazy='dynamic',
            order_by='Ticket.cancelled'
                     # todo: check, was b.'Ticket.cancelled'
        ),
        foreign_keys=[owner_id]
    )

    holder_id = DB.Column(
        DB.Integer,
        DB.ForeignKey('user.object_id'),
        nullable=True
    )
    holder = DB.relationship(
        'User',
        backref=DB.backref(
            'held_ticket',
            uselist=False
        ),
        foreign_keys=[holder_id]
    )
    holder_name = DB.Column(
        DB.String(60),
        nullable=True,
        default="Unassigned"
    )

    def __init__(self, owner, ticket_type, price):
        self.owner = owner
        self.ticket_type = ticket_type
        self.price = price

        self.expires = (datetime.datetime.utcnow() +
                        APP.config['TICKET_EXPIRY_TIME'])

        self.claim_code = '-'.join(
            util.generate_key(5, string.digits)
            for _ in range(3)
        )

    def __repr__(self):
        return '<Ticket {0} owned by {1} ({2})>'.format(
            self.object_id,
            self.owner.full_name,
            self.owner.object_id
        )


    def can_be_cancelled(self):
        if datetime.datetime.utcnow()<datetime.datetime(2023,5,5) and not self.cancelled and not self.paid:
            return True
        return False

    def can_be_resold(self):
        return False

    def can_be_claimed(self):
        if self.holder_name == 'Unassigned':
            return True
        return False

    def can_be_reclaimed(self):
        # if self.paid and datetime.datetime.utcnow()<datetime.datetime(2018,5,11) and not self.cancelled and self.holder_id==self.owner_id:
        #     return True
        return False

    def has_holder(self):
        if not self.holder_id == None:
            return True
        return False

    def can_be_paid_for(self):
        if self.paid==0:
            return True
        return False

    def can_be_collected(self):
        if self.paid:
            return True
        return False

    def is_assigned(self):
        if self.holder_name=='Unassigned':
            return False
        return True

    @staticmethod
    def get_by_claim_code(code):
        return Ticket.query.filter_by(claim_code=code).first()

    @property
    def price_pounds(self):
        """Get the price of this ticket as a string of pounds and pence."""
        price = '{0:03d}'.format(self.price)
        return price[:-2] + '.' + price[-2:]

    @property
    def transaction(self):
        """Get the transaction this ticket was paid for in."""
        for transaction_item in self.transaction_items:
            if transaction_item.transaction.paid:
                return transaction_item.transaction

        return None

    @property
    def payment_method(self):
        """Get the payment method for this ticket."""
        transaction = self.transaction

        if transaction:
            return transaction.payment_method
        else:
            return 'Unknown Payment Method'

    @property
    def price(self):
        """Get the price of the ticket."""
        return self.price_

    @property
    def status(self):
        """Get the status of this ticket."""
        if self.cancelled:
            return 'Cancelled.'
        elif not self.paid:
            return 'Awaiting payment. Expires {0}.'.format(
                self.expires.strftime('%H:%M %d/%m/%Y')
            )
        elif self.entered:
            return 'Used for entry.'
        elif self.collected and self.holder:
            return 'Ticket Sent to {0}.'.format(self.holder.full_name)
        elif self.collected:
            return 'Collected as {0}.'.format(self.barcode)
        # elif self.holder is None:
        #     return 'Awaiting ticket holder.'
        elif self.holder_name == 'Unassigned':
            return 'Awaiting ticket holder.'
        elif APP.config['REQUIRE_USER_PHOTO']:
            if not self.holder.photo.verified:
                return 'Awaiting verification of holder photo.'
        else:
            # return 'Held by {0}.'.format(self.holder.full_name)
            return 'Assigned to {0}.'.format(self.holder_name)

    @price.setter
    def price(self, value):
        """Set the price of the ticket."""
        self.price_ = max(value, 0)

        if self.price_ == 0:
            self.mark_as_paid()

    @hybrid.hybrid_property
    def collected(self):
        """Has this ticket been assigned a barcode."""
        return self.barcode != None # pylint: disable=singleton-comparison

    def mark_as_paid(self):
        """Mark the ticket as paid, and clear any expiry."""
        self.paid = True
        self.expires = None

    def add_note(self, note):
        """Add a note to the ticket."""
        if not note.endswith('\n'):
            note = note + '\n'

        if self.note is None:
            self.note = note
        else:
            self.note = self.note + note

    @staticmethod
    def count():
        """How many tickets have been sold."""
        # TODO
        return Ticket.query.filter(Ticket.cancelled == False).count() # pylint: disable=singleton-comparison

    @staticmethod
    def write_csv_header(csv_writer):
        """Write the header of a CSV export file."""
        csv_writer.writerow([
            'Ticket ID',
            'Ticket Type',
            'Paid',
            'Collected',
            'Entered',
            'Cancelled',
            'Price (Pounds)',
            'Holder\'s Name',
            'Notes',
            'Expires',
            'Barcode',
            'Owner\' User ID',
            'Owner\'s Name',
        ])

    def write_csv_row(self, csv_writer):
        """Write this object as a row in a CSV export file."""
        csv_writer.writerow([
            self.object_id,
            self.ticket_type,
            'Yes' if self.paid else 'No',
            'Yes' if self.collected else 'No',
            'Yes' if self.entered else 'No',
            'Yes' if self.cancelled else 'No',
            self.price_pounds,
            self.holder.full_name.encode('utf-8') if self.holder is not None else 'N/A',
            self.note,
            self.expires.strftime(
                '%Y-%m-%d %H:%M:%S'
            ) if self.expires is not None else 'N/A',
            self.barcode if self.barcode is not None else 'N/A',
            self.owner_id,
            self.owner.full_name.encode('utf-8'),
        ])

    def slug(self):
        if self.ticket_type=='early_member_both':
            return 'Early Bird Member Including Afternoon Workshops'
        elif self.ticket_type=='member_both':
            return 'Member Including Afternoon Workshops'
        elif self.ticket_type=='member_ball':
            return 'Member Ball Only'
        elif self.ticket_type=='early_standard_ball':
            return 'Early Bird Ball Including Afternoon Workshops'
        elif self.ticket_type=='standard_ball':
            return 'Ball Only'
        elif self.ticket_type=='standard_both':
            return 'Ball Including Afternoon Workshops'

        return 'not specified'
