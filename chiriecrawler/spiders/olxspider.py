#!/bin/env python3
import scrapy
from scrapy.loader import processors
from chiriecrawler import items
from urllib import parse
import re


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


def parse_nested_int(price_values):
    return int(re.search("[0-9]+", price_values[0]).group(0))



# Custom Loader
class OlxItemLoader(scrapy.loader.ItemLoader):
    default_item_class = items.DescrRentItem
    default_output_processor = processors.TakeFirst()


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
            loader = OlxItemLoader(selector=offer)

            loader.add_css("title", ".detailsLink strong::text")
            loader.add_css("price", ".price strong::text", parse_nested_int)
            loader.add_css("link", ".detailsLink::attr(href)")

            item = loader.load_item()
            if "link" in item:
                yield scrapy.Request(response.urljoin(item['link']),
                                     callback=self.parse_offer_page,
                                     meta={'item': item})  # pass the item

        next_page = response.css(".next a::attr(href)")
        if next_page:
            url = response.urljoin(next_page.extract_first())
            # do the same with next pages
            yield scrapy.Request(url, self.parse)

    def parse_offer_page(self, response):
        loader = OlxItemLoader(response=response, item=response.meta['item'])
        loader.add_value("has_pictures", bool(response.css(".bigImage")))
        loader.add_css("views", "#offerbottombar strong::text")
        for detail in response.css(".details .item"):
            # parse the detail fields
            if detail.css("th::text").extract_first() == "Oferit de":
                loader.add_value("is_agency", detail.css(
                    "a::text").extract_first == "Agentie")
            elif detail.css("th::text").extract_first() == "Compartimentare":
                loader.add_value("is_agency", detail.css(
                    "a::text").extract_first == "Decomandat")
            elif detail.css("th::text").extract_first() == "Suprafata":
                loader.add_value("surface",
                    detail.css("strong::text").extract(), parse_nested_int)
        loader.add_css("descr", "#textContent .large::text")
        return loader.load_item()
