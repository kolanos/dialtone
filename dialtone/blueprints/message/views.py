from flask import Blueprint

bp = Blueprint('sms', __name__)


@bp.route('/twiml/message/fallback/', methods=['POST'])
def message_fallback():
    pass


@bp.route('/twiml/message/', methods=['POST'])
def message():
    pass
