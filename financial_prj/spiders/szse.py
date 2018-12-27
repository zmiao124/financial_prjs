# -*- coding: utf-8 -*-
import scrapy
import logging
from datetime import *
from urllib.parse import urlencode
import chardet
import os
import re

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
def isweekend(d):
	if d.isoweekday() == 6 or d.isoweekday() == 7:
		return True
	return False
root_dir_name = '深圳指数数据'
dir_name = {'tab1': '深圳市场',
			'tab2': '深市主板',
			'tab3': '中小企业版',
			'tab4': '创业板'}
tab_list = ['tab1']

class SzseSpider(scrapy.Spider):
	name = 'szse'
	allowed_domains = ['www.szse.cn']
	#start_urls = ['http://www.szse.cn/']
	def __init__(self, category=None, *args, **kwargs):
		super(SzseSpider, self).__init__(*args, **kwargs)
		for key, value in dir_name.items():
			cur_dir = os.getcwd()
			dir_full_name = os.path.join(cur_dir, root_dir_name, value)
			if not os.path.exists(dir_full_name):
				os.makedirs(dir_full_name)


	def start_requests(self):
		base_url = 'http://www.szse.cn/api/report/ShowReport?'
		data = {'SHOWTYPE': 'xlsx', 'CATALOGID': 1803, 'random': 0}
		if self.start_today == '1':
			start_date = date.today()
		else:
			start_date = date(2005, 1, 1)

		step = timedelta(days=1)
		end_date = date.today()
		while start_date <= end_date:
			if isweekend(start_date):
				start_date += step
				continue

			for key in dir_name.keys():
				data['txtQueryDate'] = str(start_date)
				data['TABKEY'] = key 
				params = urlencode(data)
				url = base_url + params
				#url = 'http://www.szse.cn/api/report/ShowReport?SHOWTYPE=xlsx&CATALOGID=1803&TABKEY=tab1&txtQueryDate=2004-12-27&random=0'
				yield scrapy.Request(url=url, meta={'skip_selenium': True, 'date': str(start_date), 'TABKEY': key}, dont_filter=True) 

			start_date += step

	def parse(self, response):
		reg = re.compile(r'"(.*)"')
		if response.status != 200:
			logging.error('faild to get szse!!!')

		file_bname = response.headers['Content-Disposition']
		encode_name = chardet.detect(file_bname)['encoding']
		file_name = file_bname.decode(encode_name)
		m = reg.search(file_name)
		file_name = m.group(1)
		content_length = len(response.body)
		if content_length < 4000:
			return
		info_date = response.meta['date']
		file_basename, ext_name = os.path.splitext(file_name)	
		file_name = file_basename + info_date.replace('-', '_') + ext_name
		file_full_name = os.path.join(root_dir_name, dir_name[response.meta['TABKEY']], file_name)
		with open(file_full_name, 'wb') as f:
			f.write(response.body)
