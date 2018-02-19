# coding: utf-8
"""Database model for representing a users affiliation to their college."""

from __future__ import unicode_literals

from eisitirio.database import db
#DB = db.DB
from eisitirio.app import eisitiriodb as DB

class Affiliation(DB.Model):
    """Model for representing a users affiliation to their college."""
    __tablename__ = 'affiliation'
    object_id = DB.Column(DB.Integer, primary_key=True)

    name = DB.Column(
        DB.Unicode(25),
        nullable=False
    )

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Affiliation {0}: {1}>'.format(self.object_id, self.name)

def get_static():
    """Get static instances of the Affiliation model."""
    return [
        Affiliation('Student'),
        Affiliation('Graduand'),
        Affiliation('Graduate/Alumnus'),
        Affiliation('Staff/Fellow'),
        Affiliation('Foreign Exchange Student'),
        Affiliation('Other'),
        Affiliation('None'),
    ]
