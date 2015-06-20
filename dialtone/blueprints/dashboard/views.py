from flask import Blueprint

dashboard = Blueprint('dashboard', __name__)



@dashboard.route('/')
def root():
    return 'hello'


@dashboard.route('/calls')
def calls():
    pass


@dashboard.route('/sms/', methods=['GET', 'POST'])
def sms():
    pass


@dashboard.route('/recordings/', methods=['GET'])
def recordings():
    pass


@dashboard.route('/team/')
def team():
    pass
