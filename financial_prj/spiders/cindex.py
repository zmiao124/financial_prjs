# -*- coding: utf-8 -*-
import scrapy
from datetime import *
import os

root_dir_name = '沪深300指数数据'
class CindexSpider(scrapy.Spider):
	name = 'cindex'
	allowed_domains = ['www.csindex.com.cn']
	def start_requests(self):
		url = 'http://www.csindex.com.cn/uploads/file/autofile/perf/000300perf.xls'
		yield scrapy.Request(url=url, meta={'skip_selenium': True}, dont_filter=True)	

	def parse(self, response):
		cur_dir = os.getcwd()
		dir_full_name = os.path.join(cur_dir, root_dir_name)
		if not os.path.exists(dir_full_name):
			os.makedirs(dir_full_name)	
		start_date = date.today()
		file_name = '000300perf' + str(start_date).replace('-', '_') + '.xls'
		file_full_name = os.path.join(dir_full_name, file_name)
		with open(file_full_name, 'wb') as f:
			f.write(response.body)