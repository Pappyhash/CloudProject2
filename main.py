#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
import math

from google.appengine.api import users
from google.appengine.api import memcache

PRIME_PAGE_HTML = """\
<html>
  <body>
    <form action="/prime" method="post">
      <input type="number" name="number" value="number" onclick="this.select()">
      <div><input type="submit" value="Submit"></div>
    </form>
  </body>
</html>
"""

def isPrime (num):

	cachedPrime = memcache.get(str(num))

	if cachedPrime != None:
		return cachedPrime

	if (num <= 1):
		memcache.set(str(num), False)
		return False
	elif (num <= 3):
		memcache.set(str(num), True)
		return True
	elif (num % 2 == 0 or num % 3 == 0):
		memcache.set(str(num), False)
		return False

	i = 5
	w = 2
	while (i*i <= num):
		if (num % i == 0):
			memcache.set(str(num), False)
			return False
		i += w
		w = 6 - w
	memcache.set(str(num), True)
	return True

class MainHandler(webapp2.RequestHandler):
    def get(self):
    
    	user = users.get_current_user()

    	if user:
    		self.response.write('Hello ' + user.nickname() + ', please enter a number to be validated:')
    		self.response.write('<br/><br/>')

    		self.response.write(PRIME_PAGE_HTML)
    	else:
    		self.redirect(users.create_login_url(self.request.uri))

class Prime(webapp2.RequestHandler):
    def post(self):

    	self.response.write('Please enter another number to be validated:')
    	self.response.write('<br/><br/>')

        self.response.write(PRIME_PAGE_HTML)
        number = cgi.escape(self.request.get('number'))
        if isPrime(int(number)):
        	self.response.write(number + ' is a prime number')
        else:
        	self.response.write(number + ' is not a prime number')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/prime', Prime)
], debug=True)
