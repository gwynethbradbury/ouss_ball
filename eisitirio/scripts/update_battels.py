# coding: utf-8
"""Script to update matching from users to Battels accounts."""

from __future__ import unicode_literals

import flask_script as script
# from flask.ext import script

from eisitirio import app
from eisitirio.database import db
from eisitirio.database import models

APP = app.APP#DB = db.DB
from eisitirio.app import eisitiriodb as DB

class UpdateBattelsCommand(script.Command):
    """Flask-Script command for rematching users to battels accounts."""

    help = 'Match users to battels accounts by email'

    @staticmethod
    def run():
        """Perform the matching."""
        with APP.app_context():
            for user in models.User.query.all():
                if user.battels is not None and user.affiliation_verified is None:
                    print user.full_name
                    user.affiliation_verified = True
                    DB.session.commit()
                    continue

                battels = models.Battels.query.filter(
                    models.Battels.email == user.email
                ).first()

                if battels is not None:
                    user.battels = battels
                    user.affiliation_verified = True
                    DB.session.commit()
