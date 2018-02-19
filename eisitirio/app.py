# coding: utf-8
"""Create the application object for the ticketing system."""

from __future__ import unicode_literals

import flask

APP = flask.Flask('eisitirio', static_folder=None)

APP.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)

APP.jinja_env.trim_blocks = True
APP.jinja_env.lstrip_blocks = True


from flask_sqlalchemy import SQLAlchemy
iaas_uri = '{}://{}:{}@{}/{}' \
        .format('mysql+pymysql',
                'root',
                'GTG24DDa',
                'localhost',
                'eisitirio')

APP.config['SQLALCHEMY_DATABASE_URI'] =iaas_uri
APP.config['DATABASE_URL'] =iaas_uri

SQLALCHEMY_BINDS={'eisitirio':iaas_uri}
APP.config['SQLALCHEMY_BINDS'] =SQLALCHEMY_BINDS
eisitiriodb = SQLAlchemy(APP)
# db = eisitiriodb

# db.create_all()


