from flask import Flask

from dialtone.blueprints.api import api
from dialtone.blueprints.call import call
from dialtone.blueprints.dashboard import dashboard
from dialtone.blueprints.sms import sms
from dialtone.extensions import twilio


def create_app(name=__name__):
    app = Flask(name)
    app.config.from_object('dialtone.config')
    twilio.init_app(app)
    app.register_blueprint(api)
    app.register_blueprint(call)
    app.register_blueprint(dashboard)
    app.register_blueprint(sms)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
