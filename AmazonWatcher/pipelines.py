# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from AmazonWatcher.sqldb import sqldb

class AmazonwatcherPipeline:

    def process_item(self, item, spider):
        sqldb.add_item(item=item)
        return item
