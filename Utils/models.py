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
    Column("book_id", Integer, ForeignKey("book.book_id")),
    Column("request_id", Integer, ForeignKey("requests.request_id")),
)

class AmazonItem(Base):
    __tablename__ = "amazonitem"
    item_id = Column(Integer, primary_key=True)
    
    name = Column(String)
    url = Column(String)
    price = Column(Integer)
    
    request = relationship(
        "Requests", secondary=item_request, back_populates="amazonitem"
    )

class Requests(Base):
    __tablename__ = "requests"
    request_id = Column(Integer, primary_key=True)
    
    user_id = Column(Integer, ForeignKey("users.user_id"))
    item_id = Column(Integer, ForeignKey("amazonitem.item_id"))

    conditon = Column(String)
    last_executed = Column(Integer)
    expiry = Column(Integer)
    frequency = Column(Integer)

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    
    name = Column(String)
    email = Column(String)
    verified = Column(Boolean)
    req_count = Column(Integer)
    
    request = relationship(
        "Requests", secondary=user_request, back_populates="users"
    )