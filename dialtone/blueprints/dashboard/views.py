from flask import Blueprint
from flask import Response
from flask import current_app
from flask import g
from flask import render_template
from flask import request

from dialtone.extensions import twilio

bp = Blueprint('dashboard', __name__, template_folder='templates')


@bp.context_processor
def inject_capability_token():
    return dict(capability_token=twilio.capability_token(g.user))


@bp.route('/')
def root():
    account = twilio.accounts.get(twilio.sid)
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


@bp.route('/setup/', methods=['GET'])
def setup():
    result = twilio.setup(current_app)
    return Response('<p>{}</p>'.format('</p><p>'.join(result)))
