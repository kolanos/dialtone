from flask import Blueprint

from dialtone.extensions import twilio

bp = Blueprint('call', __name__)


@bp.route('/twiml/call/fallback/', methods=['POST'])
@twilio.twiml_response
def call_fallback():
    response = twilio.response()
    response.say('Sorry, an error occured.')
    return response


@bp.route('/twiml/call/', methods=['POST'])
@twilio.twiml_response
def call():
    response = twilio.response()
    response.say('oh, hi mark')
    return response
    pass


@bp.route('/twiml/call/confirm/', methods=['POST'])
@twilio.twiml_response
def call_confirm():
    pass


@bp.route('/twiml/call/status/', methods=['POST'])
@twilio.twiml_response
def call_status():
    pass


@bp.route('/twiml/call/record/', methods=['POST'])
@twilio.twiml_response
def call_record():
    pass


@bp.route('/twiml/dial/', methods=['POST'])
@twilio.twiml_response
def dial():
    pass


@bp.route('/twiml/dial/status/', methods=['POST'])
@twilio.twiml_response
def dial_status():
    pass
