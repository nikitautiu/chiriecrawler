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
    surface = scrapy.Field()
    is_decomandat = scrapy.Field()
    is_agency = scrapy.Field()
    has_pictures = scrapy.Field()
    date = scrapy.Field()  # data at which the offer has been added
    views = scrapy.Field()



class OlxRentItem(RentItem):
    """Contains all relevant data for an Olx rent"""
    descr = scrapy.Field()  # field for description, used for extracting keywords

