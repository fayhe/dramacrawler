# coding=utf-8
import urllib2
import json
from elasticsearch import Elasticsearch
import time

tags =  ['剧情','喜剧','爱情']

for tag in tags:
    print tag
#tag = unicode(tag, "gbk")
    num = 1500
    while (num < 2000):
        url = 'https://api.douban.com/v2/movie/search?tag=%s&start=%d' % (tag,num)
        num = num + 20
        print tag
        print num
        print url
        try:
            response = urllib2.urlopen(url, timeout=60)
            html = response.read()
        except:
            continue    
        print html
        top_250_json = json.loads(html)
        es = Elasticsearch()
        for movie_json in top_250_json['subjects']:
            try:
	           movie_url = "https://api.douban.com/v2/movie/" + movie_json['id']
	           print tag
	           print num
	           print movie_url 
	           response = urllib2.urlopen(movie_url, timeout=60)
	           html = response.read()
	           detail_movie_json = json.loads(html)
	           ##print detail_movie_json
	           res = es.index(index="douban", doc_type=tag, id=movie_json['id'], body=detail_movie_json) 
	           time.sleep(24)        
            except:
		      print "except!!"



