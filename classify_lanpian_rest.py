# coding=utf-8
from flask import Flask, render_template
from classify_lanpian import predict_movie
from flask import request
import csv
import json


app = Flask(__name__)


catedict = {}
catelist = []
reader = csv.reader(open('score_category.csv'))
for i in reader :
	catelist +=[  [i[0],int(i[1]) ]  ] 
	catedict = dict(catelist)



@app.route('/')
def static_page():
    return render_template('lanpian_index.html')



@app.route("/classify_lanpian", methods = ['POST'])
def predict():
	print request.json
	name = request.json.get('name')
	summary = request.json.get('summary')
	country = request.json.get('country')
	movie_type = request.json.get('type')
	print name
	print summary
	print "movie type " + movie_type
	print country + "country"
	num = predict_movie(summary,movie_type,country)
	for (k,v) in catedict.viewitems():
		if(v==num):
			print(" do you mean...%s" % k )
			print num
			##return k
			return json.dumps({'success':True,'type': k }), 200, {'ContentType':'application/json'} 
	return "sb"

if __name__ == "__main__":
    app.run(host='0.0.0.0')