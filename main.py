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
import re
import logging

page_header = """
	<!DOCTYPE html>
	<html>
		<head>
			<title>User Signup</title>
			<style type="text/css">
				.error {
					color: red;
				}
			</style>
		</head>
		<body>
			<h1>
				<a href="/">Signup</a>
			</h1>
	"""

page_footer = """
		</body>
	</html>
	"""

class MainHandler(webapp2.RequestHandler):
	def get(self):
		self.redirect("/signup")


class SUHandler(webapp2.RequestHandler):
	def get(self):
		self.response.write(page_header + self.createForm() + page_footer)

	def post(self):
		username = cgi.escape(self.request.get("username"))
		password = cgi.escape(self.request.get("pw"))
		pwconfirm = cgi.escape(self.request.get("pwconfirm"))
		email = cgi.escape(self.request.get("email"))

		errors = {"user":False,"pw":False,"pwc":False,"email":False}
		errormsg = ""
		userError = "That is not a valid username"
		pwError = "That is not a valid password."
		pwConfirmError = "The passwords need to match."
		emailError = "That is not a valid email address."
		
		if username == "":
			errormsg = userError
			errors["user"] = True
		else:
			unre = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
			validate = unre.match(username)
			if not validate:
				errormsg = userError
				errors["user"] = True

		if password == "":
			errormsg = pwError
			errors["pw"] = True
		else:
			pwre = re.compile(r"^.{3,20}$")
			validate = pwre.match(password)
			if not validate:
				errormsg = pwError
				errors["pw"] = True
			
		if not pwconfirm == password:
			errormsg = pwConfirmError
			errors["pwc"] = True

		if not email == "":
			if not '.' in email:
				errormsg = emailError
				errors["email"] = True

		if errormsg == "":
			self.redirect("/welcome?username=" + username)
			error_element = ""
		else:
			error_esc = cgi.escape(errormsg, quote=True)
			error_element = "<p class='error'>" + error_esc + "</p>"
			
		u=""
		p=""
		c=""
		e=""
		if errors["user"] == True:
			u=userError
		if errors["pw"] == True:
			p=pwError
		if errors["pwc"] == True:
			c=pwConfirmError
		if errors["email"] == True:
			e=emailError

		form = self.createForm(username,email,u,p,c,e)
		errormsg = ""
		self.response.write(page_header + form + page_footer)

	def createForm(self,username="",email="",ue="",pe="",pce="",ee=""):
		return """
		<form action='/signup' method="post">
			<input type='text' name='username' placeholder='username' value='{0}'/><label class="error">{2}</label><br/>
			<input type='password' name='pw' placeholder='password'/><label class="error">{3}</label><br/>
			<input type='password' name='pwconfirm' placeholder='confirm password'/><label class="error">{4}</label><br/>
			<input type='email' name='email' placeholder='email' value='{1}'/><label class="error">{5}</label><br/>
			<input type='submit'/>
		</form>""".format(username,email,ue,pe,pce,ee)

class WelcomeHandler(webapp2.RequestHandler):
	def get(self):
		main_page = """<h2>Welcome,&nbsp;""" + self.request.get("username") + """</h2>"""
		self.response.write(page_header + main_page + page_footer)


routes = [
	('/', MainHandler),
	('/signup', SUHandler),
	('/welcome', WelcomeHandler)
]

app = webapp2.WSGIApplication(routes, debug=True)
