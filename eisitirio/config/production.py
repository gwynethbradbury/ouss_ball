# coding: utf-8
"""Configuration overrides for production environment."""

from __future__ import unicode_literals

import logging
import base64

DEBUG = False
TESTING = False
SQLALCHEMY_ECHO = False
# SQLALCHEMY_DATABASE_URI = (
#     'mysql://user:password@host/database'
# )
ENVIRONMENT = 'PRODUCTION'
SEND_EMAILS = True
LOG_LEVEL = logging.WARNING

EWAY_API_BASE = 'https://api.ewaypayments.com/'
EWAY_API_KEY = 'eWay API Key'
EWAY_PASSWORD = 'eWay Password'
EWAY_API_PASSCODE = base64.b64encode(
    '{0}:{1}'.format(
        EWAY_API_KEY,
        EWAY_PASSWORD
    )
)

import os
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465
SMTP_SSL = True
SMTP_STARTTLS = False
SMTP_LOGIN = True
SMTP_USER = 'oxfordsalsaball2020@gmail.com'

import os
from dotenv import load_dotenv
project_folder = os.path.expanduser('~/ouss_ball')  # adjust as appropriate
load_dotenv(os.path.join(project_folder, '.env'))
SMTP_PASSWORD = os.getenv("SECRET_KEY")
#SMTP_PASSWORD = 'ecdrgvozwxmtqkbv'

AWS_ACCESS_KEY_ID = 'AWS Access Key ID'
AWS_SECRET_ACCESS_KEY = 'AWS Secret Access Key'
S3_BUCKET = 'prod-photos-kebleball'

TEMP_UPLOAD_FOLDER = '/tmp/eisitirio_prod_uploads'

ENABLE_ANALYTICS = True
ANALYTICS_ID = 'Google Analytics Code'
ANALYTICS_DOMAIN = 'auto'

MAINTENANCE_FILE_PATH = '/var/www/eisitirio/production/.maintenance'

EISITIRIO_URL = 'https://www.oxfordsalsaball.co.uk/'
