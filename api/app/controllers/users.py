from models.modules.core import logger, request, InvalidUsage, make_response, app, url_for, redirect
from models.dbmodels.user_model import *
from models.libs.jwt import *
from models.libs.mailing import *
from datetime import datetime
import os
import ast

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
            uid = userinfo.uid
            userinfo.isVerified = True
            db.session.commit()
            db.session.close()

            welcome_msg = f'''
            <b>Dear Customer</b><br />
            <p>Congratulations and thanks for activating your account. Please find below your account details are</p>
            <p>Email: <b>{email}</b></p>
            <p>Customer Identification number: <b>{uid}</b></p>
            <p>Once again welcome aboard.</p><br />
            '''
            send_email(
                "Welcome email", [email], welcome_msg, True, '', 'Kreador Chat account <noreply@kreadortech.io>'
            )
            return redirect(f"{app.config['SITE_URL']}login", code=302)
        except exc.SQLAlchemyError as e:
            raise Exception(e._message)
        except Exception as e:
            raise Exception(str(e))

    def login():
        email = request.json['email']
        password = request.json['password']
        user = Auth.query.filter_by(email = email).first()
        userInfo = User.query.filter_by(email = email).first()
        if not user or not userInfo:
            return make_response({
                "error": "user email is invaild"
            }, 404)

        if user.isVerified == 0:
            token = generate_email_token(email)
            link = url_for('confirm', token=token, external=True)
            link = f"{app.config['URL']}../{link}"
            confirm_msg = f'''
            Dear Customer,<br/>
            We have created an account for you on our platform. To activate your account, please click the link below: <br />
            <a href="{link}">Click to confirm your email</a><br /><br /><br />
            Please note that the link expires in 24 hours.<br /><br /> 
            <h4 style="font-weight:600">Kreador Team</h4>
            '''
            send_email(
                "Validation required", [email], confirm_msg, True, '', 'Kreador Chat account <noreply@kreadortech.io>'
            )
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
            "access": userInfo.access,
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
            if not user or not obj:
                return make_response({
                    "error": "user account info not found"
                }, 400)
            db.session.delete(user)
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
            userinfo = User('', '', '', email, '', uid, '', '', date)
            db.session.add(userinfo)
            db.session.commit()
            db.session.close()

            token = generate_email_token(email)
            link = url_for('confirm', token=token, external=True)
            link = f"{app.config['URL']}{link}"
            confirm_msg = f'''
            Dear Customer,<br/>
            We have created an account for you on our platform. To activate your account, please click the link below: <br />
            <a href="{link}">Click to confirm your email</a><br /><br /><br />
            Please note that the link expires in 24 hours.<br /><br /> 
            <h4 style="font-weight:600">Kreador Team</h4>
            '''
            send_email(
                "Validate your account", [email], confirm_msg, True, '', 'Kreador Chat account <noreply@kreadortech.io>'
            )
            return make_response({
                "message": "registration successful"
            }, 200)
        except exc.SQLAlchemyError as e:
            raise Exception(e._message)
        except Exception as e:
            raise Exception(str(e))

    def change_password():
        email = request.json['email']
        password = request.json['new_password']
        oldpassword = request.json['password']

        try:
            user = Auth.query.filter_by(email = email).first()
            if not user:
                return make_response({
                    "error": "email is invalid"
                }, 400)

            check = verify_password(user.password, oldpassword)
            if check == False:
                return make_response({
                    "error": "old password is incorrect"
                }, 401)

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
                User.email.like(value), User.auth_id.like(value), User.fullname.like(value), User.sex.like(value))).join(
                Auth, Auth.uid == User.auth_id).all()
            if not users:
                return make_response({
                    "error": "user account not found"
                }, 400)

            usersResults = []
            for user in users:
                userObject = user_scheme.dump(user)
                usersResults.append(userObject)
            return {
                "message": usersResults[::-1]
            }
        except exc.SQLAlchemyError as e:
            raise Exception(e._message)
        except Exception as e:
            raise Exception(str(e))

    def update_userinfo(uid):
        email = request.json['email']
        auth_id = request.json['auth_id']
        sex = request.json['sex']
        phone = request.json['phone']
        fullname = request.json['fullname']
        username = request.json['username']
        image = request.json['image']
        try:
            userInfo = User.query.filter_by(auth_id = uid).first()
            authinfo = Auth.query.filter_by(uid = uid).first()
            if not authinfo or not userInfo:
                return make_response({
                    "error": "invalid user id"
                }, 400)

            userInfo.fullname = fullname
            userInfo.username = username
            userInfo.sex = sex
            userInfo.phone = phone

            authinfo.email = userInfo.email = email
            userInfo.auth_id = authinfo.uid
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
