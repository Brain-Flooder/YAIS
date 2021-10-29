from flask import Flask, render_template, redirect
from threading import Thread
import random


app = Flask('')

@app.route('/')
def lol():
  if random.randint(0,10) == 0:
	  return redirect('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
  else:
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