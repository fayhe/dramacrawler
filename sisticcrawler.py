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
from optparse import OptionParser

topK = 10
elasticsearch_ip = '172.31.5.42'


class SisticSpider(scrapy.Spider):
    name = 'sisticspider'
    es = Elasticsearch() ##PROD TODO:
    ##es = Elasticsearch([elasticsearch_ip])
    host_url = 'http://www.sistic.com.sg'

    def __init__(self, area=None, *args, **kwargs):
        super(SisticSpider, self).__init__(*args, **kwargs)
        start_urls = []
        
        ##TODO: page num
        for num in range(1,3): 
            start_urls.append('http://www.sistic.com.sg/events/search?c=Theatre&l=20&o=1&p=%d' % (num))
        self.start_urls = start_urls
        self.name = '%s' % area

        for num1 in range(1,2): 
            start_urls.append('http://www.sistic.com.sg/events/search?c=Film&l=20&o=1&p=%d' % (num1))
        self.start_urls = start_urls
        self.name = '%s' % area        


    def parse(self, response):
        category = response.url[response.url.index('='): response.url.index('&')]

        for title in response.css('div.txt'):
 
            yield {'title': title.css('a ::attr(href)').extract_first()}



	    yield scrapy.Request(response.urljoin(title.css('a ::attr(href)').extract_first()), callback=self.parse_drama,
        meta={'url': title.css('a ::attr(href)').extract_first(),
              'title': title.css('a ::text').extract_first(),
              'category': category
              })


       # next_page = response.css('div.prev-post > a ::attr(href)').extract_first()
        #if next_page:
         #   yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def parse_drama(self, response):
        category = response.meta['category']
        drama_id = str(response.meta['url'])
        print  "url:" + self.host_url + str(response.meta['url'])
        ##get title
        title = ""
        title_not_encode = ""
        desc_not_encode = ""
        url = self.host_url + str(response.meta['url'])
        main_img = ""
        venue = ""
        ticket_price = ""
        event_date = ""
        start_sales_date = ""
        promoter_name = ""
        language = ""
        duration = ""
        desc = ""
        if len(response.xpath('//title/text()')) > 0:
            print "title: " + response.xpath('//title/text()')[0].extract().encode("utf-8")
            title = response.xpath('//title/text()')[0].extract().encode("utf-8")
            title_not_encode = response.xpath('//title/text()')[0].extract()

            
        ##get desc
        p_selectors= response.css('div.rich_content').css('div.more').extract()
        p_selectors_length = len(p_selectors)
        if p_selectors_length > 0:
            for i in range(0,p_selectors_length):
                print "desc: " + (remove_tags(p_selectors[i])).encode("utf-8").strip()
                desc = desc + (remove_tags(p_selectors[i])).encode("utf-8").strip()
                desc_not_encode = desc_not_encode + (remove_tags(p_selectors[i])).strip()

        ##get vendor, date, place and price
        vendor_selectors= response.css('div.entry')
        for vendor_selector in vendor_selectors:
            p_title_selectors = vendor_selector.css('div.title').extract();
            p_title_desc_selectors = vendor_selector.css('div.desc').extract();
          #  if len(p_title_selectors) > 0:
          #      print "key:" + (remove_tags(p_title_selectors[0])).encode("utf-8").strip()
            if len(p_title_desc_selectors) > 0 and len(p_title_selectors) > 0:
                key = (remove_tags(p_title_selectors[0])).strip()
                value = (remove_tags(p_title_desc_selectors[0])).strip()
                if key == 'Start Sales Date':
                    start_sales_date = value
                if key == 'Language':
                    language = value  
                if key == 'Duration':
                    duration = value                                                          
                if key == 'Promoter Name':
                    promoter_name = value                     
                if key == 'Event Date':
                    event_date = value   
                if key == 'Venue':
                    venue = value  
                if key == 'Ticket Pricing':
                    ticket_price = value                                                            
                print (remove_tags(p_title_selectors[0])).encode("utf-8").strip() + ":" + (remove_tags(p_title_desc_selectors[0])).encode("utf-8").strip()

         ##get main image
        image_selectors= response.css('div.display').css('div').css('a::attr(href)').extract_first()
        if image_selectors :
            main_img = self.host_url + image_selectors
            print "main_img:" + main_img


        nlp_tags = jieba.analyse.extract_tags(desc_not_encode, topK=topK, allowPOS=('ns', 'n'))
        nlp_adj_tags = jieba.analyse.extract_tags(desc_not_encode, topK=topK, allowPOS=('a'))
        nlp_all_tags = jieba.analyse.extract_tags(desc_not_encode, topK=topK)

        print(",".join(nlp_tags))

   
        ##index            
        doc = { 'id': drama_id, 
                'url': url,
                'drama_title': title_not_encode, 
                'main_img': main_img,
                'desc': desc_not_encode,
                'start_sales_date': start_sales_date,
                'language': language,
                'duration': duration,
                'promoter_name': promoter_name,
                'event_date': event_date,
                'venue': venue,
                'ticket_price': ticket_price,
                'nlp_tags': ",".join(nlp_tags),
                'nlp_all_tags': ",".join(nlp_all_tags),
                'nlp_adj_tags': ",".join(nlp_adj_tags),
                'category': category
                }
        res = self.es.index(index="drama", doc_type='sistic', id=drama_id, body=doc)          


    def closed(self, response):
        print "close";

        ##print url
