# coding=utf-8
import urllib2
import json
from elasticsearch import Elasticsearch
import jieba
import jieba.analyse
import jieba.posseg as pseg


def save_raw_data(file_name, data):
	file = open(file_name, 'w+')
	file.write(data.encode('utf8'))
	file.close()

def fenci(summary):
	print "hahah"
	nlp_features_list = ""
	nlp_features = pseg.cut(summary)
	for w in nlp_features:
		if w.flag == 'ns' or w.flag == 'n' or w.flag == 'ng' or w.flag == 'nl' or "a" in w.flag or "v" in w.flag or w.flag == 't':
			#print w.word + w.flag 
			nlp_features_list = nlp_features_list + " " + w.word 
	##jieba.analyse.extract_tags(summary,allowPOS=('ns', 'n','ng','nl','t','v','a'), topK=1000)
	#nlp_features_list = ' '.join(nlp_features)
	return nlp_features_list  

es = Elasticsearch()
types = ['剧情','喜剧']
folder = ['juqing','xiju']
file_root_path = '/Users/fay/Downloads/dramacrawler/raw_data/'

foler_index=0
raw_type_list = []
for type in types:
	res = es.search(index="douban", doc_type=type, size=2000, body={"query": {"match_all": {}}})
	print("Got %d Hits:" % res['hits']['total'])
	for hit in res['hits']['hits']:
		id = hit["_id"]
		print(hit["_id"])
		title = hit["_source"]["alt_title"]
		print(hit["_source"]["alt_title"])
		feature = fenci(hit["_source"]["summary"])
		save_raw_data(file_root_path + folder[foler_index] + '/' + id, title + feature)
		#print(hit["_source"]["summary"])
	foler_index = foler_index+1	
	print raw_type_list
	print("Got %d Hits:" % res['hits']['total'])



##剧情,喜剧,爱情,冒险,悬疑,犯罪,动作,家庭,奇幻,音乐,纪录片,同性,惊悚,科幻,战争,历史,儿童,古装,情色,恐怖

