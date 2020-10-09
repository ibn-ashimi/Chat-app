from models.modules.core import logger, request, InvalidUsage, make_response, app, url_for
from models.libs.filemanager import upload_image
from models.dbmodels.user_model import *
from models.modules.jwt import *
from models.modules.mailconfig import *
from datetime import datetime
import os

class Auths():
    def confirms(token):
        try:
            resp = confirm_email_token(token)
            if resp == False:
                return make_response({
                    "error": "confirmation link expired or invalid"
                }, 400)
            
            userinfo = Auth.query.filter_by(email = resp).first()
            email = userinfo.email
            userinfo.isVerified = 1
            db.session.commit()
            db.session.close()

            welcome_msg = 'Welcome to our platform user {}'.format(email)
            send_email(
                "Welcome email", [email], welcome_msg
            )
            return make_response({
                "message": "validation complete",
            }, 200)
        except exc.SQLAlchemyError as e:
            raise Exception(e._message)
        except Exception as e:
            raise Exception(str(e))

    def login():
        email = request.json['email']
        password = request.json['password']
        user = Auth.query.filter_by(email = email).first()
        if not user:
            return make_response({
                "error": "user email is invaild"
            }, 404)

        if user.isVerified == 0:
            return make_response({
                "error": "your account is not validated"
            }, 401)

        check = verify_password(user.password, password)
        if check == False:
            return make_response({
                "error": "password is incorrect"
            }, 401)
        del user.password
        del user.id

        token = generatejwt({
            "email": email,
            "isVerified": user.isVerified,
            "uid": user.uid
        })
        return jsonify({
            "jwt": token
        })

    def delete_account(uid):
        # email = request.json['email']
        try:
            user = Auth.query.filter_by(uid = uid).first()
            obj = User.query.filter_by(auth_id = uid).first()
            delivery = Delivery.query.filter_by(auth_id = uid).first()
            if not user or not obj:
                return make_response({
                    "error": "user account info not found"
                }, 400)
            db.session.delete(user)
            db.session.delete(delivery)
            db.session.delete(obj)
            db.session.commit()
            db.session.close()
            return make_response({
                "message": "user deleted successfully",
            }, 200)
        except exc.SQLAlchemyError as e:
            raise Exception(e._message)
        except Exception as e:
            raise Exception(str(e))

    def register():
        email = request.json['email']
        password = request.json['password']
        access = request.json['access'] or 'customer'

        try:
            user = Auth.query.filter_by(email = email).first()
            if user:
                return make_response({
                    "error": "email in use by another account"
                }, 400)

            uid = int(datetime.now().strftime("%Y%m%d%H%M%S"))
            new_user = Auth(uid, hash_password(password), email, False)
            db.session.add(new_user)
            db.session.flush()

            date = datetime.now()
            userinfo = User('', '', '', email, '', access, '', '', '', '', uid, '', date)
            db.session.add(userinfo)
            db.session.commit()
            db.session.close()

            token = generate_email_token(email)
            link = url_for('confirm', token=token, external=True)
            confirm_msg = 'Dear Customer,<br/>We have created a customer account for you on our website. To activate your account, please click the link below: <br /><a href="{}">Click to confirm your email</a><br /><br /><br />Please note that the link expires in 24 hours.<br />We thank you for choosing PCL Consult<br /> <br /> <h2 style="font-weight:600">The PCL Consult Team</h2><br />'.format(link)
            send_email(
                "Validate your account", [email], confirm_msg, True
            )
            return make_response({
                "message": "registration successful",
            }, 200)
        except exc.SQLAlchemyError as e:
            raise Exception(e._message)
        except Exception as e:
            raise Exception(str(e))

    def change_password():
        email = request.json['email']
        password = request.json['new_password']

        try:
            user = Auth.query.filter_by(email = email).first()
            if not user:
                return make_response({
                    "error": "email is invalid"
                }, 400)

            user.email = email
            user.password = hash_password(password)
            db.session.add(user)
            db.session.commit()
            db.session.close()
            return make_response({
                "message": "password changed",
            }, 200)
        except exc.SQLAlchemyError as e:
            raise Exception(e._message)
        except Exception as e:
            raise Exception(str(e))

    def confirm_password_link():
        try:
            resp = confirm_email_token(token, "email-forgot")
            if resp == False:
                return make_response({
                    "error": "confirmation link expired or invalid"
                }, 400)
            
            user = Auth.query.filter_by(email = resp).first()

            email = user.email
            password = "pwd" + str(int(datetime.now().strftime("%Y%m%d%H%M%S")))
            user.password = hash_password(password)
            db.session.add(user)
            db.session.commit()
            db.session.close()
            confirm_msg = "To access your account please use the password below<br /><b>Your new paswword is: <h3>{}</h3></b>".format(password)
            send_email(
                "New password for you account", [email], confirm_msg, True
            )
            return make_response({
                "message": "new password changed",
            }, 200)
        except exc.SQLAlchemyError as e:
            raise Exception(e._message)
        except Exception as e:
            raise Exception(str(e))

    def forgot_password():
        email = request.json['email']
        password = request.json['new_password']

        try:
            user = Auth.query.filter_by(email = email).first()
            if not user:
                return make_response({
                    "error": "email is invalid"
                }, 400)


            token = generate_email_token(email, 'email-forgot')
            link = url_for('forgot', token=token, external=True)
            return make_response({
                "message": "password reset link sent",
            }, 200)
        except exc.SQLAlchemyError as e:
            raise Exception(e._message)
        except Exception as e:
            raise Exception(str(e))

class Users():
    def get_all_users():
        try:
            users = User.query.all()
            return {
                "message": users_scheme.dump(users)[::-1]
            }
        except exc.SQLAlchemyError as e:
            raise Exception(e._message)
        except Exception as e:
            raise Exception(str(e))

    def get_user_info(value):
        try:
            user = User.query.filter_by(auth_id = value).first()
            if not user:
                return make_response({
                    "error": "user account not found"
                }, 400)

            userInfo = user_scheme.dump(user)  
            return {
                "message": userInfo
            }
        except exc.SQLAlchemyError as e:
            raise Exception(e._message)
        except Exception as e:
            raise Exception(str(e))

    def get_user_by(value):
        try:
            users = User.query.filter(or_(
                User.email.like(value), User.auth_id.like(value), User.firstname.like(value),
                User.access.like(value), User.sex.like(value),User.country.like(value))).join(
                Auth, Auth.uid == User.auth_id).all()
            if not users:
                return make_response({
                    "error": "user account not found"
                }, 400)

            usersResults = []
            for user in users:
                userObject = user_scheme.dump(user)
                userObject['isverified'] = user.isVerified
                usersResults.append(userObject)
            return {
                "message": usersResults[::-1]
            }
        except exc.SQLAlchemyError as e:
            raise Exception(e._message)
        except Exception as e:
            raise Exception(str(e))

    def add_userinfo():
        email = request.json['email']
        auth_id = request.json['auth_id']
        sex = request.json['sex']
        phone = request.json['phone']
        address = request.json['address']
        access = request.json['access']
        city = request.json['city']
        country = request.json['country']
        username = request.json['username']
        firstname = request.json['firstname']
        lastname = request.json['lastname']
        image = request.json['image']
        try:
            auth = Auth.query.filter_by(email = email).first()
            if not auth:
                return make_response({
                    "error": "invalid email address"
                }, 400)
            
            date = datetime.now()
            userinfo = User(username, firstname, lastname, email, sex, access, phone, address, city, country, auth_id, image, date)
            db.session.add(userinfo)
            db.session.commit()
            db.session.close()
            return make_response({
                "message": "user info saved",
            }, 200)
        except exc.SQLAlchemyError as e:
            raise Exception(e._message)
        except Exception as e:
            raise Exception(str(e))

    def update_userinfo(uid):
        email = request.json['email']
        username = request.json['username']
        firstname = request.json['firstname']
        lastname = request.json['lastname']
        image = request.json['image']
        try:
            userInfo = User.query.filter_by(auth_id = uid).first()
            authinfo = Auth.query.filter_by(uid = uid).first()
            if not authinfo or not userInfo:
                return make_response({
                    "error": "invalid user id"
                }, 400)

            userInfo.firstname = firstname
            userInfo.lastname = lastname
            userInfo.username = username
            userInfo.image = image
            authinfo.email = userInfo.email = email
            db.session.add(userInfo)
            db.session.add(authinfo)
            db.session.commit()
            db.session.close()
            return make_response({
                "message": "user info updated",
            }, 200)
        except exc.SQLAlchemyError as e:
            raise Exception(e._message)
        except Exception as e:
            raise Exception(str(e))
