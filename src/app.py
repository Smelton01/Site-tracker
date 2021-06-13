from flask import Flask, request, render_template
from .check_posts import main
from .database import check_user, create_user, delete_user
import threading
import atexit
import re
import os
import psycopg2


POOL_TIME = 15*60 # 15 minutes


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
            return render_template("warning.html", message=message)
        
        # check if user already exists
        user_exists = check_user(conn, name, email)
        
        if user_exists:
            # TODO already registered template
            message = "Your provided email address is already registered"
            return render_template("warning.html", message=message)

        # add user to database
        result = create_user(conn, name=name, email=email)

        # TODO send email nottification with latest posts
        
        if not result:
            # TODO fail template, database error template
            return "DATABASE ERROR"
     
        return render_template("success.html", name=request.form["name"])

    else:
        return render_template("index.html")

@app.post("/unsubscribe")
def unsubscribe():
    # make database connection
    conn = psycopg2.connect(os.getenv("DATABASE_URL"), sslmode='require')

    # get form data
    name, email = request.form["name"], request.form["email"]

    # remove user from database
    delete_user(conn, email)

    return render_template("unsub.html", name=name)


if __name__ == "__main__":
    app.run(debug=False)
