# Author: Ekenedirichuckwu <umobieke@msu.edu>
from flask import current_app as app
from flask import render_template, redirect, request
from .utils.database.database  import database
from werkzeug.datastructures import ImmutableMultiDict
from pprint import pprint
import json
import random
db = database()

@app.route('/')
def root():
	return redirect('/home')

@app.route('/home')
def home():
	x     = random.choice(['I can spin a book.','I can solve the rubix cube within a minute.','I am Nigerian.'])
	return render_template('home.html', fun_fact = x)

@app.route('/resume')
def resume():
	resume_data = db.getResumeData() # gets resume data
	pprint(resume_data)
	return render_template('resume.html', resume_data = resume_data) # renders

@app.route('/projects')
def projects():
	return render_template('projects.html')

@app.route('/piano')
def piano():
	return render_template('piano.html')

@app.route('/processfeedback', methods = ['POST'])
def processfeedback():
  name = request.form['name']
  email = request.form['email'] 
  message = request.form['feedback-message'] # returns values from the form
    
  db.insertRows('feedback',['name', 'email', 'comment'], [[name, email, message]]) # inserts the feedback to our table
  
  feedback_data = db.getFeedbackData() # gets existing feedbacks
  
  return render_template('feedback.html', feedback_data = feedback_data) # renders