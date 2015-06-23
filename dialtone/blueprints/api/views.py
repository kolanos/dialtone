from flask import Blueprint
from flask import jsonify

from dialtone.extensions import twilio
from dialtone.utils.twiml import scrub
from dialtone.utils.twiml import to_dict

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/')
def root():
    account = twilio.accounts.get(twilio.sid)
    return jsonify(status=account.status)


@bp.route('/calls/')
def calls():
    calls = [to_dict(call) for call in twilio.calls.list()]
    scrub(calls, 'auth')
    return jsonify(items=calls)


@bp.route('/calls/<sid>/')
def call(sid):
    call = to_dict(twilio.calls.get(id))
    scrub(call, 'auth')
    return jsonify(call)


@bp.route('/messages/')
def messages():
    messages = [to_dict(message) for message in twilio.messages.list()]
    scrub(messages, 'auth')
    return jsonify(items=messages)


@bp.route('/messages/<sid>/')
def message(sid):
    message = to_dict(twilio.messages.get(sid))
    scrub(message, 'auth')
    return jsonify(message)


@bp.route('/recordings/')
def recordings():
    recordings = [to_dict(recording) for recording in twilio.recordings.list()]
    scrub(recordings, 'auth')
    return jsonify(items=recordings)


@bp.route('/recordings/<sid>/')
def recording(sid):
    recording = to_dict(twilio.recordings.get(sid))
    scrub(recording, 'auth')
    return jsonify(recording)
