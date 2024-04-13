import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Mailhog SMTP server
SMTP_SERVER_HOST = "localhost"
SMTP_SERVER_PORT = 1025
SENDER_ADDRESS = "donotreply@audify.com"
SENDER_PASSWORD = "password"

def send_email(to, subject, body):
    msg = MIMEMultipart()
    msg['From'] = SENDER_ADDRESS
    msg['To'] = to
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'html'))

    smtp_server = smtplib.SMTP(SMTP_SERVER_HOST, SMTP_SERVER_PORT)
    smtp_server.login(SENDER_ADDRESS, SENDER_PASSWORD)
    smtp_server.send_message(msg)
    smtp_server.quit()

    return True
