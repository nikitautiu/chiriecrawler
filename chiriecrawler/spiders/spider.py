#!/bin/env python3
import scrapy
from chiriecrawler import items
from urllib import parse


def gen_search_url(no_rooms, min_price, max_price):
    """Generates a search url based on some parameters"""
    url = "http://olx.ro/imobiliare/apartamente-garsoniere-de-inchiriat/"
    if no_rooms is not None:
        url = parse.urljoin(url, "{0}-camere/".format(no_rooms))
    url = parse.urljoin(url, "cluj-napoca")
    if min_price is not None or max_price is not None:
        # dose have a query string in this case
        query_args = {}  # list of query string args
        if min_price is not None:
            min_price_str = str(min_price)
            if(min_price == 0):
                min_price_str = "free"
            query_args["search[filter_float_price:from]"] = min_price_str
        if max_price is not None:
            query_args["search[filter_float_price:to]"] = str(max_price)
        query_string = parse.urlencode(query_args)
        url = parse.urljoin(url, "?{0}".format(
            query_string))  # add query string
    return url


def parse_price(price_txt):
    return int(price_txt[:-1].strip())  # euro sign at end


class OlxSpider(scrapy.Spider):
    name = "olxspider"

    def __init__(self, no_rooms=3, min_price=None, max_price=350, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.min_price = min_price
        self.max_price = max_price
        # use the start_urls mechanism as we only have normal
        # http requests
        url = gen_search_url(no_rooms,
                             min_price,
                             max_price)
        self.start_urls = [url]


    def parse(self, response):
        """Parse function, iterates over all offer pages and
        yields all offers"""
        for offer in response.css(".offer"):
            item = items.OlxRentItem()
            item['title'] = offer.css(
                ".detailsLink strong::text").extract_first()
            price_txt = offer.css(".price strong::text").extract_first()
            item['price'] = parse_price(
                price_txt)  # remove unnecesary chars
            item['link'] = offer.css(
                ".detailsLink::attr(href)").extract_first()  # link to offer
            yield scrapy.Request(response.urljoin(item['link']),
                                 callback=self.parse_offer_page,
                                 meta={'item': item})  # pass the item to nested parser

        next_page = response.css(".next a::attr(href)")
        if next_page:
            url = response.urljoin(next_page.extract_first())
            # do the same with next pages
            yield scrapy.Request(url, self.parse)

    def parse_offer_page(self, response):
        item = response.meta['item']
        for text in response.css("#offerdescription strong a::text").extract():
            if text.strip() == "Decomandat":
                item['is_decomandat'] = True
            if text.strip() == "Semidecomandat":
                item['is_decomandat'] = False
            if text.strip() == "Agentie":
                item['is_agency'] = True
            if text.strip() == "Private":
                item['is_agency'] = False

        return item
