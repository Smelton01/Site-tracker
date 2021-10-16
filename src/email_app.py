from logging import fatal
import smtplib
import os
from email.message import EmailMessage
from email.mime.text import *
import logging


def send_email(email_content, recipients=[("Alice", "sample@email.com")], subject="Update"):
    """
    Send email updates to registered recipients
    :param email_content: email body
    :param recipients: list of (name, email) tuple of recipients 
    :param subject: email subject
    """

    FROM = os.getenv("FROM")

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(FROM, os.getenv("pwd"))

        for name, email in recipients:
            # Send custom message to recipient
            message = EmailMessage()
            message["Subject"] = subject
            message["From"] = FROM
            message["To"] = email
            message_content = f"Dear {name},\n {email_content}"
            message.set_content(message_content)

            server.send_message(message)
        server.close()
        return True

    except Exception as e:
        logging.error(e)
        return False
