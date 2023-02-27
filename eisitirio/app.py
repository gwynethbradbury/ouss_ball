# coding: utf-8
"""Create the application object for the ticketing system."""

from __future__ import unicode_literals

import flask
from flask_sslify import SSLify


APP = flask.Flask('eisitirio', static_folder=None)

sslify = SSLify(APP)

APP.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)

APP.jinja_env.trim_blocks = True
APP.jinja_env.lstrip_blocks = True

import dbconfig

from flask_sqlalchemy import SQLAlchemy
iaas_uri = '{}://{}:{}@{}/{}' \
        .format('mysql+pymysql',
                dbconfig.dbuser,
                dbconfig.dbpwd,
                dbconfig.dbhost,
                dbconfig.dbname)

APP.config['SQLALCHEMY_DATABASE_URI'] =iaas_uri
APP.config['DATABASE_URL'] =iaas_uri

SQLALCHEMY_BINDS={'eisitirio':iaas_uri}
APP.config['SQLALCHEMY_BINDS'] =SQLALCHEMY_BINDS
import os
print(os.path)

APP.config.from_pyfile('config/default.py')
APP.config.from_pyfile('config/ticket_types.py')
APP.config.from_pyfile('config/postage.py')
APP.config.from_pyfile('config/payment.py')
APP.config.from_pyfile('config/production.py')

# import flask_misaka as misaka
#
# from eisitirio.helpers import log_manager
# from eisitirio.helpers import login_manager
# from eisitirio.helpers import email_manager
# from eisitirio.helpers import sms_manager
#
# log_manager.LogManager(APP)
# email_manager.EmailManager(APP)
# login_manager.LOGIN_MANAGER.init_app(APP)
# misaka.Misaka(APP)
# # markdown.Markdown(APP)
#
# APP.sms_manager = sms_manager.SmsManager()
#
# LOG = APP.log_manager.log_main


eisitiriodb = SQLAlchemy(APP)
# db = eisitiriodb

# db.create_all()
