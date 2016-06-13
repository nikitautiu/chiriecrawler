# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RentItem(scrapy.Item):
    """Generic data for all rents"""
    title = scrapy.Field()
    price = scrapy.Field()
    link = scrapy.Field()
    date = scrapy.Field()  # data at which the offer has been added
    views = scrapy.Field()
    keywords = scrapy.Field()  # any locaton data mined from description


class OlxRentItem(scrapy.Item):
    """Contains all relevant data for an Olx rent"""
    title = scrapy.Field()
    price = scrapy.Field()
    link = scrapy.Field()
    descr = scrapy.Field()  # field for description, used for extracting keywords
    age = scrapy.Field()  # data at which the offer has been added
    views = scrapy.Field()

