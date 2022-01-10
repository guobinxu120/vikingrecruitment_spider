import scrapy
from urlparse import urlparse
from scrapy import Request
from scrapy.utils.response import open_in_browser
from collections import OrderedDict
import csv

class CategoriesOfabcdin_cl(scrapy.Spider):

    name = "start_spider"
    # f = open('./categorii_conext.csv')
    # csv_items1 = csv.DictReader(f)
    # start_urls=[]
    # for i, row in enumerate(csv_items1):
    # 	start_urls.append(row['Link'])
    start_urls = ('http://www.vikingrecruitment.com/jobs/search/yacht/',)

    use_selenium = False

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, callback=self.parse)

    def parse(self, response):
        products = response.xpath('//div[contains(@id, "joblist")]/div')

        for div_product in products:
            item = OrderedDict()
            meta_contents = div_product.xpath('./div/dl/dd/text()').extract()
            item['title'] = meta_contents[0].strip()
            item['ref'] = div_product.xpath('./div/h3/a/text()').extract_first().replace('Details', '')
            description_item = OrderedDict()

            description_item['Employer_Type'] = meta_contents[1].strip()
            description_item['Job_Type'] = meta_contents[2].strip()
            if (len(meta_contents) > 5):
                sting_cert = ''
                for i in range(3, len(meta_contents)-1):
                    sting_cert = sting_cert +'\n'+ meta_contents[i].strip()
                description_item['Certification_Experience'] = sting_cert.strip()
            else:
                description_item['Certification_Experience'] = meta_contents[3].strip()
            description_item['Location']= meta_contents[len(meta_contents)-1].strip()
            description_item['Job_Description'] = ' '.join(div_product.xpath('.//div[@class="description-wrap"]/p//text()').extract())
            item['description'] = description_item
            yield item

