from flask import Blueprint

bp = Blueprint('dashboard', __name__)


@bp.route('/')
def root():
    return 'hello'


@bp.route('/calls')
def calls():
    pass


@bp.route('/sms/', methods=['GET', 'POST'])
def sms():
    pass


@bp.route('/recordings/', methods=['GET'])
def recordings():
    pass


@bp.route('/team/')
def team():
    pass
