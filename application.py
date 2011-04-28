from flask import Flask
app = Flask(__name__)

from google.appengine.ext import db
from google.appengine.api import users

from flask import redirect, url_for, request, render_template, abort, flash, get_flashed_messages

import config
from twitter import BotCore

core = BotCore()

@app.route('/')
def index():
	return 'hoge'
	#write index
	
		
@app.route('/crawl')
def crawl():
	core.get()
	return "crawl"
	
@app.route('/update')
def update():
#	core.update()
	core.post()
	return 'update'

@app.route('/amano')
def amano():
	core.amano()
	return 'amano'

@app.route('/reply')
def reply():
	core.reply()
	return 'reply'

# set the secret key.  keep this really secret:
app.secret_key = 'the secret key'

if __name__ == '__main__':
	app.run()
