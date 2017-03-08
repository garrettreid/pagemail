#!/usr/bin/env python
from flask import Flask, render_template, url_for, redirect, request, flash, g, send_from_directory
from pagemail import EmailView, Config, close_db, set_cookie, track_user

## Initial setup ##
app = Flask(__name__)
@app.teardown_appcontext
def teardown_handler(exception):
	close_db() # closing DB seems like good form


## Our pages ##
@app.route("/")
def index():
	return render_template('index.html')

@app.route("/view/<uuid>/")
@set_cookie
def view(uuid):
	config = Config()
	email = EmailView(view_uuid=uuid)
	track_user(email.dbid)
	return render_template('view.html', email=email, config=config)

@app.route("/admin/<uuid>/")
@set_cookie
def admin(uuid):
	config = Config()
	email = EmailView(admin_uuid=uuid)
	return render_template('admin.html', email=email, views=email.views, config=config)

@app.route("/robots.txt")
def robots():
	return render_template('robots.txt')


## Shim to test run locally ##
if __name__ == "__main__":
	app.debug = True # automatically reload on code changes
	app.secret_key = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" # for local invocation
	app.run()
