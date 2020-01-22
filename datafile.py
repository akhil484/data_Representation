from flask import Flask,render_template,jsonify
import scraper



app = Flask(__name__)



@app.route('/')
def graphs():
	return render_template("data_pre.html",fighter_name=scraper.fighters_name,fighter_record=scraper.fighters_record)



@app.route('/stats')
def stats():
	names=[]
	numbers=[]
	for key in scraper.dic:
		if scraper.dic[key]>1:
			names.append(key)
			numbers.append(scraper.dic[key])
	return jsonify({'name':names, 'num':numbers})


if __name__=='__main__':
	app.run(debug=True)