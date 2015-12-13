import scrapy
from scrapy import signals
from scrapy.exporters import XmlItemExporter
from scrapy.exceptions import DropItem

class ImagePipeline(object):

    def __init__(self):
        self.files = {}
        self.times = 1
        self.count = 1
        self.distant = 20

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        file = open('%s_20.xml' % self.times, 'w+b')
        self.files[spider] = file
        self.exporter = XmlItemExporter(file)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        if scrapy.Request(item['imgeurl'][1], callback=self.check):
            DropItem('No Image for this item')
        elif self.count <= self.distant:
            self.count += 1
            self.exporter.export_item(item)
            return item
        else:
            self.exporter.finish_exporting()
            file = self.files.pop(spider)
            file.close()
            self.times += 1
            file = open('%s_20.xml' % self.times, 'w+b')
            self.files[spider] = file
            self.exporter = XmlItemExporter(file)
            self.exporter.start_exporting()
            self.count = 1
            self.processs_item(item, spider)
    
    def check(self, response):
        if response.body is None:
            return false
        else:
            return true
            
            
        
