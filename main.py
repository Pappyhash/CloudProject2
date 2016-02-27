"""`main` is the top level module for your Flask application."""

# Import the Flask Framework
from flask import Flask
from flask import request
app = Flask(__name__)
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.
from google.appengine.api import memcache
from google.appengine.api import users
from math import sqrt

@app.route('/')
def hello():
	res = ''
	
	user = users.get_current_user()
	if user:
		res += 'Hello ' + user.nickname() + '! You\'re logged in. Isn\'t that cool? <a href="' + users.create_logout_url('/') + '">Logout</a><br>\n'
	else:
		res += 'Please <a href="' + users.create_login_url('/') + '">Login</a><br>\n'
		return res

	input = request.args.get('n')
	if not input or not input.isdigit():
		res += 'Please enter a number<br>\n'
		res += '<form method="get"><input name="n" /><button type="submit">Submit</button></form>'
		return res

	result = memcache.get(input)
	if result:
		res += 'cached fibonacci result: ' + str(result)
	else:
		n = int(input)
		result = int(((1+sqrt(5))**n-(1-sqrt(5))**n)/(2**n*sqrt(5)))
		memcache.set(str(n), str(result))
		res += 'calculated fibonacci result: ' + str(result)

	res += '<br><a href="/">Calculate another fibonacci number</a>'

	return res

@app.route('/reset')
def reset():
	memcache.flush_all()
	return 'cache reset'


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500
