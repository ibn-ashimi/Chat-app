from models.modules.core import app, url_for, URLSafeTimedSerializer, SignatureExpired
import smtplib, email, base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

mail_secret = URLSafeTimedSerializer(app.config['SECRET_KEY'])
msg = MIMEMultipart()