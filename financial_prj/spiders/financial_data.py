# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlencode
import json
import re
import chardet
import os

class FinancialDataSpider(scrapy.Spider):
	name = 'financial_data'
	allowed_domains = ['vip.stock.finance.sina.com.cn/mkt']
	start_urls = ['http://vip.stock.finance.sina.com.cn/mkt/#hs_a']
	wait_element = 'div[id="list_pages_top2"]'

	def parse(self, response):
		try:
			max_page_no = response.css('div[id="list_pages_top2"] a::text')[-2].extract()
		except IndexError:
			max_page_no = 1

		num = response.css('div[id="list_amount_ctrl"] a.active::text').extract_first()

		base_url = 'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?'
		data = {'sort':'symbol','asc': 1, 'node': 'hs_a', 'symbol': '', '_s_r_a': 'auto'}
		data['num'] = num
		for page in range(2, int(max_page_no)+1):
			data['page'] = page 
			params = urlencode(data)
			url = base_url + params
			yield scrapy.Request(url=url, callback=self.parse_page, meta={'skip_selenium': True}, dont_filter=True)

	def parse_page(self, response):
		balancesheet_url = 'http://money.finance.sina.com.cn/corp/go.php/vDOWN_BalanceSheet/displaytype/4/stockid/{code}/ctrl/all.phtml'
		profitsheet_url = 'http://money.finance.sina.com.cn/corp/go.php/vDOWN_ProfitStatement/displaytype/4/stockid/{code}/ctrl/all.phtml'
		cashflow_url = 'http://money.finance.sina.com.cn/corp/go.php/vDOWN_CashFlow/displaytype/4/stockid/{code}/ctrl/all.phtml'
		results = re.findall(r'symbol:"(.*?)".*?code:"(.*?)".*?name:"(.*?)"', response.text, re.S)
		#for result in results:
		for result in results:
			symbol, code, name = result
			url = balancesheet_url.format(code=code)
			yield scrapy.Request(url=url, callback=self.parse_file, meta={'skip_selenium': True, 'name': name, 'symbol':symbol, 'type': 'BS'}, dont_filter=True)
			url = profitsheet_url.format(code=code)
			yield scrapy.Request(url=url, callback=self.parse_file, meta={'skip_selenium': True, 'name': name, 'symbol':symbol, 'type': 'PS'}, dont_filter=True)
			url = cashflow_url.format(code=code)
			yield scrapy.Request(url=url, callback=self.parse_file, meta={'skip_selenium': True, 'name': name, 'symbol':symbol, 'type': 'CF'}, dont_filter=True)
		#return {'file_urls':[url1, url2, url3]}

	def parse_file(self, response):
		print(response.meta['name'], response.meta['type'])
		file_bname = response.headers['Content-Disposition']
		file_name = file_bname.decode('GB2312')
		#file_name = file_bname.decode(chardet.detect(file_bname)['encoding'])
		result = re.search('filename=(.*)$', file_name)
		file_name = result.group(1)
		file_name = re.sub(r'\*', '_', file_name)
		dir_name = self.settings['DOWNLOAD_DIR_PATH']
		dir_name = os.path.join('.', dir_name)
		if not os.path.exists(dir_name):
			os.makedirs(dir_name)
		file_name = os.path.join(dir_name, file_name)
		print(file_name)
		with open(file_name, 'wb') as f:
			f.write(response.body)
		#print(stock_list)

class FinancialDataSpiderTest(scrapy.Spider):
	name = 'financial_data_test'
	allowed_domains = ['vip.stock.finance.sina.com.cn/mkt']
	start_urls = ['http://vip.stock.finance.sina.com.cn/mkt/#hs_a']
	wait_element = 'div[id="list_pages_top2"]'

	def parse(self, response):
		try:
			max_page_no = response.css('div[id="list_pages_top2"] a::text')[-2].extract()
		except IndexError:
			max_page_no = 1

		num = response.css('div[id="list_amount_ctrl"] a.active::text').extract_first()

		base_url = 'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?'
		data = {'sort':'symbol','asc': 1, 'node': 'hs_a', 'symbol': '', '_s_r_a': 'auto'}
		data['num'] = num
		data['page'] = 16 
		params = urlencode(data)
		url = base_url + params
		yield scrapy.Request(url=url, callback=self.parse_page, meta={'skip_selenium': True}, dont_filter=True)

	def parse_page(self, response):
		balancesheet_url = 'http://money.finance.sina.com.cn/corp/go.php/vDOWN_BalanceSheet/displaytype/4/stockid/{code}/ctrl/all.phtml'
		profitsheet_url = 'http://money.finance.sina.com.cn/corp/go.php/vDOWN_ProfitStatement/displaytype/4/stockid/{code}/ctrl/all.phtml'
		cashflow_url = 'http://money.finance.sina.com.cn/corp/go.php/vDOWN_CashFlow/displaytype/4/stockid/{code}/ctrl/all.phtml'
		results = re.findall(r'symbol:"(.*?)".*?code:"(.*?)".*?name:"(.*?)"', response.text, re.S)
		#for result in results:
		code = '300760'
		url = balancesheet_url.format(code=code)
		yield scrapy.Request(url=url, callback=self.parse_file, meta={'skip_selenium': True}, dont_filter=True)
		url = profitsheet_url.format(code=code)
		yield scrapy.Request(url=url, callback=self.parse_file, meta={'skip_selenium': True}, dont_filter=True)
		url = cashflow_url.format(code=code)
		yield scrapy.Request(url=url, callback=self.parse_file, meta={'skip_selenium': True}, dont_filter=True)

	def parse_file(self, response):
		file_bname = response.headers['Content-Disposition']
		print ("encoding:", chardet.detect(file_bname)['encoding'])
		#file_name = file_bname.decode(chardet.detect(file_bname)['encoding'])
		print(file_bname)
		file_name = file_bname.decode('GBK',errors='ignore')

		result = re.search('filename=(.*)$', file_name)
		file_name = result.group(1)
		file_name = re.sub(r'\*', '_', file_name)
		print('file_name:', file_name)
		dir_name = self.settings['DOWNLOAD_DIR_PATH']
		dir_name = os.path.join('.', dir_name)
		if not os.path.exists(dir_name):
			os.makedirs(dir_name)
		file_name = os.path.join(dir_name, file_name)
		print(file_name)
		with open(file_name, 'wb') as f:
			f.write(response.body)
