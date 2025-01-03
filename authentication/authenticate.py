from functools import wraps
from flask import request, current_app
import jwt

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return {'message': 'Token ausente!'}, 401
        try:
            token = token.split(" ")[1]
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return {'message': 'Token expirado!'}, 401
        except jwt.InvalidTokenError:
            return {'message': 'Token inválido!'}, 401
        return f(*args, **kwargs)

    return decorated
