# coding: utf-8
"""Database model for an announcement sent to registered users."""

from __future__ import unicode_literals

import datetime

from eisitirio import app
from eisitirio.database import db
from eisitirio.database import user
import flask
APP = flask.current_app#app.APP
#DB = db.DB
from eisitirio.app import eisitiriodb as DB
USER_ANNOUNCE_LINK = DB.Table(
    'user_announce_link',
    DB.Model.metadata,
    DB.Column(
        'user_id',
        DB.Integer,
        DB.ForeignKey('user.object_id')
    ),
    DB.Column(
        'announcement_id',
        DB.Integer,
        DB.ForeignKey('announcement.object_id')
    )
)

EMAIL_ANNOUNCE_LINK = DB.Table(
    'email_announce_link',
    DB.Model.metadata,
    DB.Column(
        'user_id',
        DB.Integer,
        DB.ForeignKey('user.object_id')
    ),
    DB.Column(
        'announcement_id',
        DB.Integer,
        DB.ForeignKey('announcement.object_id')
    )
)

class Announcement(DB.Model):
    """Model for an announcement sent to registered users."""
    __tablename__ = 'announcement'
    object_id = DB.Column(DB.Integer, primary_key=True)

    timestamp = DB.Column(
        DB.DateTime(),
        nullable=False
    )
    content = DB.Column(
        DB.UnicodeText(65536),
        nullable=False
    )
    subject = DB.Column(
        DB.UnicodeText(256),
        nullable=False
    )
    send_email = DB.Column(
        DB.Boolean,
        default=True,
        nullable=False
    )
    use_noreply = DB.Column(
        DB.Boolean,
        default=False,
        nullable=False
    )
    email_sent = DB.Column(
        DB.Boolean,
        default=False,
        nullable=False
    )

    sender_id = DB.Column(
        DB.Integer,
        DB.ForeignKey('user.object_id'),
        nullable=False
    )
    sender = DB.relationship(
        'User',
        backref=DB.backref(
            'announcements-sent',
            lazy='dynamic'
        )
    )

    college_id = DB.Column(
        DB.Integer,
        DB.ForeignKey('college.object_id'),
        nullable=True
    )
    college = DB.relationship(
        'College',
        backref=DB.backref(
            'announcements',
            lazy='dynamic'
        )
    )

    affiliation_id = DB.Column(
        DB.Integer,
        DB.ForeignKey('affiliation.object_id'),
        nullable=True
    )
    affiliation = DB.relationship(
        'Affiliation',
        backref=DB.backref(
            'announcements-received',
            lazy='dynamic'
        )
    )

    is_waiting = DB.Column(
        DB.Boolean,
        nullable=True
    )
    has_tickets = DB.Column(
        DB.Boolean,
        nullable=True
    )
    holds_ticket = DB.Column(
        DB.Boolean,
        nullable=True
    )
    has_collected = DB.Column(
        DB.Boolean,
        nullable=True
    )
    has_uncollected = DB.Column(
        DB.Boolean,
        nullable=True
    )

    users = DB.relationship(
        'User',
        secondary=USER_ANNOUNCE_LINK,
        backref='announcements'
    )

    emails = DB.relationship(
        'User',
        secondary=EMAIL_ANNOUNCE_LINK,
        lazy='dynamic'
    )

    def __init__(self,
                 subject,
                 content,
                 sender,
                 send_email,
                 college=None,
                 affiliation=None,
                 has_tickets=None,
                 holds_ticket=None,
                 is_waiting=None,
                 has_collected=None,
                 has_uncollected=None,
                 use_noreply=False):
        self.timestamp = datetime.datetime.utcnow()
        self.subject = subject
        self.content = content
        self.sender = sender
        self.send_email = send_email
        self.use_noreply = use_noreply
        self.college = college
        self.affiliation = affiliation
        self.has_tickets = has_tickets
        self.holds_ticket = holds_ticket
        self.is_waiting = is_waiting
        self.has_collected = has_collected
        self.has_uncollected = has_uncollected

        recipient_query = user.User.query

        if self.college is not None:
            recipient_query = recipient_query.filter(
                user.User.college == self.college
            )

        if self.affiliation is not None:
            recipient_query = recipient_query.filter(
                user.User.affiliation == self.affiliation
            )

        for recipient in recipient_query.all():
            if (
                    ( # pylint: disable=too-many-boolean-expressions
                        self.has_tickets is None or
                        recipient.has_tickets() == self.has_tickets
                    ) and
                    (
                        self.holds_ticket is None or
                        recipient.has_held_ticket() == self.holds_ticket
                    ) and
                    (
                        self.is_waiting is None or
                        recipient.is_waiting == self.is_waiting
                    ) and
                    (
                        self.has_collected is None or
                        recipient.has_collected_tickets() == self.has_collected
                    ) and
                    (
                        self.has_uncollected is None or (
                            recipient.has_uncollected_tickets() ==
                            self.has_uncollected
                        )
                    )
            ):
                self.users.append(recipient)
                if send_email:
                    self.emails.append(recipient)

    def __repr__(self):
        return '<Announcement {0}: {1}>'.format(self.object_id, self.subject)

    def send_emails(self, count):
        """Send the announcement as an email to a limited number of recipients.

        Used for batch sending, renders the text of the announcement into an
        email and sends it to users who match the criteria.

        Args:
            count: (int) Maximum number of emails to send

        Returns:
            (int) How much of the original limit is remaining (i.e. |count|
            minus the nuber of emails sent)
        """
        if self.use_noreply:
            sender = APP.config['EMAIL_FROM']
        else:
            sender = self.sender.email

        try:
            for recipient in self.emails:
                if count <= 0:
                    break

                APP.email_manager.send_text(recipient.email, self.subject,
                                            self.content, sender)

                self.emails.remove(recipient)
                count = count - 1
        finally:
            self.email_sent = (self.emails.count() == 0)
            DB.session.commit()

        return count
