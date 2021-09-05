from flask import Flask, request, render_template
from .check_posts import main
from .database import check_user, create_user, delete_user
from .email_app import send_email
import threading
import atexit
import re
import os
import psycopg2
import logging


POOL_TIME = 60*15 # 15 minutes
footer = "These email updates are provided by Simon J. View details  at https://github.com/Smelton01/Site_tracker \nTo unsubcribe for further updates please go to https://fuknowclass.herokuapp.com/"


# lock to control databae access
data_lock = threading.Lock()
app_thread = threading.Thread()

def create_app():
    app = Flask(__name__)

    def interrupt():
        global app_thread
        app_thread.cancel()

    def check_updates():
        global conn
        global app_thread

        with data_lock:
            # call the main scraper module to check for new posts
            main()

        # set the thread to run in the backgroud arccording to POOL_TIME interval
        app_thread = threading.Timer(POOL_TIME, check_updates, ())
        app_thread.start()

    def check_updates_start():
        """
        Initializas the thread to run in the background
        """
        global app_thread

        # create main thread
        app_thread = threading.Timer(POOL_TIME, check_updates, ())
        app_thread.start()
    
    # Initialize thread
    check_updates_start()

    # when you kill Flask (SIGTERM), clear the trigger for the next thread
    atexit.register(interrupt)
    return app

app = create_app()

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # database connection
        conn = psycopg2.connect(os.getenv("DATABASE_URL"), sslmode='require')

        # get form data
        name, email = request.form["name"], request.form["email"]

        if not re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email):
            # TODO invalid email template
            message = "Please enter a valid email address"
            logging.error(message)
            return render_template("warning.html", message=message)
        
        # check if user already exists
        user_exists = check_user(conn, name, email)
        
        if user_exists:
            # TODO already registered template
            message = "Your provided email address is already registered"
            logging.error(message)
            return render_template("warning.html", message=message)

        # add user to database
        result = create_user(conn, name=name, email=email)

        # TODO send email nottification with latest posts
        
        if not result:
            # TODO fail template, database error template
            logging.critical("DATABASE ERROR")
            return "500:DATABASE ERROR"
     
        success_email = f"\nThank You for registering on our site. \nWe will be sending you posts from the Fukuoka Now Classified section from this email as soon as they are posted.\n{footer} "
        send_email(success_email, RECIPIENTS=[(name, email)], SUBJECT="Registration Complete.")
        return render_template("success.html", name=request.form["name"])

    else:
        return render_template("index.html")

@app.post("/unsubscribe")
def unsubscribe():
    # make database connection
    conn = psycopg2.connect(os.getenv("DATABASE_URL"), sslmode='require')

    # get form data
    name, email = request.form["name"], request.form["email"]

    res = check_user(conn, name, email)

    if not res:
        message = "Your email addresss is not registered."
        logging.error(message)
        return render_template("warning.html", message=message)

    # remove user from database
    delete_user(conn, email)

    return render_template("unsub.html", name=name)


if __name__ == "__main__":
    app.run(debug=False)
