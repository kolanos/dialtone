from flask import Blueprint

dashboard = Blueprint('api', __name__)

@dashboard.route('/')
def root():
    pass


@dashboard.route('/calls')
def calls():
    pass


@dashboard.route('/sms/', method=['GET', 'POST'])
def sms():
    pass


@dashboard.route('/recordings/'), methods=['GET'])
def recordings():
    pass


@dashboard.route('/team/')
def team():
    pass
