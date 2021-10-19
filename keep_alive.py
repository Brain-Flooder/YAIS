from flask import Flask, render_template
from threading import Thread
import random


app = Flask('')

@app.route('/')
def home():
	return render_template('home.html')

def run():
  app.run(
		host='0.0.0.0',
		port=random.randint(2000,9000)
	)

def keep_alive():
	'''
	Creates and starts new thread that runs the function run.
	'''
	t = Thread(target=run)
	t.start()