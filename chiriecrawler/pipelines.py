# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from chiriecrawler import items, tagger


class TagExtractorPipeline(object):
    taggable_fields = ["title", "descr"]

    def process_item(self, item, spider):
        tagger_obj = tagger.default_tagger()
        tags = set()

        for field in self.taggable_fields:
            tags.update(tagger_obj.extract(item[field]))

        result_item = items.convert_item(item, items.RentItem)
        result_item["tags"] = tags
        return result_item

