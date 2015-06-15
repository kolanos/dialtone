from __future__ import absolute_import

from functools import wraps

from flask import Response
from flask import abort
from flask import request
from twilio.rest import TwilioRestClient
from twilio import twiml
from twilio.util import RequestValidator


class Twilio(object):
    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        self.account_sid = self.app.config.get('TWILIO_ACCOUNT_SID')
        self.auth_token = self.app.config.get('TWILIO_AUTH_TOKEN')
        self.client = TwilioRestClient(self.account_sid, self.auth_token)
        self.validator = RequestValidator(self.auth_token)

    def __getattr__(self, name):
        if hasattr(self.client, name):
            return getattr(self.client, name)
        return super(Twilio, self).__getattr__(name)

    @property
    def response(self):
        return twiml.Response

    @property
    def twiml(self):
        return twiml

    def validate_request(self, func):
        """Decorator to validate that the request is coming from Twilio."""
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if self.app.TESTING:
                return func(*args, **kwargs)
            url = request.base_url
            vars = request.values
            signature = request.header.get('X-Twilio-Signature')
            if not self.validator.validate(url, vars, signature):
                return abort(403)
            return func(*args, **kwargs)
        return decorated_view

    def twiml_response(self, func):
        """Decorator that sets view headers for TwiML responses."""
        @wraps(func)
        def decorated_view(*args, **kwargs):
            response = func(*args, **kwargs)
            return Response(response, content_type='text/xml; charset=utf-8')
        return decorated_view
