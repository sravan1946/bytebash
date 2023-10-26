from flask import Flask, jsonify, request, session, render_template
import json
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_bytes(32)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method != "POST":
        return render_template("login.html", msg="Please login")
    username = request.form["username"]
    password = request.form["password"]
    with open("./data/users.json", "r") as users:
        users = json.loads(users.read())
    if username not in users:
        return render_template("login.html", msg="Invalid username")
    if users[username] != password:
        return render_template("login.html", msg="Invalid password")
    session["user"] = username
    session["logged_in"] = True
    return render_template("index.html", msg="Login successful")

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method != "POST":
        return render_template("register.html", msg="Please register")
    username = request.form["username"]
    password = request.form["password"]
    with open("./data/users.json", "r") as user:
        users = json.loads(user.read())
    if username in users:
        return render_template("register.html", msg="Username taken")
    users[username] = password
    with open("./data/users.json", "w") as user:
        user.write(json.dumps(users))
    return render_template("login.html", msg="Registration successful")

@app.route("/logout", methods=["GET"])
def logout():
    session["logged_in"] = False
    session["user"] = None
    return render_template("login.html", msg="Logout successful")

@app.route("/upload", methods=["POST", "GET"])
def upload():
    if request.method != "POST":
        return render_template("upload.html")
    if not session.get("logged_in", False):
        return render_template("login.html", msg="Please login")
    if request.form.get("mealt","0") == "0":
        return render_template("upload.html", msg="Please select a meal type")
    with open("./data/recipies.json", "r") as upload:
        uploads = json.loads(upload.read())
        print(request.form)
    recipe = {
        "title": request.form["title"],
        "ingredients": request.form["ingredients1"],
        "instructions": request.form["instructions"],
        "author": session["user"],
        "likes": 0,
        "dislikes": 0
    }
    uploads.update({len(uploads)+1: recipe})
    with open("./data/recipies.json", "w") as upload:
        upload.write(json.dumps(uploads))
    return render_template("index.html", msg="Upload successful")

@app.route("/breakfast", methods=["GET"])
def breakfast():
    return render_template("breakfast.html")
@app.route("/lunch", methods=["GET"])
def lunch():
    return render_template("lunch.html")
@app.route("/snack", methods=["GET"])
def snack():
    return render_template("snack.html")
@app.route("/dinner", methods=["GET"])
def dinner():
    return render_template("dinner.html")


@app.route("/", methods=["GET"])
def index():
    if session.get("logged_in", False):
        return render_template("index.html")
    return render_template("login.html", msg="Please login")
