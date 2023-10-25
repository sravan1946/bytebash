from flask import Flask, request, session, render_template
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
        return render_template("upload.html", msg="Please upload")
    if not session.get("logged_in", False):
        return render_template("login.html", msg="Please login")
    with open("./data/uploads.json", "r") as upload:
        uploads = json.loads(upload.read())
    # store each recipe as a dictionary with unique id
    recipe = {
        "title": request.form["title"],
        "ingredients": request.form["ingredients"],
        "instructions": request.form["instructions"],
        "author": session["user"],
        "tags": request.form["tags"],
        "image": request.form["image"],
        "likes": 0,
        "dislikes": 0
    }
    uploads.update({len(uploads): recipe})
    with open("./data/uploads.json", "w") as upload:
        upload.write(json.dumps(uploads))
    return render_template("index.html", msg="Upload successful")
    


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", user = session.get("user", "Anonymous"))
