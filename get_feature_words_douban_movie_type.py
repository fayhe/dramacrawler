# coding=utf-8
from datetime import datetime
from elasticsearch import Elasticsearch
import jieba
import jieba.analyse

es = Elasticsearch()
summary_list = []


res = es.search(index="douban", doc_type="剧情", body={"query": {"match_all": {}}})
print("Got %d Hits:" % res['hits']['total'])
for hit in res['hits']['hits']:
    ##print(hit["_source"]["summary"])
    summary_list.append(hit["_source"]["summary"])

summary_str = ''.join(summary_list)  
#print summary_str  

nlp_features = jieba.analyse.extract_tags(summary_str,allowPOS=('ns', 'n','ng','nl','t','v','a'), topK=1000)
nlp_features_list = ' '.join(nlp_features)  

print nlp_features_list