from flask import Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

db = SQLAlchemy()
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
app.permanent_session_lifetime = timedelta(hours=1)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
db.init_app(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    def __repr__(self):
        return '<Email %r' % self.email

@app.route('/', methods = ["GET", "POST"])
def index(): 
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        session["user"] = email
        return redirect(url_for("index"))
    else:
        return render_template("index.html")

@app.route('/register', methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        user = User(
            email=request.form["email"],
            password=request.form["password"],
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("view"))
    return render_template("register.html")

@app.route('/login', methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        found = db.one_or_404(db.select(User).filter_by(email=request.form["email"]))
        if found.password == request.form["password"]:
            return redirect(url_for("view"))
    return render_template("login.html")

@app.route('/view')
def view():
    return render_template("view.html", users = db.session.execute(db.select(User).order_by(User.email)).scalars())

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
