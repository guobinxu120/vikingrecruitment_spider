# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import XmlItemExporter
from scrapy import signals

class VikingrecruitmentSpiderPipeline(object):
    def __init__(self):

        self.files = {}
    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        file = open('temp.xml' , 'w+b')
        self.files[spider] = file
        self.exporter = XmlItemExporter(file, item_element='item', root_element='channel' )
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()
        with open('temp.xml', 'r') as myfile:
            data = myfile.read().replace('<?xml version="1.0" encoding="utf-8"?>', '')
            result_file = open('output.xml', 'w+b')
            data = '<rss xmlns:atom="http://www.w3.org/2005/Atom" version="2.0">\n' + data + '\n</rss>'
            result_file.write(data)
            result_file.close()


    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


