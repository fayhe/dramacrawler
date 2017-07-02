# coding=utf-8
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
import jieba.posseg as pseg
import sklearn.externals.joblib as jl
import pandas as pd
import numpy as np
import scipy.sparse


vocabulary_to_load = pickle.load(open('lanpian_vocabulary', 'r'))
fh =  TfidfVectorizer( vocabulary=vocabulary_to_load);
svclf = jl.load('lanpian.pkl')

def fenci(summary):
	nlp_features_list = ""
	nlp_features = pseg.cut(summary)
	for w in nlp_features:
		##if w.flag == 'ns' or w.flag == 'n' or w.flag == 'ng' or w.flag == 'nl' or "a" in w.flag or "v" in w.flag or w.flag == 't':
			#print w.word + w.flag 
			nlp_features_list = nlp_features_list + " " + w.word 
	##jieba.analyse.extract_tags(summary,allowPOS=('ns', 'n','ng','nl','t','v','a'), topK=1000)
	#nlp_features_list = ' '.join(nlp_features)
	return nlp_features_list 



def predict_movie(summary, category_index, country_label):
	kv = fenci(summary)

	category_array = [0,0,0,0,0,0,0,0,0,0]
	category_array[int(category_index)-1] = 1
	for_np = [category_array]

	country_array = [0,0]
	country_array[int(country_label)] = 1
	for_np_c = [country_array]
	#print kv
	fh._validate_vocabulary()
	mt = fh.fit_transform([kv])
	print for_np
	n = np.array(for_np)
	nc = np.array(for_np_c)  
	mt = scipy.sparse.hstack([mt, n, nc]) 
	num =  svclf.predict(mt)

	print num
	return num	


##predict("1958年5月25日，中共八届五中全会在北京召开，当天下午，毛泽东率领全体中央委员到十三陵水库工地参加义务劳动。工地沸腾了，领袖们谈笑风生的和普通群众肩并肩手挽手的挖土提框、搬砖运石的镜头，至今仍然感染着全国的劳动者。")


