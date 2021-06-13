import smtplib
import os
from email.message import EmailMessage
from email.mime.text import *

def send_email(TEXT,  FROM = os.getenv("FROM"), TO = ["b4ck10up@gmail.com"], SUBJECT = "Update"):
    """
    Function to send email updates to recipients
    """
    message = EmailMessage()
    message["Subject"] = SUBJECT
    message["From"] = FROM
    message["Bcc"] = TO
    message["To"] = FROM
    
    message.set_content(TEXT)
    
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(FROM, os.getenv("pwd"))
        server.send_message(message)
        server.close()
        return True
    except Exception as e:
        print(e)
        return False
