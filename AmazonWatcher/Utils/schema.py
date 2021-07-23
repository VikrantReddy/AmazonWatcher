from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship
from sqlalchemy.types import Boolean

from .sqldb import engine

Base = declarative_base()


item_request = Table(
    "item_request",
    Base.metadata,
    Column("item_id", String(20), ForeignKey("amazonitem.item_id")),
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
    item_id = Column(String(20), primary_key=True)
    request_id = relationship(
        "Requests", secondary=item_request, back_populates="item")

    name = Column(String(250))
    url = Column(String(250))
    price = Column(Integer)


class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    requests = relationship(
        "Requests", secondary=user_request, back_populates="user")

    name = Column(String(50))
    email = Column(String(50))
    verified = Column(Boolean)
    req_count = Column(Integer)


class Requests(Base):
    __tablename__ = "requests"
    request_id = Column(Integer, primary_key=True)
    item = relationship("AmazonItem", secondary=item_request,
                        back_populates="request_id")
    user = relationship("User", secondary=user_request,
                        back_populates="requests")

    condition = Column(String(50))
    last_executed = Column(Integer)
    expiry = Column(Integer)
    frequency = Column(Integer)


if __name__ == "__main__":
    Base.metadata.create_all(engine)
