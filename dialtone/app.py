from flask import Flask

from dialtone.extensions import db
from dialtone.extensions import twilio


def create_app(name=__name__):
    app = Flask(name)

    app.config.from_object('dialtone.config')
    app.config.from_envvar('DIALTONE_SETTINGS')
    db.init_app(app)
    twilio.init_app(app)
    return app
