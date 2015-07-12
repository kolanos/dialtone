from flask import Blueprint

bp = Blueprint('message', __name__)


@bp.route('/twiml/message/', methods=['POST'])
def message():
    pass


@bp.route('/twiml/message/fallback/', methods=['POST'])
def message_fallback():
    pass



