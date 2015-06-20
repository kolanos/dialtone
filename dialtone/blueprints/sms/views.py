from flask import Blueprint

bp = Blueprint('sms', __name__)


@bp.route('/twiml/sms/fallback/', methods=['POST'])
def sms_fallback():
    pass


@bp.route('/twiml/sms/', methods=['POST'])
def sms():
    pass
