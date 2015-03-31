# coding: utf-8
from flask import Blueprint, request, render_template, redirect, flash, url_for
from flask.ext.login import login_required, current_user

from kebleball import app
from kebleball.database import db
from kebleball.database import user
from kebleball.database import ticket

APP = app.APP
DB = db.DB

User = user.User
Ticket = ticket.Ticket

RESALE = Blueprint('resale', __name__)

@RESALE.route('/resale', methods=['GET', 'POST'])
@login_required
def resale_home():
    if request.method == 'POST':
        tickets = Ticket.query \
            .filter(Ticket.object_id.in_(request.form.getlist('tickets[]'))) \
            .filter(Ticket.owner_id == current_user.object_id) \
            .filter(Ticket.paid == True) \
            .all()

        while None in tickets:
            tickets.remove(None)

        resale_to = User.get_by_email(request.form['resaleEmail'])

        if not resale_to:
            flash(
                u'No user with that email exists'
                'error'
            )
            return render_template('resale/resaleHome.html')
        elif resale_to == current_user:
            flash(
                u"You can't resell tickets to yourself",
                'info'
            )
            return render_template('resale/resaleHome.html')

        Ticket.start_resale(tickets, resale_to)

        flash(
            u'The resale process has been started',
            'info'
        )

    return render_template('resale/resaleHome.html')

@RESALE.route('/resale/cancel', methods=['GET', 'POST'])
@login_required
def cancel_resale():
    if request.method == 'POST':
        tickets = Ticket.query \
            .filter(Ticket.object_id.in_(request.form.getlist('tickets[]'))) \
            .filter(Ticket.owner_id == current_user.object_id) \
            .filter(Ticket.paid == True) \
            .all()

        for ticket in tickets:
            if not ticket:
                continue

            ticket.resale_key = None
            ticket.resaleconfirmed = None
            ticket.reselling_to = None
            ticket.reselling_to_id = None

        DB.session.commit()

        flash(
            u'The tickets have been removed from resale',
            'success'
        )

    return render_template('resale/cancelResale.html')

@RESALE.route('/resale/confirm/<int:resale_from>/<int:resale_to>/<key>')
@login_required
def resale_confirm(resale_from, resale_to, key):
    if Ticket.confirm_resale(resale_from, resale_to, key):
        flash(
            (
                u'The resale arrangement has been confirmed. '
                u'You must now arrange payment'
            ),
            'info'
        )
    else:
        flash(
            (
                u'An error occurred, and the resale could not be confirmed. '
                u'If the error persists, please contact <a href="{0}" '
                u'target="_blank">the webmaster</a>.'
            ).format(
                APP.config['WEBSITE_EMAIL_LINK']
            ),
            'warning'
        )

    return redirect(url_for('dashboard.dashboard_home'))

@RESALE.route('/resale/complete/<int:resale_from>/<int:resale_to>/<key>')
@login_required
def resale_complete(resale_from, resale_to, key):
    if Ticket.complete_resale(resale_from, resale_to, key):
        flash(
            (
                u'The resale arrangement has been completed, and the tickets '
                u'have been transferred.'
            ),
            'success'
        )
    else:
        flash(
            (
                u'An error occurred, and the resale could not be completed. '
                u'If the error persists, please contact <a href="{0}" '
                u'target="_blank">the webmaster</a>.'
            ).format(
                APP.config['WEBSITE_EMAIL_LINK']
            ),
            'warning'
        )

    return redirect(url_for('dashboard.dashboard_home'))

@RESALE.route('/resale/cancel/<int:resale_from>/<int:resale_to>/<key>')
@login_required
def resale_cancel(resale_from, resale_to, key):
    if Ticket.cancel_resale(resale_from, resale_to, key):
        flash(
            u'The resale arrangement has been cancelled.',
            'info'
        )
    else:
        flash(
            (
                u'An error occurred, and the resale could not be cancelled. '
                u'If the error persists, please contact <a href="{0}" '
                u'target="_blank">the webmaster</a>.'
            ).format(
                APP.config['WEBSITE_EMAIL_LINK']
            ),
            'warning'
        )

    return redirect(url_for('dashboard.dashboard_home'))
