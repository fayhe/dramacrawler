import scrapy
import sys
sys.path.append('../')

import jieba
import jieba.analyse
from optparse import OptionParser
from objdict import ObjDict
import json
from elasticsearch import Elasticsearch
from datetime import datetime
from random import randint
from time import sleep
from w3lib.html import remove_tags

class SisticSpider(scrapy.Spider):
    name = 'sisticspider'
    es = Elasticsearch()
    host_url = 'http://www.sistic.com.sg'

    def __init__(self, area=None, *args, **kwargs):
        super(SisticSpider, self).__init__(*args, **kwargs)
        start_urls = []
        
        ##TODO: page num
        for num in range(1,3): 
            print "num!!!!!!!!!!!"
            start_urls.append('http://www.sistic.com.sg/events/search?c=Theatre&l=20&o=1&p=%d' % (num))
        self.start_urls = start_urls
        self.name = '%s' % area


    def parse(self, response):
        for title in response.css('div.txt'):
 
            yield {'title': title.css('a ::attr(href)').extract_first()}



	    yield scrapy.Request(response.urljoin(title.css('a ::attr(href)').extract_first()), callback=self.parse_drama,
        meta={'url': title.css('a ::attr(href)').extract_first(),
              'title': title.css('a ::text').extract_first()
              })


       # next_page = response.css('div.prev-post > a ::attr(href)').extract_first()
        #if next_page:
         #   yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def parse_drama(self, response):
        print  "keke!!!!!!"
        print  "url:" + self.host_url + str(response.meta['url'])
        
        ##get title
        if len(response.xpath('//title/text()')) > 0:
            print "title: " + response.xpath('//title/text()')[0].extract().encode("utf-8")
        ##get desc
        p_selectors= response.css('div.rich_content').css('div.more').css('p').extract()
        p_selectors_length = len(p_selectors)
        if p_selectors_length > 0:
            for i in range(0,p_selectors_length):
                print "desc: " + (remove_tags(p_selectors[i])).encode("utf-8").strip()

        ##get vendor, date, place and price
        vendor_selectors= response.css('div.entry')
        for vendor_selector in vendor_selectors:
            p_title_selectors = vendor_selector.css('div.title').extract();
            p_title_desc_selectors = vendor_selector.css('div.desc').extract();
          #  if len(p_title_selectors) > 0:
          #      print "key:" + (remove_tags(p_title_selectors[0])).encode("utf-8").strip()
            if len(p_title_desc_selectors) > 0 and len(p_title_selectors) > 0:
                print (remove_tags(p_title_selectors[0])).encode("utf-8").strip() + ":" + (remove_tags(p_title_desc_selectors[0])).encode("utf-8").strip()

         ##get main image
        image_selectors= response.css('div.display').css('div').css('a::attr(href)').extract_first()
        if image_selectors :
            main_img = self.host_url + image_selectors
            print "main_img:" + main_img


    def closed(self, response):
        print "close";

        ##print url
