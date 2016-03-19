from flask import Flask
from flask import request
from flask import render_template
import json
import requests
import xmltodict
import urllib
import urllib.parse
from pymongo import MongoClient

client = MongoClient('mongodb://cloud:cloud@ds015899.mlab.com:15899/cloud-p2')
db = client.get_default_database()

app = Flask(__name__)

def store_data_point(symbol, date, price):
	return db['app'].insert({ 'symbol': symbol, 'date': date, 'price': price })

def get_data_point(symbol, date):
	doc = db['app'].find_one({ 'symbol': symbol, 'date': date })
	if doc is None:
		# point not in database
	return doc.price

def get_prediction(symbol, startDate, endDate):
	pass
	#startPrice = get_data_point(symbol,)

def parse_api_error(obj):
	return None # TODO: parse errors and return in custom format

def create_error(message):
	return { 'error': { 'message': message } }

def wrap_get_request(url, params):
	try:
		r = requests.get(url, params)
		if r.status_code != 200:
			return create_error('request did not return correct status code')
		obj = xmltodict.parse(r.text)
		return json.dumps(parse_api_error(obj) or obj)
	except Exception as ex:
		return json.dumps(create_error(str(ex)))

def lookupStockHistory(symbol, startDate, endDate):
	url = 'http://dev.markitondemand.com/MODApis/Api/v2/InteractiveChart/json?parameters='
	params = ['Normalized', 'StartDate', 'EndDate', 'Company']
	input = {}
	input['Normalized'] = False
	input['DataPeriod'] = 'Day'

	element = [{}]
	element[0]['Symbol'] = symbol
	element[0]['Type'] = 'price'
	element[0]['Params'] = ["c"]
	input['Elements'] = element

	input['StartDate'] = startDate + 'T00:00:00-00'
	input['EndDate'] = endDate + 'T00:00:00-00'

	url = url + urllib.parse.quote(json.dumps(input))

	r = requests.get(url)
	result = json.loads(r.text)

	dates = result['Dates']
	prices = result['Elements'][0]['DataSeries']['close']['values']
	for i in range(0, len(dates)):
		store_data_point(symbol, dates[i], prices[i])

	return r.text

@app.route('/', methods=['GET', 'POST'])
def root():
	if request.method == 'POST':
		company = request.form['company']
		return render_template('index.html')
	else:
		return render_template('index.html')

@app.route('/lookup')
def lookupSymbol():
	return wrap_get_request('http://dev.markitondemand.com/Api/v2/Lookup', { 'input': request.args.get('input') })

@app.route('/quote')
def quote():
	return wrap_get_request('http://dev.markitondemand.com/Api/v2/Quote', { 'symbol': request.args.get('symbol') })

@app.route('/StockHistory')
def eliSucks():
	return lookupStockHistory(request.args.get('Company'), request.args.get('StartDate'), request.args.get('EndDate'))

if __name__ == '__main__':
	app.run(debug=True,port=8080,host='0.0.0.0')