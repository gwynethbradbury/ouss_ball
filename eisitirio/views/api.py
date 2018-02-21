# coding: utf-8
"""Views related to the purchase process."""

from __future__ import unicode_literals

import flask_login as login
# from flask.ext import login
import flask
from sqlalchemy import or_

from eisitirio import app
from eisitirio.database import db
from eisitirio.database import models

APP = flask.current_app#app.APP#DB = db.DB
from eisitirio.app import eisitiriodb as DB

API = flask.Blueprint('api', __name__)

@API.route('/api/verify-ticket/<int:ticket_id>')
def api_verify_ticket(ticket_id):
    ticket = models.Ticket.query.get_or_404(ticket_id)

    print ticket

    if ticket is not None:
        return "true"
    else:
        return "false"
