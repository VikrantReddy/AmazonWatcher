import pymysql
pymysql.install_as_MySQLdb()

import sqlalchemy
from urllib.parse import quote_plus as urlquote
import os

engine = sqlalchemy.create_engine(f"mysql://{os.environ.get('AMAZONWATCHER_DATABASE_USER')}:{urlquote(os.environ.get('AMAZONWATCHER_DATABASE_PASSWORD'))}@localhost/{os.environ.get('AMAZONWATCHER_DATABASE')}")

from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Boolean

Base = declarative_base()


item_request = Table(
    "item_request",
    Base.metadata,
    Column("item_id", Integer, ForeignKey("amazonitem.item_id")),
    Column("request_id", Integer, ForeignKey("requests.request_id")),
)

user_request = Table(
    "user_request",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.user_id")),
    Column("request_id", Integer, ForeignKey("requests.request_id")),
)

class AmazonItem(Base):
    __tablename__ = "amazonitem"
    item_id = Column(Integer, primary_key=True)
    request_id = relationship("Requests",secondary=item_request,back_populates="item")
    
    name = Column(String(250))
    url = Column(String(250))
    price = Column(Integer)

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    requests = relationship("Requests",secondary=user_request,back_populates="user") 

    name = Column(String(50))
    email = Column(String(50))
    verified = Column(Boolean)
    req_count = Column(Integer)    

class Requests(Base):
    __tablename__ = "requests"
    request_id = Column(Integer, primary_key=True)
    item = relationship("AmazonItem",secondary=item_request,back_populates="request_id")
    user = relationship("User",secondary=user_request, back_populates = "requests")

    condition = Column(String(50))
    last_executed = Column(Integer)
    expiry = Column(Integer)
    frequency = Column(Integer)

if __name__ == "__main__":
    Base.metadata.create_all(engine)