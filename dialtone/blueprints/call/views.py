from flask import Blueprint

from dialtone.extensions import twilio

call = Blueprint('call', __name__)


@call.route('/twiml/call/fallback/', methods=['POST'])
@twilio.twiml_response
def call_fallback():
    pass


@call.route('/twiml/call/', methods=['POST'])
@twilio.twiml_response
def call():
    pass


@call.route('/twiml/call/confirm/', methods=['POST'])
@twilio.twiml_response
def call_confirm():
    pass


@call.route('/twiml/call/status/', methods=['POST'])
@twilio.twiml_response
def call_status():
    pass


@call.route('/twiml/call/record/', methods=['POST'])
@twilio.twiml_response
def call_record():
    pass


@call.route('/twiml/dial/', methods=['POST'])
@twilio.twiml_response
def dial():
    pass


@call.route('/twiml/dial/status/', methods=['POST'])
@twilio.twiml_response
def dial_status():
    pass
