from flask import Blueprint, render_template, request
from flask_login import current_user, login_required

main = Blueprint("main", __name__)

@main.route("/")
def home(user_id):
    return render_template("home.html",name=current_user)

@main.route("/profile")
@login_required
def profile():
    pass

@main.route("/registerwatcher", methods=["POST"])
def register():
    print(request.form)
    return render_template("conditions.html",user={"name":"Sam"})
    

@main.route("/conditons")
def conditions():
    return render_template("conditions.html",user={"name":"Sam"})





