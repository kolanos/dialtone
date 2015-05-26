from __future__ import absolute_import

from twilio.rest import TwilioRestClient


class Twilio(object):
    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.account_sid = app.config.get('TWILIO_ACCOUNT_SID')
        self.auth_token = app.config.get('TWILIO_AUTH_TOKEN')
        self.client = TwilioRestClient(self.account_sid, self.auth_token)

    def __getattr__(self, name):
        if hasattr(self.client, name):
            return getattr(self.client, name)
        return super(Twilio, self).__getattr__(name)
