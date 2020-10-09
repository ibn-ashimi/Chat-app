from models.modules.dbconfig import db, ma, hash_password, verify_password
from sqlalchemy import exc

class Auth(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    uid = db.Column(db.Integer, unique = True)
    password = db.Column(db.String(200))
    isVerified = db.Column(db.Integer)
    email = db.Column(db.String(100))
    userInfo = db.relationship('User', backref="auth", uselist=False)

    def __init__(self, uid, password, email, isVerified):
        self.uid = uid
        self.password = password
        self.email = email
        self.isVerified = isVerified

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    auth_id = db.Column(db.Integer, db.ForeignKey('auth.id'), unique = True)
    username = db.Column(db.String(50))
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    sex = db.Column(db.String(7))
    access = db.Column(db.String(7))
    address = db.Column(db.String(200))
    city = db.Column(db.String(20))
    country = db.Column(db.String(20))
    image = db.Column(db.String(500))
    date_added = db.Column(db.String(50))

    def __init__(self, username, firstname, lastname, email, sex, access, phone, address, city, country, auth_id, image, date_added):
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.sex = sex
        self.access = access
        self.phone = phone
        self.address = address
        self.city = city
        self.country = country
        self.auth_id = auth_id
        self.date_added = date_added

class AuthSchema(ma.Schema):
    class Meta:
        fields = ('uid', 'email', 'isVerified')

class UserSchema(ma.Schema):
    class Meta:
        fields = ('username', 'firstname', 'lastname', 'email', 'sex', 'access', 'phone', 'address', 'city', 'country', 'auth_id', 'image', 'date_added', 'user')

auth_scheme = AuthSchema()
auths_scheme = AuthSchema(many = True)

user_scheme = UserSchema()
users_scheme = UserSchema(many = True)

db.create_all()