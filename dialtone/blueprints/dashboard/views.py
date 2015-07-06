from flask import Blueprint
from flask import render_template
from flask import request

from dialtone.extensions import twilio

bp = Blueprint('dashboard', __name__, template_folder='templates')


@bp.route('/')
def root():
    account = twilio.accounts.get()
    return render_template('status.html', account=account)


@bp.route('/calls')
def calls():
    calls = twilio.calls.list(**request.args)
    return render_template('calls.html', calls=calls)


@bp.route('/messages/', methods=['GET', 'POST'])
def messages():
    messages = twilio.messages.list(**request.args)
    return render_template('messages.html', messages=messages)


@bp.route('/recordings/', methods=['GET'])
def recordings():
    recordings = twilio.recordings.list(**request.args)
    return render_template('recordings.html', recordings=recordings)
