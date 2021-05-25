from flask import Flask, request, render_template
from ..database import check_user, create_user, create_connection
database = "../res/database.db"

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user = (request.form["name"], request.form["email"])
        # TODO validate email
        conn = create_connection(database)
        create_user(conn, user)
        return render_template("success.html", name=request.form["name"])

    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=False)
