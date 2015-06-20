from flask import Blueprint

from dialtone.extensions import twilio

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/')
def root():
    return twilio.accounts.get(twilio.sid)


@api.route('/calls/')
def calls():
    return twilio.calls.list()


@api.route('/calls/<id>/')
def call(id):
    return twilio.calls.get(id)


@api.route('/sms/')
def sms():
    return twilio.messages.list()


@api.route('/recordings/')
def recordings():
    return twilio.recordings.list()
