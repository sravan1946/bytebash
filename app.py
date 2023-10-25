import flask
from flask import Flask, request, jsonify, render_template
import json

app = Flask(__name__)

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method != "POST":
        return render_template("login.html", msg="Please login in")
    username = request.form["username"]
    password = request.form["password"]
    return jsonify({"username": username, "password": password})

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method != "POST":
        return render_template("register.html", msg="Please register")
    username = request.form["username"]
    password = request.form["password"]
    return jsonify({"username": username, "password": password})