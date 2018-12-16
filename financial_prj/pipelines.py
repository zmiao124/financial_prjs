# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.files import FilesPipeline

class FinancialPrjPipeline(object):
	def __init__ (self, mongo_uri, mongo_db):
		self.mongo_db = mongo_db
		self.mongo_uri = mongo_uri

	@classmethod
	def from_crawler(cls, crawler):
		return cls(mongo_uri=crawler.settings.get('MONGO_URI'), mongo_db = crawler.settings.get('MONGO_DB', 'financial_db'))

	def open_spider(self, spider):
		self.client = pymongo.MongoClient(self.mongo_uri)
		self.db = self.client[self.mongo_db]

	def close_spider(self, spider):
		self.client.close()

	def process_item(self, item, spider):
		item_dict = dict(item)
		collection_name = item_dict.pop('ssei_name') 
		collection =  self.db[collection_name]
		if not collection.find_one({'update_time': item['update_time']}):
			collection.insert(item_dict)
		return item
"""
class FinancialFilePipline(FilesPipeline):
	def get_media_requests(self, item, info):
		print("helloworld")
		for url in item['file_urls']:
			yield Request(url, meta={'skip_selenium': True}, dont_filter=True)

	def item_completed(self, results, item, info):
		file_paths = [x['path'] for ok, x in results if ok]
		print("hhh", file_paths)
		raise DropItem
"""

