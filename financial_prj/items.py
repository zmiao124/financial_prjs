# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FinancialPrjItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class SseIndexItem(scrapy.Item):
    # define the fields for your item here like:
    """
    ssei_name = scrapy.Field()
    update_time = scrapy.Field()
    ssei_no = scrapy.Field()
    ssei_num = scrapy.Field()
    ssei_closing = scrapy.Field()
    ssei_aver_price = scrapy.Field()
    ssei_vol = scrapy.Field()
    ssei_share_cap = scrapy.Field()
    ssei_total_value = scrapy.Field()
    ssei_proportion = scrapy.Field()
    ssei_pe = scrapy.Field()
    """
    ssei_name = scrapy.Field()
    update_time = scrapy.Field()
    ssei_data = scrapy.Field()

class SseIndexHeaderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
