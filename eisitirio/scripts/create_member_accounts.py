# coding: utf-8
"""Script to prefill the database with colleges and affiliations."""

from __future__ import unicode_literals

import os
import uuid

import flask_script as script
# from flask.ext import script

from eisitirio import app
from eisitirio.database import db
from eisitirio.database import models
from eisitirio.database import static
from eisitirio.helpers import photos

import eisitirio.member_list as ML
from eisitirio.views.front import member_password_create as send_set_password

class CreateBetaMemberAccountsCommand(script.Command):
    """Flask-Script command for prefilling the database."""

    help = 'Create accounts for all members and send emails with password reset'

    @staticmethod
    def run():
        """Prefill the database."""
        with app.APP.app_context():
            photo = None
            users=[]
            college = models.College.query.first()
            member_aff = models.Affiliation.query.filter_by(object_id=2).first()
            commit_aff = models.Affiliation.query.filter_by(object_id=3).first()
            for member in ML.beta_member_list:

                m = member[0]#member email
                c = member[1]#code
                aff=member_aff#affiliation
                if c<0:
                    aff = member_aff#normal member: 1
                elif c==1:
                    aff=commit_aff#comittee - free ticket: 2
                user = models.User(
                    m,
                    'oussmember',
                    m,
                    'Not set',
                    '01234567890',
                    college,
                    aff,
                    photo
                )


                user.note = 'Automatically created user from mailing list.\n'
                user.role = 'User'
                user.verified = True
                user.affiliation_verified = True

                users.append(user)

            for u in users:
                db.DB.session.add(u)

            db.DB.session.commit()

            count = users.__len__()
            c=0
            for u in users:
                if send_set_password(u):
                    c=c+1

            print("successfully sent password email to {} of {} OUSS members".format(c,count))
class CreateMemberAccountsCommand(script.Command):
    """Flask-Script command for prefilling the database."""

    help = 'Create accounts for all members and send emails with password reset'

    @staticmethod
    def run():
        """Prefill the database."""
        with app.APP.app_context():
            photo = None
            users=[]
            college = models.College.query.first()
            member_aff = models.Affiliation.query.filter_by(object_id=2).first()
            commit_aff = models.Affiliation.query.filter_by(object_id=3).first()
            for member in ML.real_member_list:

                m = member[0]#member email
                c = member[1]#code
                aff=member_aff#affiliation
                if c<0:
                    aff = member_aff#normal member: 1
                elif c==1:
                    aff=commit_aff#comittee - free ticket: 2
                elif c==2:
                    aff=member_aff
                user = models.User(
                    m,
                    'oussmember',
                    m,
                    'Not set',
                    '01234567890',
                    college,
                    aff,
                    photo,is_member=True
                )


                user.note = 'Automatically created user from mailing list.\n'
                user.role = 'User'
                user.verified = True
                user.affiliation_verified = True

                users.append(user)

            for u in users:
                db.DB.session.add(u)

            db.DB.session.commit()

            count = users.__len__()
            c=0
            for u in users:
                if send_set_password(u):
                    c=c+1

            print("successfully sent password email to {} of {} OUSS members".format(c,count))
