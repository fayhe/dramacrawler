import urllib2
import json
from elasticsearch import Elasticsearch

response = urllib2.urlopen('https://api.douban.com/v2/movie/top250?start=50&count=50')
html = response.read()
top_250_json = json.loads(html)
es = Elasticsearch()
for movie_json in top_250_json['subjects']:
    try:
	    movie_url = "https://api.douban.com/v2/movie/" + movie_json['id']
	    response = urllib2.urlopen(movie_url)
	    html = response.read()
	    detail_movie_json = json.loads(html)
	    print detail_movie_json
	    res = es.index(index="douban", doc_type='movie', id=movie_json['id'], body=detail_movie_json) 
    except:
		print "except!!"



