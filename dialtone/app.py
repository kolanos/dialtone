from flask import Flask

from dialtone.blueprints.api import api
from dialtone.blueprints.call import call
from dialtone.blueprints.dashboard import dashboard
from dialtone.blueprints.message import message
from dialtone.extensions import twilio
from dialtone.filters import relative_date


def create_app(name=__name__):
    app = Flask(name)
    app.config.from_object('dialtone.config')
    twilio.init_app(app)
    app.jinja_env.filters['relativeDate'] = relative_date
    app.register_blueprint(api)
    app.register_blueprint(call)
    app.register_blueprint(dashboard)
    app.register_blueprint(message)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
