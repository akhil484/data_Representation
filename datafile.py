from flask import Flask,render_template,jsonify
from scraper import *



app = Flask(__name__)

@app.before_first_request
def before_request():
	global fighters_name
	global fighters_record
	global dic
	fighters_name,fighters_record,dic = scrape_data()


@app.route('/')
def graphs():
	return render_template("data_pre.html",fighter_name=fighters_name,fighter_record=fighters_record)



@app.route('/stats')
def stats():
	names=[]
	numbers=[]
	for key in dic:
		if dic[key]>1:
			names.append(key)
			numbers.append(dic[key])
	return jsonify({'name':names, 'num':numbers})


if __name__=='__main__':
	app.run(debug=True)