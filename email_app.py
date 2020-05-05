import smtplib
import os

def send_email(TEXT,  FROM = "b4ck10up@gmail.com", TO = "b4ck10up@gmail.com", SUBJECT = "Update"):
    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(FROM, os.getenv("pwd"))
        print("got this far")
        server.sendmail(FROM, TO, message.encode("utf-8"))
        #print("got this far")
        server.close()
        return True
    except Exception as e:
        print(e)
        return False