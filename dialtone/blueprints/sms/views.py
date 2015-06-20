from flask import Blueprint

sms = Blueprint('sms', __name__)


@sms.route('/twiml/sms/fallback/', methods=['POST'])
def twiml_sms_fallback():
    pass


@sms.route('/twiml/sms/', methods=['POST'])
def twiml_sms():
    pass
