import smtplib
from email.mime.text import MIMEText
from twilio.rest import Client

from app.core.conf import settings


def send_notification(email: str, phone_number: str, message: str):
    send_email_notification(email, message)
    send_sms_notification(phone_number, message)


def send_email_notification(email: str, message: str):
    smtp_server = settings.SMTP_SERVER
    smtp_port = 587
    sender_email = settings.SENDER_EMAIL
    sender_password = settings.SENDER_PASSWORD
    receiver_email = email

    msg = MIMEText(message)
    msg['Subject'] = 'Room Reservation Notification'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)


# Twilio
def send_sms_notification(phone_number: str, message: str):
    account_sid = settings.ACCOUNT_SID
    auth_token = settings.AUTH_TOKEN
    twilio_number = settings.TWILIO_NUMBER

    client = Client(account_sid, auth_token)
    client.messages.create(
        body=message,
        from_=twilio_number,
        to=phone_number
    )