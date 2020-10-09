from models.modules.core import app, jsonify, InvalidUsage, Response, lru_cache
from controllers.users import Users, Auths
from models.modules.jwt import *

@app.route('/remove/<authid>', methods=['DELETE'])
@validate_token
def removeuser(authid):
    try:
        return Auths.delete_account(authid)
    except Exception as e:
        raise InvalidUsage(str(e), status_code=500)

@app.route('/login', methods=['POST'])
def login():
    try:
        return Auths.login()
    except Exception as e:
        raise InvalidUsage(str(e), status_code=500)

@app.route('/register', methods=['POST'])
def register():
    try:
        return Auths.register()
    except Exception as e:
        raise InvalidUsage(str(e), status_code=500)

@app.route('/confirm-email/<token>', methods=['GET'])
def confirm(token):
    try:
        return Auths.confirms(token)
    except Exception as e:
        raise InvalidUsage(str(e), status_code=500)

@app.route('/users', methods=['GET'])
@validate_token
@lru_cache(maxsize=512)
def getallusers():
    try:
        return Users.get_all_users()
    except Exception as e:
        raise InvalidUsage(str(e), status_code=500)

@app.route('/users/access/<value>', methods=['GET'])
@validate_token
@lru_cache(maxsize=512)
def getuserby(value):
    try:
        return Users.get_user_by(value)
    except Exception as e:
        raise InvalidUsage(str(e), status_code=500)

@app.route('/users/<authid>', methods=['GET'])
@validate_token
def getuserinfo(authid):
    try:
        return Users.get_user_info(authid)
    except Exception as e:
        raise InvalidUsage(str(e), status_code=500)

@app.route('/users/<authid>', methods=['PUT'])
@validate_token
def updateuserinfo(authid):
    try:
        return Users.update_userinfo(authid)
    except Exception as e:
        raise InvalidUsage(str(e), status_code=500)

@app.route('/users', methods=['POST'])
@validate_token
def saveuserinfo():
    try:
        return Users.add_userinfo()
    except Exception as e:
        raise InvalidUsage(str(e), status_code=500)
