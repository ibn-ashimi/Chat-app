from models.modules.core import logger, request, InvalidUsage, make_response, app, url_for
from models.modules.mailconfig import *
from models.dbmodels.newsletter_model import *
from datetime import datetime
import ast

class Newsletter():
    def getAllSubscribers():
        try:
            users = Subscribe.query.all()
            Results = []
            for user in users:
                user.topics = ast.literal_eval(user.topics)
                Object = subscriber_scheme.dump(user)
                Results.append(Object)
            return {
                "message": Results[::-1]
            }
        except exc.SQLAlchemyError as e:
            raise Exception(e._message)
        except Exception as e:
            raise Exception(str(e))
    
    def subscribe_user():
        try:
            email = request.json['email']
            name = request.json['name']
            topics = request.json['topics']

            date = datetime.now()
            subscribeinfo = Subscribe(email, name, str(topics), date)
            db.session.add(subscribeinfo)
            db.session.commit()
            db.session.close()
            return make_response({
                "message": "subscribe info saved",
            }, 200)

        except exc.SQLAlchemyError as e:
            raise Exception(e._message)
        except Exception as e:
            raise Exception(str(e))
    
    def unsubscribe(email):
        try:
            subscriber = Subscribe.query.filter_by(email = email).first()
            if not subscriber:
                return make_response({
                    "error": "no subscriber info found"
                }, 400)
                
            db.session.delete(subscriber)
            db.session.commit()
            db.session.close()
            return make_response({
                "message": "unsubscribed successfully",
            }, 200)
        except exc.SQLAlchemyError as e:
            raise Exception(e._message)
        except Exception as e:
            raise Exception(str(e))

class Email():
    def contact(path):
        try:
            email = request.json['email']
            subject = request.json['subject']
            message = request.json['message']
            send_email(subject, [email], message, True)
            return make_response({
                "message": 'email sent'
            }, 200)
        except Exception as e:
            raise Exception(str(e))