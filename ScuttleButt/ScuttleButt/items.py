# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScuttlebuttItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Price = scrapy.Field()
    Content = scrapy.Field()
    Destination = scrapy.Field()

    #kayak price
    Kayak_Price = scrapy.Field()
    Kayak_Destination = scrapy.Field()

    #LatLongSpider.py
    LatLong = scrapy.Field()
    Airport_Name = scrapy.Field()
    Identifier = scrapy.Field()
    #############################

    Source_Website = scrapy.Field()
    pass
