# coding: utf-8
"""Database model for representing a paypal transaction."""

from __future__ import unicode_literals

from eisitirio import app
from eisitirio.database import db
from eisitirio.database import eway_transaction
from eisitirio.database import transaction
#DB = db.DB
from eisitirio.app import eisitiriodb as DB
APP = app.APP

class PayPalTransaction(transaction.Transaction):
    """Model for representing a paypal transaction."""
    __tablename__ = 'paypal_transaction'
    __mapper_args__ = {'polymorphic_identity': 'PayPal'}
    object_id = DB.Column(DB.Integer, primary_key=True)

    object_id = DB.Column(
        DB.Integer(),
        DB.ForeignKey('transaction.object_id'),
        primary_key=True
    )

    # This holds the order_id
    access_code = DB.Column(
        DB.Unicode(200),
        nullable=True
    )
    charged = DB.Column(
        DB.Integer(),
        nullable=False,
        default=0
    )

    completed = DB.Column(
        DB.DateTime(),
        nullable=True
    )
    result_code = DB.Column(
        DB.Unicode(2),
        nullable=True
    )
    # This holds the PASREF field for realex
    paypal_id = DB.Column(
        DB.String(50),
        nullable=True
    )
    refunded = DB.Column(
        DB.Integer(),
        nullable=False,
        default=0
    )

    order_id = DB.Column(
        DB.Integer(),
        nullable=True
    )

    # eway_transaction_id = DB.Column(
    #     DB.Integer(),
    #     DB.ForeignKey('eway_transaction.object_id'),
    #     nullable=True
    # )
    # eway_transaction = DB.relationship(
    #     'EwayTransaction',
    #     backref=DB.backref(
    #         'transactions',
    #         lazy='dynamic'
    #     )
    # )

    def __init__(self, user, eway_trans=None):
        super(PayPalTransaction, self).__init__(user, 'PayPal')

        # if eway_transaction is not None:
        #     self.eway_transaction = eway_trans

    def __repr__(self):
        return '<PayPalTransaction({0}): {1} item(s)>'.format(
            self.object_id,
            self.items.count()
        )
