import os
from urllib.parse import quote_plus as urlquote

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{os.environ.get('AMAZONWATCHER_DATABASE_USER')}:{urlquote(os.environ.get('AMAZONWATCHER_DATABASE_PASSWORD'))}@localhost/{os.environ.get('AMAZONWATCHER_DATABASE')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

