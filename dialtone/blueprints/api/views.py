from flask import Blueprint
from flask import jsonify

from dialtone.extensions import twilio
from dialtone.utils import todict

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/')
def root():
    account = twilio.accounts.get(twilio.sid)
    return jsonify(status=account.status)


@bp.route('/calls/')
def calls():
    calls = [todict(call) for call in twilio.calls.list()]
    [call.pop('auth') for call in calls]
    return jsonify(items=calls)


@bp.route('/calls/<sid>/')
def call(sid):
    call = todict(twilio.calls.get(id))
    call.pop('auth')
    return jsonify(call)


@bp.route('/messages/')
def messages():
    messages = [todict(message) for message in twilio.messages.list()]
    [message.pop('auth') for message in messages]
    return jsonify(items=messages)


@bp.route('/messages/<sid>/')
def message(sid):
    message = todict(twilio.messages.get(sid))
    message.pop('auth')
    return jsonify(message)


@bp.route('/recordings/')
def recordings():
    recordings = [todict(recording) for recording in twilio.recordings.list()]
    [recording.pop('auth') for recording in recordings]
    return jsonify(items=recordings)


@bp.route('/recordings/<sid>/')
def recording(sid):
    recording = todict(twilio.recordings.get(sid))
    recording.pop('auth')
    return jsonify(recording)
