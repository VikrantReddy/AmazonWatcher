import json
import os
from urllib.parse import quote_plus as urlquote

import pymysql
import sqlalchemy

pymysql.install_as_MySQLdb()

secrets = json.load(open("secrets.json"))

engine = sqlalchemy.create_engine(
    f"mysql://{secrets.get('AMAZONWATCHER_DATABASE_USER')}:{urlquote(secrets.get('AMAZONWATCHER_DATABASE_PASSWORD'))}@localhost/{secrets.get('AMAZONWATCHER_DATABASE')}")
