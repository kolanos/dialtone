from functools import wraps

from flask import g
from flask import Response
from flask import request


def check_auth(username, password):
    """
    This function is called to check if a username /password combination is
    valid.
    """
    return username == 'admin' and password == 'secret'


def authenticate():
    """Sends a 401 response that enables basic auth."""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            g.user = None
            return authenticate()
        g.user = auth.username
        return func(*args, **kwargs)
    return decorated_view
