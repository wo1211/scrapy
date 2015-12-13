import scrapy
from scrapy.selector import Selector
from image.items import ImageItem


class ImageSpider(scrapy.Spider):
    name = "img"
    allowed_domains = ["twdown.com"]
    start_urls = ["http://keet.twdown.com/bbs/forum-15-1.html"]

    def parse(self, response):
        sel = Selector(response)
        pages = sel.xpath('//td[@class="f_title"]/a[1]/@href').extract()
        for page in pages:
            url = 'http://keet.twdown.com/bbs/' + page
            yield scrapy.Request(url, callback=self.page_parse)
    
    def page_parse(self, response):
        item = ImageItem()
        #split for the contentid
        contentid = response.url.split('-')
        item['contentid'] = contentid[1]
        #split for title
        title = response.xpath('(//span[@class="bold"])[2]/text()').extract_first()
        indexa = title.find(']')
        indexb = title.rfind('[')
        item['title'] = title[indexa+1: indexb].strip()
        item['imgeurl'] = response.xpath('(//div[@class="t_msgfont"])[1]//img/@src').extract()
        return item


    
        
       