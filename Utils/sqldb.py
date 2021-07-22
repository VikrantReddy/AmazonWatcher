import pymysql

pymysql.install_as_MySQLdb()

import os
from urllib.parse import quote_plus as urlquote

import sqlalchemy

engine = sqlalchemy.create_engine(f"mysql://{os.environ.get('AMAZONWATCHER_DATABASE_USER')}:{urlquote(os.environ.get('AMAZONWATCHER_DATABASE_PASSWORD'))}@localhost/{os.environ.get('AMAZONWATCHER_DATABASE')}")
