from flask import Flask, request, jsonify, render_template
import json

app = Flask(__name__)

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

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")
