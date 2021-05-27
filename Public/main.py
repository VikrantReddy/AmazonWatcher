from flask import Blueprint, render_template
from flask_login import login_required, current_user

main = Blueprint("main", __name__)


@main.route("/")
def home():
    pass

@main.route("/profile")
@login_required
def profile():
    pass
