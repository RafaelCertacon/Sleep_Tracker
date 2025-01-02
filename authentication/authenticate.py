from functools import wraps
from app import *

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return {'message': 'Token ausente!'}, 401
        try:
            jwt.decode(token, app.config['SECRET_KEY'], algorithms=["RS256"])
        except:
            return {'message': 'Token inválido!'}, 401
        return f(*args, **kwargs)
    return decorated
