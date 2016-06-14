# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import datetime


class RentItem(scrapy.Item):
    """Generic data for all rents

    Will be using the following convention:
    A field will be either set or not. Not setting a field means information
    about it could not be extracted from crawling the page.
    """
    title = scrapy.Field(serizlizer=str)
    link = scrapy.Field(serializer=str)
    price = scrapy.Field(serializer=int)
    surface = scrapy.Field(serizlizer=int)
    is_decomandat = scrapy.Field(serializer=bool)
    is_agency = scrapy.Field(serializer=bool)
    has_pictures = scrapy.Field(serializer=bool)
    date = scrapy.Field(serializer=datetime.datetime)
    views = scrapy.Field(serializer=int)
    tags = scrapy.Field(serializer=list)  # keywords extracted from descr
    # and other sources, also used for post-processing


class DescrRentItem(RentItem):
    """Contains all relevant data for an unparsed rent"""
    descr = scrapy.Field()  # field for description
    # used for keyword extraction


def convert_item(item, item_cls):
    """Converts an item to another item type, ignoring incompatible fields"""
    result_item = item_cls()
    for (key, value) in item.items():
        if key in result_item.fields:
            result_item[key] = value
    return result_item