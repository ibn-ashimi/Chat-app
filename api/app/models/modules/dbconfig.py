from models.modules.core import os, SQLAlchemy, Marshmallow, app, logger

baseDir = os.path.abspath(os.path.dirname(__file__))
DB_USERNAME = app.config['MYSQL_USERNAME']
DB_PASSWORD = app.config['MYSQL_PASSWORD']
DB_NAME = app.config['MYSQL_DB']
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@localhost:3306/{}'.format(DB_USERNAME, DB_PASSWORD, DB_NAME)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(baseDir, 'db.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)
logger.debug("database connection started")
import hashlib
import binascii
import os

def hash_password(password):
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

def verify_password(stored_password, provided_password):
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'), salt.encode('ascii'), 100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password
