from flask import Blueprint,render_template
from flask_login import login_required, current_user

main = Blueprint("main", __name__)

@main.route("/")
def home():
    return render_template("home.html",user={"name":"Sam"})

@main.route("/profile")
@login_required
def profile():
    pass

@main.route("/conditons")
def conditions():
    return render_template("conditions.html",user={"name":"Sam"})





