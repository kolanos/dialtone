from flask import Blueprint
from flask import jsonify

from dialtone.extensions import twilio

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/')
def root():
    account = twilio.accounts.get(twilio.sid)
    info = {
        'status': account.status}
    return jsonify(info)


@bp.route('/calls/')
def calls():
    return jsonify(twilio.calls.list())


@bp.route('/calls/<id>/')
def call(id):
    return jsonify(twilio.calls.get(id))


@bp.route('/sms/')
def sms():
    return jsonify(twilio.messages.list())


@bp.route('/recordings/')
def recordings():
    return jsonify(twilio.recordings.list())
