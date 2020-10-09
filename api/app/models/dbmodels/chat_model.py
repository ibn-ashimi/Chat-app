from models.modules.dbconfig import db, ma
from sqlalchemy import exc


class ChatModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    channel_id = db.Column(db.BigInteger, unique = True)
    channel_name = db.Column(db.String(50))
    uid = db.Column(db.String(50))
    users = db.Column(db.Text())
    date_added = db.Column(db.String(50))
    chat_history = db.relationship('MessagesModel', backref="chat_model", uselist=False)


class MessagesModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    channel_id = db.Column(db.BigInteger, db.ForeignKey('chat_model.channel_id'), unique = True)
    messages = db.Column(db.Text())

class ChatModelSchema(ma.Schema):
    class Meta:
        fields = ('channel_id', 'channel_name', 'uid', 'users', 'date_added')

class MessagesModelSchema(ma.Schema):
    class Meta:
        fields = ('channel_id', 'messages')

chat_model_scheme = ChatModelSchema()
chat_models_scheme = ChatModelSchema(many = True)

messages_model_scheme = MessagesModelSchema()
messages_models_scheme = MessagesModelSchema(many = True)


db.create_all()