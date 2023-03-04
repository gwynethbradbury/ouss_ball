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
from eisitirio.helpers import validators
from eisitirio.helpers import login_manager
from eisitirio.logic import cancellation_logic
from eisitirio.logic import realex_logic
from eisitirio.logic import paypal_logic
from eisitirio.logic import purchase_logic
from eisitirio.logic import payment_logic
# from eisitirio.logic.custom_logic import ticket_logic
# APP = app.APP#DB = db.DB
APP = flask.current_app
from eisitirio.app import eisitiriodb as DB
from eisitirio import dbconfig

PURCHASE = flask.Blueprint('purchase', __name__)



# CREATE TABLE ipn (unix INT(10), payment_date VARCHAR(30), transhash VARCHAR(200), last_name VARCHAR(30), payment_gross FLOAT(6,2), payment_fee FLOAT(6,2), payment_net FLOAT(6,2), payment_status VARCHAR(15), txn_id VARCHAR(25));

import time

@PURCHASE.route('/success/', methods=['GET'])
def success():
    print(flask.request.args)
    if flask.request.method == 'POST':
        payer_id = flask.request.form.get('payer_id')
        print(payer_id)
        data = flask.request.form
    else:
        payer_id = flask.request.args.get('payer_id')
        print(payer_id)
        data = flask.request.args



    try:
        arg = ''
        flask.request.parameter_storage_class = ImmutableOrderedMultiDict
        values = data
        for x, y in values.items():
            arg += "&{x}={y}".format(x=x, y=y)

        validate_url = 'https://www.paypal.com' \
                       '/cgi-bin/webscr?cmd=_notify-validate{arg}' \
            .format(arg=arg)
        print(requests.get(validate_url))
        r = requests.get(validate_url)
        try:
            print(flask.request.form.get('item_number'))
        except Exception as e:
            return print(e)
        if True: #r.text == 'VERIFIED':
            try:
                payer_email = thwart(data.get('payer_email'))
                unix = int(time.time())
                payment_date = thwart(data.get('payment_date'))
                transhash = thwart(data.get('custom'))
                last_name = thwart(data.get('last_name'))
                payment_gross = thwart(data.get('payment_gross'))
                payment_fee = thwart(data.get('payment_fee'))
                payment_net = float(payment_gross) - float(payment_fee)
                payment_status = thwart(data.get('payment_status'))
                txn_id = thwart(data.get('txn_id'))
                transaction_number = int(thwart(data.get('item_number')))
                print("transaction_number is " + thwart(data.get('item_number')))
                paypal_logic.process_payment_new(transaction_number, transhash, paypal_id=txn_id, payment_gross=float(payment_gross))
            except Exception as e:
                with open('/tmp/ipnout.txt', 'a') as f:
                    data = 'ERROR WITH IPN DATA\n' + str(values) + '\n'
                    f.write(data)

            with open('/tmp/ipnout.txt', 'a') as f:
                data = 'SUCCESS\n' + str(values) + '\n'
                f.write(data)

            # TODO PAYMENT COMPLETE LOGIC
            # print("INSERT INTO ipn (unix, payment_date, transhash, last_name, payment_gross, payment_fee, payment_net, payment_status, txn_id) VALUES ({}, {}, {}, {}, {}, {}, {}, {}, {})"
            #         .format(unix, payment_date, transhash, last_name, payment_gross, payment_fee, payment_net, payment_status,txn_id)
            #      )
            # from eisitirio.app import eisitiriodb as DB
            # from sqlalchemy.sql import text
            # DB.session.execute(text
            #     ("INSERT INTO ipn (unix, payment_date, transhash, last_name, payment_gross, payment_fee, payment_net, payment_status, txn_id) VALUES ({}, {}, {}, {}, {}, {}, {}, {}, {})"
            #         .format(unix, payment_date, transhash, last_name, payment_gross, payment_fee, payment_net, payment_status,txn_id)
            #      ))
            # DB.session.commit()

            # c, conn = connection()
            # c.execute(
            #     "INSERT INTO ipn (unix, payment_date, username, last_name, payment_gross, payment_fee, payment_net, payment_status, txn_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            #     (unix, payment_date, username, last_name, payment_gross, payment_fee, payment_net, payment_status,
            #      txn_id))
            # conn.commit()
            # c.close()
            # conn.close()
            # gc.collect()

        else:
            with open('/tmp/ipnout.txt', 'a') as f:
                data = 'FAILURE\n' + str(values) + '\n'
                f.write(data)

        # return r.text
        print(r.text)

        try:
            return flask.render_template("success.html")
        except Exception as e:
            return str(e)

    except Exception as e:
        print(e)
        return str(e)





    try:
        return flask.render_template("success.html")
    except Exception as e:
        return str(e)

import requests
from werkzeug.datastructures import ImmutableOrderedMultiDict
import flask_mysqldb
# todo:
def thwart(a):
    return a #flask_mysqldb.escape_string(a)

@PURCHASE.route('/ipn/', methods=['POST'])
def ipn():
    print("HIHIHIHIHI")
    return
#     try:
#         arg = ''
#         flask.request.parameter_storage_class = ImmutableOrderedMultiDict
#         print('ZZZZZZZ')
#         values = flask.request.form
#         for x, y in values.items():
#             arg += "&{x}={y}".format(x=x, y=y)
#         print('ZZZZZZZ')
#
#         validate_url = 'https://www.sandbox.paypal.com' \
#                        '/cgi-bin/webscr?cmd=_notify-validate{arg}' \
#             .format(arg=arg)
#         print('ZZZZZZZ')
#         print(requests.get(validate_url))
#         r = requests.get(validate_url)
#         try:
#             print(flask.request.form.get('item_number'))
#         except Exception as e:
#             return print(e)
#         if r.text == 'VERIFIED':
#             try:
#                 payer_email = thwart(flask.request.form.get('payer_email'))
#                 unix = int(time.time())
#                 payment_date = thwart(flask.request.form.get('payment_date'))
#                 username = thwart(flask.request.form.get('custom'))
#                 last_name = thwart(flask.request.form.get('last_name'))
#                 payment_gross = thwart(flask.request.form.get('payment_gross'))
#                 payment_fee = thwart(flask.request.form.get('payment_fee'))
#                 payment_net = float(payment_gross) - float(payment_fee)
#                 payment_status = thwart(flask.request.form.get('payment_status'))
#                 txn_id = thwart(flask.request.form.get('txn_id'))
#                 transaction_number = thwart(flask.request.form.get('item_number'))
#                 print("transaction_number is "+transaction_number)
#                 paypal_logic.process_payment_new(transaction_id, hash, paypal_id=txn_id)
#             except Exception as e:
#                 with open('/tmp/ipnout.txt', 'a') as f:
#                     data = 'ERROR WITH IPN DATA\n' + str(values) + '\n'
#                     f.write(data)
#
#             with open('/tmp/ipnout.txt', 'a') as f:
#                 data = 'SUCCESS\n' + str(values) + '\n'
#                 f.write(data)
#
#             # TODO PAYMENT COMPLETE LOGIC
#             print("INSERT INTO ipn (unix, payment_date, username, last_name, payment_gross, payment_fee, payment_net, payment_status, txn_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
#                 (unix, payment_date, username, last_name, payment_gross, payment_fee, payment_net, payment_status,
#                  txn_id))
#             from eisitirio.app import eisitiriodb as DB
#             DB.session.execute("INSERT INTO ipn (unix, payment_date, username, last_name, payment_gross, payment_fee, payment_net, payment_status, txn_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
#                 (unix, payment_date, username, last_name, payment_gross, payment_fee, payment_net, payment_status,
#                  txn_id))
#             DB.session.commit()
#             # c, conn = connection()
#             # c.execute(
#             #     "INSERT INTO ipn (unix, payment_date, username, last_name, payment_gross, payment_fee, payment_net, payment_status, txn_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
#             #     (unix, payment_date, username, last_name, payment_gross, payment_fee, payment_net, payment_status,
#             #      txn_id))
#             # conn.commit()
#             # c.close()
#             # conn.close()
#             # gc.collect()
#
#         else:
#             with open('/tmp/ipnout.txt', 'a') as f:
#                 data = 'FAILURE\n' + str(values) + '\n'
#                 f.write(data)
#
#         return r.text
#     except Exception as e:
#         print(e)
#         return str(e)




@PURCHASE.route('/purchase', methods=['GET', 'POST'])
@login.login_required
def purchase_home():
    """First step of the purchasing flow.

    Checks if the user can purchase tickets, and processes the purchase form.
    """
    if login.current_user.purchase_group:
        if login.current_user == login.current_user.purchase_group.leader:
            if APP.config['TICKETS_ON_SALE']:
                return flask.redirect(flask.url_for('group_purchase.checkout'))
            else:
                flask.flash(
                    (
                        'You cannot currently purchase tickets because you are '
                        'leading a purchase group. You will be able to '
                        'purchase tickets on behalf of your group when general '
                        'release starts.'
                    ),
                    'info'
                )
                return flask.redirect(flask.url_for('dashboard.dashboard_home'))
        else:
            flask.flash(
                (
                    'You cannot currently purchase tickets because you are a '
                    'member of a purchase group. Your group leader {0} will be '
                    'able to purchase tickets on behalf of your group when '
                    'general release starts.'
                ).format(login.current_user.purchase_group.leader.full_name),
                'info'
            )
            return flask.redirect(flask.url_for('dashboard.dashboard_home'))

    ticket_info = purchase_logic.get_ticket_info(
        login.current_user
    )
    if models.Waiting.query.count() > 0 or not ticket_info.ticket_types:
        flask.flash(
            'You are not able to purchase tickets at this time.',
            'info'
        )

        if purchase_logic.wait_available(login.current_user):
            flask.flash(
                (
                    'Please join the waiting list, and you will be allocated '
                    'tickets as they become available'
                ),
                'info'
            )
            return flask.redirect(flask.url_for('purchase.wait'))
        else:
            return flask.redirect(flask.url_for('dashboard.dashboard_home'))

    num_tickets = {
        ticket_type.slug: 0
        for ticket_type, _ in ticket_info.ticket_types
    }

    if flask.request.method == 'POST':
        for ticket_type, _ in ticket_info.ticket_types:
            num_tickets[ticket_type.slug] = int(
                flask.request.form['num_tickets_{0}'.format(ticket_type.slug)]
            )

        flashes = purchase_logic.validate_tickets(
            ticket_info,
            num_tickets
        )

        payment_method, payment_term = purchase_logic.check_payment_method(
            flashes
        )

        voucher = None
        if (
                'voucher_code' in flask.request.form and
                flask.request.form['voucher_code'] != ''
        ):
            (result, response, voucher) = validators.validate_voucher(
                flask.request.form['voucher_code'])
            if not result:
                flashes.append(
                    (
                        '{} Please clear the discount code field to continue '
                        'without using a voucher.'
                    ).format(response['message'])
                )

        postage, address = purchase_logic.check_postage(flashes)

        if flashes:
            flask.flash(
                (
                    'There were errors in your order. Please fix '
                    'these and try again'
                ),
                'error'
            )
            for msg in flashes:
                flask.flash(msg, 'warning')

            return flask.render_template(
                'purchase/purchase_home.html',
                form=flask.request.form,
                num_tickets=num_tickets,
                ticket_info=ticket_info
            )


        tickets = purchase_logic.create_tickets(
            login.current_user,
            ticket_info,
            num_tickets
        )

        if voucher is not None:
            (success, tickets, error) = voucher.apply(tickets,
                                                      login.current_user)
            if not success:
                flask.flash('Could not use voucher - ' + error, 'error')


        roundup_price = purchase_logic.check_roundup_donation(flashes)

        if roundup_price != 0:
            roundup_donation = None

            roundup_donation = models.RoundupDonation(
                    roundup_price,
                    login.current_user,
            )

            if roundup_donation is not None:
                # Tack on the roundup donation fee to their ticket(s)
                # Entry
                tickets = roundup_donation.apply(tickets)
                DB.session.add(roundup_donation);


        DB.session.add_all(tickets)
        DB.session.commit()

        APP.log_manager.log_event(
            'Purchased Tickets',
            tickets=tickets,
            user=login.current_user
        )

        # return flask.render_template(
        #    'purchase/purchase_home.html',
        #    num_tickets=num_tickets,
        #    ticket_info=ticket_info
        # )
        return payment_logic.do_payment(
         tickets,
         postage,
         payment_method,
         payment_term,
         address
        )
    else:
        return flask.render_template(
            'purchase/purchase_home.html',
            num_tickets=num_tickets,
            ticket_info=ticket_info
        )

@PURCHASE.route('/upgrade', methods=['GET', 'POST'])
def upgrade_ticket_redirect():
    return flask.redirect(flask.url_for('purchase.upgrade_ticket'))

@PURCHASE.route('/purchase/upgrade', methods=['GET', 'POST'])
@login.login_required
def upgrade_ticket():
    """Buy an upgrade ticket

    Checks if the user can purchase tickets, and processes the purchase form.
    """

    price_per_ticket, number_upgrade = purchase_logic.get_ticket_info_for_upgrade(login.current_user)

    if number_upgrade <= 0 or not ticket_logic.can_buy_upgrade(login.current_user):
        flask.flash(
            'You are not able to upgrade tickets at this time.',
            'info'
        )
        return flask.redirect(flask.url_for('dashboard.dashboard_home'))


    if flask.request.method == 'POST':
        selected_tickets = flask.request.form.getlist('tickets[]')
        if not selected_tickets:
            flask.flash(
                'Please select the tickets you want to upgrade.',
                'info'
            )
            return flask.redirect(flask.url_for('purchase.upgrade_ticket'))

        total_amt = price_per_ticket * len(selected_tickets)

        admin_fee = models.AdminFee(
            total_amt,
            "Ticket Upgrade: {0}".format(','.join(selected_tickets)),
            login.current_user,
            login.current_user
        )

        APP.log_manager.log_event(
            'Upgraded Tickets: {0}'.format(', '.join(selected_tickets)),
            admin_fee=admin_fee,
            user=login.current_user
        )

        DB.session.add(admin_fee)
        DB.session.commit()

        return payment_logic.pay_admin_fee(admin_fee, 'Card', 'HT')

    return flask.render_template('purchase/upgrade.html')

@PURCHASE.route('/purchase/wait', methods=['GET', 'POST'])
@login.login_required
def wait():
    """Handles joining the waiting list.

    Checks if the user can join the waiting list, and processes the form to
    create the requisite waiting list entry.
    """
    wait_available = purchase_logic.wait_available(login.current_user)

    if not wait_available:
        flask.flash('You cannot join the waiting list at this time.', 'info')

        return flask.redirect(flask.url_for('dashboard.dashboard_home'))

    if flask.request.method != 'POST':
        return flask.render_template(
            'purchase/wait.html',
            wait_available=wait_available
        )

    flashes = []

    num_tickets = int(flask.request.form['num_tickets'])

    if num_tickets > wait_available:
        flashes.append('You cannot wait for that many tickets')
    elif num_tickets < 1:
        flashes.append('You must wait for at least 1 ticket')

    if flashes:
        flask.flash(
            (
                'There were errors in your order. Please fix '
                'these and try again'
            ),
            'error'
        )

        for msg in flashes:
            flask.flash(msg, 'warning')

        return flask.render_template(
            'purchase/wait.html',
            num_tickets=num_tickets,
            wait_available=wait_available
        )

    DB.session.add(
        models.Waiting(
            login.current_user,
            num_tickets
        )
    )
    DB.session.commit()

    APP.log_manager.log_event(
        'Joined waiting list for {0} tickets'.format(
            num_tickets
        ),
        user=login.current_user
    )

    flask.flash(
        (
            'You have been added to the waiting list for {0} ticket{1}.'
        ).format(
            num_tickets,
            '' if num_tickets == 1 else 's'
        ),
        'success'
    )

    return flask.redirect(flask.url_for('dashboard.dashboard_home'))

@PURCHASE.route('/purchase/complete-payment', methods=['GET', 'POST'])
@login.login_required
def complete_payment():
    """Allow the user to complete payment for tickets.

    Used if card payment fails, or for manually allocated tickets.
    """
    if flask.request.method == 'POST':
        flashes = []

        tickets = models.Ticket.query.filter(
            models.Ticket.object_id.in_(flask.request.form.getlist('tickets[]'))
        ).filter(
            models.Ticket.owner_id == login.current_user.object_id
        ).filter(
            models.Ticket.paid == False # pylint: disable=singleton-comparison
        ).all()

        if not tickets:
            flashes.append('You have not selected any tickets to pay for.')

        method, term = purchase_logic.check_payment_method(flashes)

        postage, address = purchase_logic.check_postage(flashes)

        if flashes:
            flask.flash(
                (
                    'There were errors in your order. Please fix '
                    'these and try again'
                ),
                'error'
            )
            for msg in flashes:
                flask.flash(msg, 'warning')

            return flask.render_template(
                'purchase/complete_payment.html',
                form=flask.request.form
            )

        return payment_logic.do_payment(
            tickets,
            postage,
            method,
            term,
            address
        )
    else:
        return flask.render_template(
            'purchase/complete_payment.html'
        )

@PURCHASE.route('/purchase/cancel', methods=['GET', 'POST'])
@login.login_required
def cancel():
    """Allow the user to cancel tickets."""
    if flask.request.method == 'POST':
        cancellation_logic.cancel_tickets(
            login.current_user.active_tickets.filter(
                models.Ticket.object_id.in_(
                    flask.request.form.getlist('tickets[]')
                )
            ).all()
        )

    return flask.render_template('purchase/cancel.html')

@PURCHASE.route('/resell', methods=['GET', 'POST'])
@login.login_required
def resell():
    """Allow the user to resell tickets.

    Resell here actually means that the reseller's tickets will be cancelled,
    and new tickets created in the account of the recipient.
    """
    if flask.request.method != 'POST':
        return flask.render_template('purchase/resell.html')

    tickets = login.current_user.active_tickets.filter(
        models.Ticket.object_id.in_(flask.request.form.getlist('tickets[]'))
    ).all()

    resell_to = models.User.get_by_email(flask.request.form['resell_to'])

    flashes = []

    if not tickets:
        flashes.append("You haven't selected any tickets.")

    if not resell_to:
        flashes.append('No user with that email exists')
    elif resell_to == login.current_user:
        flashes.append('You can\'t resell tickets to yourself')

    if flashes:
        for flash in flashes:
            flask.flash(flash, 'error')

        return flask.render_template('purchase/resell.html')

    if cancellation_logic.cancel_tickets(tickets, quiet=True):
        found_uncancelled = False

        new_tickets = []

        ticket_type = APP.config['DEFAULT_TICKET_TYPE']

        for ticket in tickets:
            if ticket.cancelled:
                new_tickets.append(models.Ticket(
                    resell_to,
                    ticket_type.slug,
                    ticket_type.price
                ))
            else:
                found_uncancelled = True

        DB.session.add_all(new_tickets)
        DB.session.commit()

        APP.email_manager.send_template(
            resell_to.email,
            'You have been resold tickets',
            'resale.email',
            reseller=login.current_user,
            resell_to=resell_to,
            num_tickets=len(new_tickets),
            expiry=new_tickets[0].expires
        )

        APP.log_manager.log_event(
            'Cancelled tickets for resale',
            tickets=tickets,
            user=login.current_user
        )

        APP.log_manager.log_event(
            'Created tickets from resale',
            tickets=new_tickets,
            user=resell_to
        )

        if found_uncancelled:
            flask.flash('The resale was partially successful.', 'success')
            flask.flash(
                (
                    'Some of your tickets could not be automatically '
                    'cancelled, and so could not be resold. You can try again '
                    'later, but if this problem continues to occur, you should '
                    'contact <a href="{0}">the ticketing officer</a>'
                ).format(
                    APP.config['TICKETS_EMAIL_LINK']
                ),
                'warning'
            )
        else:
            flask.flash('The resale was successful.', 'success')
    else:
        flask.flash(
            (
                'None of your tickets could be automatically cancelled, and so '
                'they could not be resold. You can try again later, but if '
                'this problem continues to occur, you should contact '
                '<a href="{0}">the ticketing officer</a>'
            ).format(
                APP.config['TICKETS_EMAIL_LINK']
            ),
            'error'
        )

    return flask.render_template('purchase/resell.html')

@PURCHASE.route('/purchase/postage', methods=['GET', 'POST'])
@login.login_required
def buy_postage():
    """Allow the user to buy postage for tickets."""
    if flask.request.method == 'POST':
        flashes = []

        tickets = models.Ticket.query.filter(
            models.Ticket.object_id.in_(flask.request.form.getlist('tickets[]'))
        ).filter(
            models.Ticket.cancelled == False # pylint: disable=singleton-comparison
        ).filter(or_(
            models.Ticket.owner == login.current_user,
            models.Ticket.holder == login.current_user
        )).all()

        if not tickets:
            flashes.append(
                'You have not selected any tickets to buy postage for.'
            )

        method, term = purchase_logic.check_payment_method(flashes)

        postage, address = purchase_logic.check_postage(flashes)

        if flashes:
            flask.flash(
                (
                    'There were errors in your order. Please fix '
                    'these and try again'
                ),
                'error'
            )
            for msg in flashes:
                flask.flash(msg, 'warning')

            return flask.render_template(
                'purchase/buy_postage.html',
                form=flask.request.form
            )

        return payment_logic.buy_postage(
            tickets,
            postage,
            method,
            term,
            address
        )

    return flask.render_template('purchase/buy_postage.html')

@PURCHASE.route(
    '/purchase/admin_fee/<int:admin_fee_id>',
    methods=['GET', 'POST']
)
@login.login_required
def pay_admin_fee(admin_fee_id):
    """Allow the user to pay an admin fee."""
    admin_fee = models.AdminFee.query.get_or_404(admin_fee_id)

    if not admin_fee:
        flask.flash('Admin Fee not found', 'warning')
    elif admin_fee.charged_to != login.current_user:
        flask.flash('That is not your admin fee to pay.', 'warning')
    elif admin_fee.paid:
        flask.flash('That admin fee has been paid.', 'warning')
    else:
        if flask.request.method == 'POST':
            flashes = []

            payment_method, payment_term = purchase_logic.check_payment_method(
                flashes
            )

            if flashes:
                flask.flash(
                    (
                        'There were errors in your input. Please fix '
                        'these and try again'
                    ),
                    'error'
                )
                for msg in flashes:
                    flask.flash(msg, 'warning')

                return flask.render_template(
                    'purchase/pay_admin_fee.html',
                    fee=admin_fee
                )

            return payment_logic.pay_admin_fee(admin_fee, payment_method,
                                               payment_term)
        else:
            return flask.render_template(
                'purchase/pay_admin_fee.html',
                fee=admin_fee
            )

    return flask.redirect(flask.request.referrer or
                          flask.url_for('dashboard.dashboard_home'))

@PURCHASE.route('/purchase/payment-interstitial/<int:transaction_id>', methods=['GET'])
@login.login_required
def payment_interstitial(transaction_id):
    form = realex_logic.generate_payment_form(
        models.Transaction.query.get_or_404(transaction_id)
    )
    return flask.render_template('purchase/payment_interstitial.html', form=form)




# import braintree

# gateway = braintree.BraintreeGateway(access_token='access_token$sandbox$z8yxpx29x7tqntyb$efc5ea183c041f87ec0f678b35baa11d')
# @PURCHASE.route("/purchase/client_token", methods=["GET"])
# def client_token():
#     return gateway.client_token.generate()

# @PURCHASE.route("/checkout", methods=["POST"])
# def create_purchase():
#     nonce = flask.request.form["payment_method_nonce"]
#     # Use payment method nonce here...



    # result = gateway.transaction.sale({
    #     "amount" : flask.request.form["amount"],
    #     "merchant_account_id": "USD",
    #     "payment_method_nonce" : flask.request.form["payment_method_nonce"],
    #     "order_id" : "Mapped to PayPal Invoice Number",
    #     "descriptor": {
    #       "name": "Descriptor displayed in customer CC statements. 22 char max"
    #     },
    #     "shipping": {
    #       "first_name": "OU",
    #       "last_name": "SS",
    #       "company": "OUSS",
    #       "street_address": "Oxford",
    #       "extended_address": "Oxford",
    #       "locality": "Oxford",
    #       "region": "OX",
    #       "postal_code": "OX1 2EA",
    #       "country_code_alpha2": "UK"
    #     },
    #     "options" : {
    #       "paypal" : {
    #         "custom_field" : "PayPal custom field",
    #         "description" : "Description for PayPal email receipt"
    #       },
    #     }
    # })
    # if result.is_success:
    #     "Success ID: ".format(result.transaction.id)
    # else:
    #     format(result.message)








from paypal import PayPalConfig
from paypal import PayPalInterface

config = PayPalConfig(API_USERNAME="gwyneth.bradbury_api1.googlemail.com",
                      API_PASSWORD="SFE8ECYRR8VPWPAT",
                      API_SIGNATURE="A5Q8Xsj7f-LN-LLYpJahUp1iNoCcAkbCIbqIxpx9steOH36jxT2EBCLS",
                      DEBUG_LEVEL=0)


interface = PayPalInterface(config=config)

from flask import url_for

@PURCHASE.route('/purchase/payment-paypal/<int:transaction_id>', methods=['GET'])
@login.login_required
# @PURCHASE.route("/")
def payment_paypal(transaction_id):
    t = models.Transaction.query.get_or_404(transaction_id)
    form, hash, amount = paypal_logic.generate_payment_form(
        t
    )

    isServer = True
    # if dbconfig.dbhost=='localhost':
    #     isServer=False

    return flask.render_template('purchase/payment_paypal.html',
                                 amount=t.value_pounds_surcharge( app.APP.config['PAYPAL_SURCHARGE']),
                                 transaction_id=transaction_id, hash=hash, surcharge=app.APP.config['PAYPAL_SURCHARGE'],
                                 isServer = isServer)

    # return """
    #     <a href="%s">
    #         <img src="https://www.paypalobjects.com/en_US/i/btn/btn_xpressCheckout.gif">
    #     </a>
    #     """ % url_for('purchase.paypal_redirect',transaction_id=transaction_id)

# @PURCHASE.route('/purchase/payment-paypal/<int:transaction_id>', methods=['GET'])
# @login.login_required
# def payment_paypal(transaction_id):
#     form = paypal_logic.generate_payment_form(
#         models.Transaction.query.get_or_404(transaction_id)
#     )
#     return flask.render_template('purchase/payment_paypal.html', form=form)






@PURCHASE.route("/paypal/redirect")
@login.login_required
def paypal_redirect():
    kw = {
        'amt': '10.00',
        'currencycode': 'USD',
        'returnurl': url_for('purchase.paypal_confirm', _external=True),#'www.oxfordsalsaball.co.uk/purchase/payment-processed',#
        'cancelurl': url_for('purchase.paypal_cancel', _external=True),#'www.oxfordsalsaball.co.uk/purchase/payment-processed',#
        'paymentaction': 'Sale'
    }

    setexp_response = interface.set_express_checkout(**kw)
    return flask.redirect(interface.generate_express_checkout_redirect_url(setexp_response.token))

@PURCHASE.route("/paypal/confirm")
@login.login_required
def paypal_confirm():
    getexp_response = interface.get_express_checkout_details(token=request.args.get('token', ''))

    if getexp_response['ACK'] == 'Success':
        return """
            Everything looks good! <br />
            <a href="%s">Click here to complete the payment.</a>
        """ % url_for('paypal_do', token=getexp_response['TOKEN'])
    else:
        return """
            Oh noes! PayPal returned an error code. <br />
            <pre>
                %s
            </pre>
            Click <a href="%s">here</a> to try again.
        """ % (getexp_response['ACK'], url_for('index'))


@PURCHASE.route("/paypal/do/<string:token>")
@login.login_required
def paypal_do(token):
    getexp_response = interface.get_express_checkout_details(token=token)
    kw = {
        'amt': getexp_response['AMT'],
        'paymentaction': 'Sale',
        'payerid': getexp_response['PAYERID'],
        'token': token,
        'currencycode': getexp_response['CURRENCYCODE']
    }
    interface.do_express_checkout_payment(**kw)

    return flask.redirect(url_for('purchase.paypal_status', token=kw['token']))

@PURCHASE.route("/paypal/status/<string:token>")
@login.login_required
def paypal_status(token):
    checkout_response = interface.get_express_checkout_details(token=token)

    if checkout_response['CHECKOUTSTATUS'] == 'PaymentActionCompleted':
        # Here you would update a database record.
        return """
            Awesome! Thank you for your %s %s purchase.
        """ % (checkout_response['AMT'], checkout_response['CURRENCYCODE'])
    else:
        return """
            Oh no! PayPal doesn't acknowledge the transaction. Here's the status:
            <pre>
                %s
            </pre>
        """ % checkout_response['CHECKOUTSTATUS']

@PURCHASE.route("/paypal/cancel")
@login.login_required
def paypal_cancel():
    return flask.redirect(url_for('purchase.payment_paypal'))

# if __name__ == '__main__':
#     app.run(host='127.0.0.1', port=8338, debug=True)









@PURCHASE.route('/purchase/payment-processed', methods=['GET','POST'])
def payment_processed():
    """Callback from realex. Data received in a POST request, see the
    Realex website for details on how the data is structured. This records
    the end result of the transaction in the database (using
    'process_payment') and then redirects the user to their dashboard.
    Errors and warnings are recorded using flask.flash inside of
    process_payment."""
    if flask.request.method == 'POST':
        response = realex_logic.process_payment(flask.request)
        return flask.render_template('purchase/payment_processed.html')
        # return flask.redirect(flask.url_for('dashboard.dashboard_home'))
    else:
        return flask.render_template('purchase/payment_processed.html')
        # return flask.redirect(flask.url_for('dashboard.dashboard_home'))


@PURCHASE.route('/purchase/paypal-processed/<int:transaction_id>/<string:hash>', methods=['GET','POST'])
def _paypal_processed(transaction_id,hash,paypal_id=0):
    pass
@PURCHASE.route('/purchase/paypal-processed/<int:transaction_id>/<string:hash>/<string:paypal_id>', methods=['GET','POST'])
def paypal_processed(transaction_id,hash,paypal_id):
    """Callback from realex. Data received in a POST request, see the
    Realex website for details on how the data is structured. This records
    the end result of the transaction in the database (using
    'process_payment') and then redirects the user to their dashboard.
    Errors and warnings are recorded using flask.flash inside of
    process_payment."""
    response = paypal_logic.process_payment(flask.request,transaction_id,hash,paypal_id=paypal_id)
    return flask.render_template('purchase/payment_processed.html')
    # return flask.redirect(flask.url_for('dashboard.dashboard_home'))

@PURCHASE.route('/purchase/verify-ticket/<int:ticket_id>')
def api_verify_ticket(ticket_id):
    ticket = models.Ticket.query.get_or_404(ticket_id)

    print(ticket)

    if ticket is not None:
        return "true"
    else:
        return "false"
