# -*- coding: utf-8 -*-
import scrapy
from financial_prj.items import SseIndexItem

class SseindexSpider(scrapy.Spider):
    name = 'sseindex'
    allowed_domains = ['www.sse.com.cn/market/sseindex/overview/focus/']
    start_urls = ['http://www.sse.com.cn/market/sseindex/overview/focus/']
    wait_element = 'div.th_div_center'
    def parse(self, response):
    	header_name_list = response.xpath('//tbody//tr[@class="greybg"]//div/text()').extract()
    	print(header_name_list)
    	sels = response.xpath('//tbody/tr[@class="isClickTr"]')
    	update_date = response.xpath('//tbody/tr/td/text()').re('更新日期：(.*)')
    	for sel in sels:
    		item = SseIndexItem()
    		item['ssei_name'] = sel.xpath('./td/a/text()').extract_first()
    		item['ssei_data'] = sel.xpath('./td/div/text()').extract()
    		item['update_time'] = update_date[0]
    		yield item