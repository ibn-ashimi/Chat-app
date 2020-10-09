from models.modules.core import Mail, Message, app, url_for, URLSafeTimedSerializer, SignatureExpired
mail_secret = URLSafeTimedSerializer(app.config['SECRET_KEY'])
mailconfig = {
    "Sender": app.config['MAIL_SENDER'],
}
mail = Mail(app)