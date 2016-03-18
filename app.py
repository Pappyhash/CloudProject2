from flask import Flask
from flask import request
from flask import render_template
import json
import requests
import xmltodict
from pymongo import MongoClient

client = MongoClient('mongodb://cloud:cloud@ds015899.mlab.com:15899/cloud-p2')
db = client.get_default_database()

#db['app'].insert({ 'test': 'test' })

app = Flask(__name__)

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

@app.route('/')
def root():
	return render_template('index.html')

@app.route('/lookup')
def lookup():
	return wrap_get_request('http://dev.markitondemand.com/Api/v2/Lookup', { 'input': request.args.get('input') })

@app.route('/quote')
def quote():
	return wrap_get_request('http://dev.markitondemand.com/Api/v2/Quote', { 'symbol': request.args.get('symbol') })

@app.route('/StockHistory')
def lookup():
	url = 'http://dev.markitondemand.com/MODApis/Api/v2/InteractiveChart/json?parameters='
	params = ['Normalized', 'StartDate', 'EndDate', 'Company']
	input = {}
	for i in range(0,len(params)):
		if params[i] == 'Company':
			element = [{}]
			element[0]['Symbol'] = request.args.get(params[i])
			element[0]['Type'] = 'price'
			element[0]['Params'] = ["c"]
			input['Elements'] = element
		elif params[i] == 'StartDate':
			input[params[i]] = request.args.get(params[i]) + 'T00:00:00-00'
		elif params[i] == 'EndDate':
			input[params[i]] = request.args.get(params[i]) + 'T00:00:00-00'
		else:	
			input[params[i]] = request.args.get(params[i])
	
	input['DataPeriod'] = 'Day'

	url = url + urllib.quote_plus(json.dumps(input))

	r = requests.get(url)
	return r.text

if __name__ == '__main__':
	app.run(debug=True,port=8080,host='0.0.0.0')