from models.modules.mailconfig import *

def send_email(subject, recipient_emails = [], body = '', html = True, attach = '', sender = ""):
    try :
        if sender == "": 
            sender = app.config['MAIL_SENDER']
        msg['From'] = sender
        msg['To'] = ', '.join(recipient_emails)
        msg['Subject'] = subject
        if attach != '':
            with open(attach['localurl'], 'rb') as f:
                # set attachment mime and file name, the image type is png
                mime = MIMEBase(attach['type'], attach['extension'], filename=attach['filename'])
                # add required header data:
                mime.add_header('Content-Disposition', 'attachment', filename=attach['filename'])
                mime.add_header('X-Attachment-Id', '0')
                mime.add_header('Content-ID', '<0>')
                # read attachment file content into the MIMEBase object
                mime.set_payload(f.read())
                # encode with base64
                encoders.encode_base64(mime)
                # add MIMEBase object to MIMEMultipart object
                msg.attach(mime)
        if html is False:
            msg_content = MIMEText(body, 'plain', 'utf-8')
        if html is True:
            msg_content = MIMEText(body, 'html', 'utf-8')
        msg.attach(msg_content)
        mail = smtplib.SMTP(app.config['MAIL_SERVER'], app.config['MAIL_PORT']) 
        # mail = smtplib.SMTP_SSL(app.config['MAIL_SERVER'], app.config['MAIL_PORT'])
        mail.starttls()
        mail.login(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        mail.sendmail(msg['From'], msg['To'], msg.as_string())
        mail.quit()
    except Exception as e:
        print(str(e))
        raise Exception(e._message)

def generate_email_token(email, type = 'email-confirm'):
    return mail_secret.dumps(email, salt=type)

def confirm_email_token(token, type = 'email-confirm'):
    try :
        return mail_secret.loads(token, salt=type, max_age=3600)
    except SignatureExpired:
        return False
        