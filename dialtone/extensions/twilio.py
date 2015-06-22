from __future__ import absolute_import

from functools import wraps

from flask import current_app
from flask import Response
from flask import abort
from flask import request
from twilio import twiml
from twilio.rest import TwilioRestClient
from twilio.util import RequestValidator


class Twilio(object):
    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.sid = self.app.config.get('TWILIO_SID')
        self.token = self.app.config.get('TWILIO_TOKEN')
        self.client = TwilioRestClient(account=self.sid, token=self.token)
        self.validator = RequestValidator(self.token)

    def __getattr__(self, name):
        if hasattr(self.client, name):
            return getattr(self.client, name)
        return super(Twilio, self).__getattr__(name)

    @property
    def response(self):
        return TwiMLResponse

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
            if isinstance(response, twiml.Response):
                response = response.toxml()
            return Response(response, content_type='text/xml; charset=utf-8')
        return decorated_view


class TwiMLResponse(twiml.Response):
    def say(self, text, **kwargs):
        """Overload the say method to set the voice and language."""
        kwargs['voice'] = current_app.config.get('VOICE', 'alice')
        kwargs['language'] = current_app.config.get('LANGUAGE', 'en-US')
        super(TwiMLResponse, self).say(text, **kwargs)

    def dial(self, number=None, **kwargs):
        """Overload the dial method to set the timeout."""
        kwargs['timeout'] = current_app.config.get('DIAL_TIMEOUT', 60)
        super(TwiMLResponse, self).dial(number, **kwargs)
