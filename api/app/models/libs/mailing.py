from models.modules.mailconfig import *

def send_email(subject, recipient_emails, body, html = False, attach = ''):
    try :
        msg = Message(subject, sender = mailconfig['Sender'], recipients = recipient_emails)
        if html == True:
            msg.html = body
        else:
            msg.body = body

        if attach != '':
            with app.open_resources(attach['url']) as attachment:
                msg.attach(attach['url'], attach['type'], attachment.read())
        mail.send(msg)
    except Exception as e:
        raise Exception(e._message)

def generate_email_token(email, type = 'email-confirm'):
    return app.config['URL'] + mail_secret.dumps(email, salt=type)

def bulk_sms(users, subject, body, html = False):
    try:
        with mail.connect() as conn:
            for user in users:
                msg = Message(subject, sender = mailconfig['Sender'], recipients = [user['email']])
                if html == True:
                    msg.html = body
                else:
                    msg.body = body
                conn.send(msg)
    except Exception as e:
        raise Exception(e._message)

def confirm_email_token(token, type = 'email-confirm'):
    try :
        return mail_secret.loads(token, salt=type, max_age=240)
    except SignatureExpired:
        return False
        