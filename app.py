from flask import Flask
from flask import request
import json
import requests
import xmltodict

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

@app.route('/lookup')
def lookup():
	return wrap_get_request('http://dev.markitondemand.com/Api/v2/Lookup', { 'input': request.args.get('input') })

@app.route('/quote')
def quote():
	return wrap_get_request('http://dev.markitondemand.com/Api/v2/Quote', { 'symbol': request.args.get('symbol') })

if __name__ == '__main__':
	app.run(debug=True,port=8080,host='0.0.0.0')