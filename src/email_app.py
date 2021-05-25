import smtplib
import os
from email.message import EmailMessage
from email.mime.text import *

# footer = "This email app was designed by Simon J. View the source code at https://github.com/Smelton01/Site_tracker \nTo unsibcribe please click this <a href='https://github.com/Smelton01/Site_tracker'>link</a>"


def send_email(TEXT,  FROM = os.getenv("FROM"), TO = ["b4ck10up@gmail.com"], SUBJECT = "Update"):
    
    message = EmailMessage()
    message["Subject"] = SUBJECT
    message["From"] = FROM
    message["To"] = TO
    
    message.set_content(TEXT)
    # message.add_alternative(footer, subtype="html")
    # print(message)
    # Prepare the message and send the email
    # message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    # """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    
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


# send_email("This email app was designed by Simon J. View the source code at https://github.com/Smelton01/Site_tracker \nTo unsibcribe please click this <a href='https://github.com/Smelton01/Site_tracker'>link</a>")
