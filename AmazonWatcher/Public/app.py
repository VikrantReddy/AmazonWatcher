from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from Amazon.Public import app, db
from Amazon.Utils import User

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.session.query_property(User.user_id==int(user_id))

from Amazon.Public.auth import auth as auth_blueprint

app.register_blueprint(auth_blueprint)

from Amazon.Public.main import main as main_blueprint

app.register_blueprint(main_blueprint)

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)