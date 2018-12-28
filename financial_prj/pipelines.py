# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.files import FilesPipeline
import os
import pyexcel as pe

root_dir_name = '上海指数数据'

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

class FinancialPrjXlsxPipeline(object):
	def open_spider(self, spider):
		cur_dir = os.getcwd()
		dir_full_name = os.path.join(cur_dir, root_dir_name)
		if not os.path.exists(dir_full_name):
			os.makedirs(dir_full_name)

	def close_spider(self, spider):
		pass

	def process_item(self, item, spider):
		item_dict = dict(item)
		cur_dir = os.getcwd()
		#get file name
		file_name = item_dict['ssei_name']
		update_time = item_dict['update_time']
		ssei_data = item_dict['ssei_data']
		ssei_data.insert(0, update_time)
		sheet_name = file_name

		file_name = file_name.replace(' ', '') + '.xlsx'
		file_full_name = os.path.join(cur_dir, root_dir_name, file_name)	

		if os.path.exists(file_full_name):
			sheet = pe.get_sheet(file_name=file_full_name)
			update_time_list = sheet.column[0]
			if update_time not in update_time_list:
				sheet.row += ssei_data
				sheet.save_as(file_full_name)
		else:
			data = [['更新时间', '指数代码', '样本数量', '收盘', '样本均价', '成交额(亿元)', '平均股本(亿股)', '总市值(万亿)', '占比(%)', '静态市盈率'],
					ssei_data]
			pe.save_as(array=data, dest_file_name=file_full_name, sheet_name=sheet_name)
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

