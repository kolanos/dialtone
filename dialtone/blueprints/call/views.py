from flask import Blueprint
from flask import current_app
from flask import request
from flask import url_for

from dialtone.extensions import twilio

bp = Blueprint('call', __name__)


@bp.route('/twiml/call/fallback/', methods=['POST'])
@twilio.twiml_response
def call_fallback():
    response = twilio.response()
    msg = 'Sorry, your call could not be completed. Please try again later.'
    response.say(msg)
    response.hangup()
    return response


@bp.route('/twiml/call/', methods=['POST'])
@twilio.twiml_response
def call():
    response = twilio.response()
    origin = request.values.get('from')
    with response.dial(action=url_for('.call_status', _external=True)) as d:
        for phone in current_app.config.get('PHONES', []):
            d.number(
                phone,
                url=url_for('.call_confirm', _external=True, origin=origin))
    return response


@bp.route('/twiml/call/confirm/', methods=['GET', 'POST'])
@twilio.twiml_response
def call_confirm():
    response = twilio.response()
    origin = request.values.get('origin')
    digits = request.values.get('digits')
    if digits:
        return response
    msg = 'You have a call from {}, press # to accept.'
    response.say(msg.format(origin))
    with response.gather(finishOnKey='#') as g:
        g.say('Connecting you now...')
    response.hangup()
    return response


@bp.route('/twiml/call/status/', methods=['POST'])
@twilio.twiml_response
def call_status():
    response = twilio.response()
    status = request.values.get('DialCallStatus')
    if status in ['failed', 'busy', 'no-answer', 'canceled']:
        msg = ('The person you are trying to call is currently busy. '
               'Please record a message after the beep.')
        response.say(msg)
        response.record(action=url_for('.call_record', _external=True))
    return response


@bp.route('/twiml/call/record/', methods=['POST'])
@twilio.twiml_response
def call_record():
    response = twilio.response()
    response.say('Thank you. Your message has been recorded. Goodbye')
    response.hangup()
    return response


@bp.route('/twiml/dial/', methods=['POST'])
@twilio.twiml_response
def dial():
    response = twilio.response()
    digits = request.values.get('digits')
    response.dial(
        digits,
        callerId=current_app.config.get('OUTGOING_NUMBER'),
        action=url_for('.dial_status', _external=True))
    return response


@bp.route('/twiml/dial/status/', methods=['POST'])
@twilio.twiml_response
def dial_status():
    response = twilio.response()
    status = request.values.get('DialCallStatus')
    if status in ['failed', 'busy', 'no-answer', 'canceled']:
        msg = ('Sorry, your call could not be completed. '
               'Please try again later.')
        response.say(msg)
    response.hangup()
    return response
