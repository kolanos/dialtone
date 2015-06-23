from __future__ import absolute_import

from functools import partial
from functools import wraps

from flask import Response as HttpResponse
from flask import abort
from flask import current_app
from flask import request
from flask import url_for
from twilio import twiml
from twilio.rest import TwilioRestClient
from twilio.util import RequestValidator


class Twilio(object):
    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.sid = app.config.get('TWILIO_SID')
        self.token = app.config.get('TWILIO_TOKEN')
        self.client = TwilioRestClient(account=self.sid, token=self.token)
        self.validator = RequestValidator(self.token)

    def __getattr__(self, name):
        if hasattr(self, 'client') and hasattr(self.client, name):
            return getattr(self.client, name)
        raise AttributeError('%r has no attribute %r' % (
            self.__class__, name))

    @property
    def response(self):
        return Response

    @property
    def action(self):
        return partial(url_for, _external=True, _scheme='https')

    def validate_request(self, func):
        """Decorator to validate that the request is coming from Twilio."""
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if current_app.TESTING:
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
            return HttpResponse(
                response,
                content_type='text/xml; charset=utf-8')
        return decorated_view


class Response(twiml.Response):
    def say(self, text, **kwargs):
        """Overload the say method to set the voice and language."""
        kwargs['voice'] = current_app.config.get('VOICE', 'alice')
        kwargs['language'] = current_app.config.get('LANGUAGE', 'en-US')
        return super(Response, self).say(text, **kwargs)

    def dial(self, number=None, **kwargs):
        """Overload the dial method to set the timeout."""
        kwargs['timeout'] = current_app.config.get('DIAL_TIMEOUT', 60)
        return super(Response, self).dial(number, **kwargs)
