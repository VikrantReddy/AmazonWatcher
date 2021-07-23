# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from AmazonWatcher import engine
from AmazonWatcher import schema
from sqlalchemy import update
from sqlalchemy.orm import Session

OrmAmazonItem = schema.AmazonItem


class AmazonwatcherPipeline:

    def process_item(self, item, spider):
        session = Session(engine, future=True)
        statement = update(OrmAmazonItem)\
            .where(OrmAmazonItem.item_id == item.item_id)\
            .values(price=item.price)
        session.execute(statement)
        session.commit()
        return item
