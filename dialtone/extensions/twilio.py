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
from twilio.util import TwilioCapability


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

    def setup(self, app):
        result = []
        name = 'dialtone-debug' if app.config['DEBUG'] else 'dialtone'
        application = self.applications.list(friendly_name=name)
        if not application:
            application = self.applications.create(friendly_name=name)
            result.append(
                'Application {} ({}) created'.format(
                    name, application.sid))
        else:
            application = application[0]
            result.append(
                'Application {} ({}) updated'.format(
                    name, application.sid))
        application.update(
            voice_url=self.action('call.call'),
            voice_method='POST',
            voice_fallback_url=self.action('call.call_fallback'),
            voice_fallback_method='POST',
            status_callback=self.action('call.call_status'),
            status_callback_method='POST',
            voice_caller_id_lookup=False,
            sms_url=self.action('message.message'),
            sms_method='POST',
            sms_fallback_url=self.action('message.message_fallback'),
            sms_fallback_method='POST',
            sms_status_callback=self.action('message.message_status'))
        self.app_sid = application.sid
        if not app.config['DEBUG']:
            outgoing_number = app.config['OUTGOING_NUMBER']
            incoming_phone = self.phone_numbers.list(
                phone_number=outgoing_number)
            if not incoming_phone:
                raise Exception(
                    'Phone number {} could not be found on this Twilio '
                    'account.'.format(outgoing_number))
            else:
                incoming_phone = incoming_phone[0]
            incoming_phone.update(
                voice_application_sid=self.app_sid,
                sms_application_sid=self.app_sid)
            result.append('Phone Number {} ({}) updated'.format(
                incoming_phone.phone_number, incoming_phone.sid))
        return result

    @property
    def response(self):
        return Response

    @property
    def action(self):
        return partial(url_for, _external=True, _scheme='https')

    def capability_token(self, user):
        capability = TwilioCapability(self.sid, self.token)
        capability.allow_client_outgoing(self.app_sid)
        capability.allow_client_incoming(user)
        return capability.generate()

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
