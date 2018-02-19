# coding: utf-8
"""Default/global configuration for the application."""

from __future__ import unicode_literals

import datetime
import logging

from eisitirio.helpers import timed_config

# App Config

SECRET_KEY = (
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
GENERAL_RELEASE_STARTS = datetime.datetime(2016, 01, 30, 10, 0, 0)

GUEST_TICKETS_AVAILABLE = timed_config.Until(
    1550,
    datetime.datetime(2016, 04, 14, 19, 30, 0),
    1666
)
TICKET_EXPIRY_TIME = datetime.timedelta(days=1)
MAX_TICKETS_PER_TRANSACTION = 4
MAX_TICKETS_WAITING = 4
GENERAL_RELEASE_MAX_TICKETS = 4
MAX_TICKETS = timed_config.Until(
    2,
    _LIMITED_RELEASE_ENDS,
    GENERAL_RELEASE_MAX_TICKETS
)
CURRENT_TERM = 'TT'
EMAIL_FROM = 'noreply@kebleball.com'
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
    'Keble',
]

MAX_TICKET_CLAIMS = 2

# Features

REQUIRE_USER_PHOTO = True

ENABLE_POSTAGE = True

ENABLE_GROUP_PURCHASE = True
MAX_GROUP_MEMBERS = 4

ENABLE_CANCELLATION = True
ENABLE_RESALE = False
ENABLE_SEPARATE_POSTAGE = True
ENABLE_CHANGING_DETAILS = False
ENABLE_CHANGING_PHOTOS = False
ENABLE_RECLAIMING_TICKETS = True

PAYMENT_METHODS = [
    'Card',
    'Battels-MT',
    'Battels-MTHT',
    'Battels-HT',
]

FEATURE_CONSTANTS = [
    'REQUIRE_USER_PHOTO',
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

LOCKDOWN_STARTS = datetime.datetime(2016, 04, 23)
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
]
TEMPLATE_CONFIG_KEYS.extend(FEATURE_CONSTANTS)

START_TIME = datetime.datetime(2016, 5, 7, 20) # 8pm, 7th May 2016
GATES_CLOSE = datetime.datetime(2016, 5, 7, 23) # 11pm, 7th May 2016
END_TIME = datetime.datetime(2016, 5, 8, 4) # 4am, 8th May 2016
THEME = 'Panopticon'

COLLEGE = "/".join(HOST_COLLEGES)
BALL_NAME = 'Keble Ball'
TITLE = '{0} {1}'.format(BALL_NAME, START_TIME.year)
THEME = 'Panopticon'
DATE_FORMAT = '%d%m%Y'

EMAIL_SIGNOFF = 'The {0} Committee'.format(BALL_NAME)

# Location of installed system
# Should be set in environment specific config
EISITIRIO_URL = ''

TREASURER_EMAIL_LINK = (
    'http://www.google.com/recaptcha/mailhide/d?k='
    '01sJMU6xpqAr0zE0F_G0V-QQ==&c=GfM4SPA4UnE8hXdp0WlLsjlXnqI2V5U-U8lhp9CgS3E='
)
TICKETS_EMAIL_LINK = (
    'http://www.google.com/recaptcha/mailhide/d?k='
    '01sJMU6xpqAr0zE0F_G0V-QQ==&c=rbxZ3WcBT6IGaGvfDZTkxG7CR0UVVGm0Uc353dDfBx0='
)
WEBSITE_EMAIL_LINK = (
    'http://www.google.com/recaptcha/mailhide/d?k='
    '01VW2HusQat4KpnmQYJBSfhQ==&c=0pBadqH9ae41gTIaahTM78kkmPpv_-wELjktV6Zs-d0='
)

TREASURER_EMAIL = 'treasurer@kebleball.com'
TICKETS_EMAIL = 'tickets@kebleball.com'
WEBSITE_EMAIL = 'website@kebleball.com'
