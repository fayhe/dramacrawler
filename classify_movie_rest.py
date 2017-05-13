# coding=utf-8
from flask import Flask
from classify_movie import predict_movie
from flask import request
import csv

app = Flask(__name__)


catedict = {}
catelist = []
reader = csv.reader(open('category.csv'))
for i in reader :
	catelist +=[  [i[0],int(i[1]) ]  ] 
	catedict = dict(catelist)




@app.route("/", methods = ['POST'])
def predict():
	summary = request.form['summary']
	num = predict_movie(summary)
	for (k,v) in catedict.viewitems():
		if(v==num):
			print(" do you mean...%s" % k )
			print num
			return k
	return "sb"

if __name__ == "__main__":
    app.run()