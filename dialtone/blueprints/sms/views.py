from flask import Blueprint

sms = Blueprint('sms', __name__)


@sms.route('/twiml/sms/fallback/', method=['POST'])
def sms_fallback():
    pass


@sms.route('/twiml/sms/', method=['POST'])
def sms():
    pass
