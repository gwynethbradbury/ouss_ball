# coding: utf-8
"""Default/global configuration for the application."""

from __future__ import unicode_literals

import datetime
import logging

from eisitirio.helpers import timed_config

# App Config

SECRET_KEY = ('123456790'
    # Generate some bytes.
)
MAINTENANCE_MODE = False
SQLALCHEMY_POOL_RECYCLE = 300
SEND_FILE_MAX_AGE_DEFAULT = 1209600
PREFERRED_URL_SCHEME = 'https'
LOG_LEVEL = logging.DEBUG

MAINTENANCE_FILE_PATH = '/var/www/flask/.maintenance'

SQLALCHEMY_TRACK_MODIFICATIONS = False

THUMBNAIL_SIZE = (200, 200)
IMAGE_EXTENSIONS = [
    'jpg',
    'jpeg',
    'png',
]
IMAGE_ACCEPT_STRING = ",".join("." + ext for ext in IMAGE_EXTENSIONS)

ENABLE_ANALYTICS = False
ANALYTICS_ID = ''
ANALYTICS_DOMAIN = ''

# Tickets Config

_LIMITED_RELEASE_STARTS = datetime.datetime(2015, 11, 30, 9, 0, 0)
_LIMITED_RELEASE_ENDS = datetime.datetime(2016, 01, 25, 9, 0, 0)
GENERAL_RELEASE_STARTS = datetime.datetime(2018, 02, 01, 10, 0, 0)

GUEST_TICKETS_AVAILABLE_TOTAL =  550
GUEST_TICKETS_AVAILABLE = GUEST_TICKETS_AVAILABLE_TOTAL#timed_config.Until(
#     1550,
#     datetime.datetime(2018, 05, 10, 23, 59, 0),
#     1666
# )
TICKET_EXPIRY_TIME = datetime.timedelta(days=1)
MAX_TICKETS_PER_TRANSACTION = 10
MAX_TICKETS_WAITING = 10
GENERAL_RELEASE_MAX_TICKETS = 10
MAX_TICKETS = GENERAL_RELEASE_MAX_TICKETS#timed_config.Until(
#     2,
#     _LIMITED_RELEASE_ENDS,
#     GENERAL_RELEASE_MAX_TICKETS
# )
CURRENT_TERM = 'TT'
EMAIL_FROM = 'oxfordsalsaball2020@gmail.com'
# EMAIL_FROM = 'noreply@oxfordsalsaball.co.uk'
SEND_EMAILS = True
LIMITED_RELEASE = timed_config.Until(
    False,
    _LIMITED_RELEASE_STARTS,
    True,
    _LIMITED_RELEASE_ENDS,
    False
)
TICKETS_ON_SALE = timed_config.Until(False, GENERAL_RELEASE_STARTS, True)
WAITING_OPEN = timed_config.Until(False, GENERAL_RELEASE_STARTS, True)
EMAILS_BATCH = 100 # Number of emails to send in one batch
STATISTICS_KEEP = datetime.timedelta(days=7)
HOST_COLLEGES = [
    'OUSS Member',
]#this is a list of affiliations

MAX_TICKET_CLAIMS = 2

# Features

REQUIRE_USER_PHOTO = False
REQUIRE_USER_DIETARY_REQS = False

ENABLE_POSTAGE = False

ENABLE_GROUP_PURCHASE = False
MAX_GROUP_MEMBERS = 4

ENABLE_CANCELLATION = False
ENABLE_RESALE = False
ENABLE_SEPARATE_POSTAGE = False
ENABLE_CHANGING_DETAILS = False
ENABLE_CHANGING_PHOTOS = False
ENABLE_RECLAIMING_TICKETS = True

PAYMENT_METHODS = [
    # 'Card',
    'PayPal',
    # 'Battels-MT',
    # 'Battels-MTHT',
    # 'Battels-HT',
]

FEATURE_CONSTANTS = [
    'REQUIRE_USER_PHOTO',
    'REQUIRE_USER_DIETARY_REQS',
    'ENABLE_POSTAGE',
    'PAYMENT_METHODS',
    'ENABLE_GROUP_PURCHASE',
    'MAX_GROUP_MEMBERS',
    'ENABLE_RESALE',
]

# Lockdown Mode - to be enabled close to the ball,
# when ticket information needs to be managed manually. Is a general case of
# many of the ENABLE_XYZ values above.
#
# Prevents:
# * Automated ticket cancellation/refunds
# * Resales
# * Users purchasing postage
# * Users changing personal details or photos

LOCKDOWN_STARTS = datetime.datetime(2022, 04, 28)
LOCKDOWN_MODE = timed_config.Until(False, LOCKDOWN_STARTS, True)

# Template config

TEMPLATE_CONFIG_KEYS = [
    'LOCKDOWN_STARTS',
    'CURRENT_TERM',
    'START_TIME',
    'GATES_CLOSE',
    'END_TIME',
    'COLLEGE',
    'BALL_NAME',
    'TITLE',
    'THEME',
    'DATE_FORMAT',
    'TREASURER_EMAIL_LINK',
    'TICKETS_EMAIL_LINK',
    'WEBSITE_EMAIL_LINK',
    'TREASURER_EMAIL',
    'TICKETS_EMAIL',
    'WEBSITE_EMAIL',
    'TICKET_TYPES',
    'NO_POSTAGE_OPTION',
    'POSTAGE_OPTIONS',
    'POSTAGE_OPTIONS_NEED_ADDRESS',
    'IMAGE_ACCEPT_STRING',
    'ENABLE_ANALYTICS',
    'ANALYTICS_ID',
    'ANALYTICS_DOMAIN',
    'EISITIRIO_URL',
    'EMAIL_SIGNOFF',
    'GENERAL_RELEASE_MAX_TICKETS',
    'TICKET_EXPIRY_TIME',
    'MAX_TICKET_CLAIMS',
    'ARTIST_PRICE',
    'STD_ALL_PRICE',
    'STD_ALL_EARLY_PRICE',
    'STD_PARTY_PRICE',
    'MEMBER_ALL_PRICE',
    'MEMBER_ALL_EARLY_PRICE',
    'MEMBER_PARTY',
    'GROUP_TICKET_PRICE',
    'GROUP_TICKET_PRICE2',
    'GROUP_SIZE',
    'GROUP_SIZE2',
    'GROUP_TICKET_PRICENUM',
    'GROUP_TICKET_PRICE2NUM'
    # 'GROUP_TICKET_PRICE_p'
]
TEMPLATE_CONFIG_KEYS.extend(FEATURE_CONSTANTS)

START_TIME = datetime.datetime(2022, 05, 13, 13,30) # 8pm, 11th May 2018
GATES_CLOSE = datetime.datetime(2022, 05, 13, 00,30) # 1am, 12th May 2018
END_TIME = datetime.datetime(2022, 05, 13, 01,30) # 1am, 12th May 2018
THEME = "Oxford's Salsa ball"

COLLEGE = "/".join(HOST_COLLEGES)
BALL_NAME = 'OUSS Salsa Ball'
# TITLE = '{0} {1}'.format(BALL_NAME, START_TIME.year)
TITLE = '{0}'.format(BALL_NAME)
DATE_FORMAT = '%d.%m.%Y'

EMAIL_SIGNOFF = 'The {0} Committee'.format(BALL_NAME)

# Location of installed system
# Should be set in environment specific config
EISITIRIO_URL = 'www.oxfordsalsaball.co.uk/'

TREASURER_EMAIL_LINK = (
    'mailto:treasurer@oxfordsalsaball.co.uk'
)
TICKETS_EMAIL_LINK = (
    'mailto:tickets@oxfordsalsaball.co.uk'
)
WEBSITE_EMAIL_LINK = (
    'mailto:webmaster@oxfordsalsaball.co.uk'
)

TREASURER_EMAIL = 'treasurer@oxfordsalsaball.co.uk'
TICKETS_EMAIL = 'tickets@oxfordsalsaball.co.uk'
WEBSITE_EMAIL = 'webmaster@oxfordsalsaball.co.uk'

GRAPH_STORAGE_FOLDER='static/admin/graphs'

# TICKETS:


# Full	25
# Full student	20
# Advance party	20
# Advance party student/member	16
# OTD party	22
# OTD party student/member	18


STD_ALL_PRICE = '25.00'
STD_ALL_EARLY_PRICE = '25.00'
STD_PARTY_PRICE = '25.00'


MEMBER_ALL_PRICE = '20.00'
MEMBER_ALL_EARLY_PRICE = '20.00'
MEMBER_PARTY = '20.00'


ARTIST_PRICE = 0
GROUP_TICKET_PRICE = '20.00'
GROUP_TICKET_PRICENUM = 2000
GROUP_TICKET_PRICE2 = '18.00'
GROUP_TICKET_PRICE2NUM = 1800
# GROUP_TICKET_PRICE_p = 1800
GROUP_SIZE=6
GROUP_SIZE2=10
