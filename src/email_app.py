from logging import fatal
import smtplib
import os
from .email.message import EmailMessage
from .email.mime.text import *
import logging

def send_email(email_content, RECIPIENTS = [("Alice", "sample@email.com")], SUBJECT = "Update"):
    """
    Function to send email updates to registered recipients
    """
    
    FROM = os.getenv("FROM")
    
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(FROM, os.getenv("pwd"))

        for name, email in RECIPIENTS:
            # Send custom message to recipient

            message = EmailMessage()
            message["Subject"] = SUBJECT
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
