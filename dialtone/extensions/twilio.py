from __future__ import absolute_import

from functools import wraps

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
        self.app = app
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
            if isinstance(response, twiml.Response):
                response = response.toxml()
            return Response(response, content_type='text/xml; charset=utf-8')
        return decorated_view

    def dictify(self, obj, classkey=None):
        if isinstance(obj, dict):
            data = {}
            for (k, v) in obj.items():
                data[k] = self.dictify(v, classkey)
            return data
        elif hasattr(obj, "_ast"):
            return self.dictify(obj._ast())
        elif hasattr(obj, "__iter__"):
            return [self.dictify(v, classkey) for v in obj]
        elif hasattr(obj, "__dict__"):
            data = dict([(key, self.dictify(value, classkey))
                for key, value in obj.__dict__.iteritems() 
                if not callable(value) and not key.startswith('_')])
            if classkey is not None and hasattr(obj, "__class__"):
                data[classkey] = obj.__class__.__name__
            return data
        else:
            return obj
