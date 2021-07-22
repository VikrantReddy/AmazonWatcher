# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass


@dataclass    
class AmazonItem:
    name: str
    url : str
    price: int
    item_id: int

@dataclass
class User:
    name: str
    email: str
    uid : int
    reqcount : int
    verified: bool

@dataclass
class Requests:
    rid: int
    uid: int
    item_id: int
    condition: str
    last_executed: str
    expiry: str
    frequency: str
    