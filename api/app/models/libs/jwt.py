from models.modules.core import make_response, request, app, jsonify, InvalidUsage
import jwt
import datetime
from functools import wraps

userInfo = {}

def validate_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('Authorization')
        if not auth:
            return make_response({
                "error": "authorization required. access forbidden"
            }, 403)
        
        token = auth.split(' ')[1]
        
        if not token:
            return make_response({
                "error": "bad request. missing token"
            }, 400)

        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except Exception as e:
            return make_response({
                "error": "Token is invalid " + str(e)
            }, 500)
        
        return f(*args, **kwargs)
    return decorated

def generatejwt(data): 
        token = jwt.encode({
            'user': data,
            'exp': datetime.datetime.now() + datetime.timedelta(minutes=15000)
        }, app.config['SECRET_KEY'])
        return token.decode('UTF-8')
        