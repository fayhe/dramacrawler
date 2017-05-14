# coding=utf-8
from flask import Flask, render_template
from classify_movie import predict_movie
from flask import request
import csv
import json

app = Flask(__name__)


catedict = {}
catelist = []
reader = csv.reader(open('category.csv'))
for i in reader :
	catelist +=[  [i[0],int(i[1]) ]  ] 
	catedict = dict(catelist)



@app.route('/')
def static_page():
    return render_template('index.html')



@app.route("/classify_movie_type", methods = ['POST'])
def predict():
	print request.json
	name = request.json.get('name')
	summary = request.json.get('summary')
	print name
	print summary
	num = predict_movie(summary)
	for (k,v) in catedict.viewitems():
		if(v==num):
			print(" do you mean...%s" % k )
			print num
			##return k
			return json.dumps({'success':True,'type': k }), 200, {'ContentType':'application/json'} 
	return "sb"

if __name__ == "__main__":
    app.run(host='0.0.0.0')