from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods = ["GET", "POST"])
def home():
    #stuff

@app.route('/login', methods = ["GET", "POST"])
def login():
    # if request.method == "GET":
    #     return render_template("login.html")
    # else:
    #     user = request.form["name"]
    #     return redirect(url_for("user", usr = user))

