from cell import Cell

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://jiggoha:pass_word@localhost/hobby_dev_crossword"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Clue(db.Model):
  # values that Clue.direction can take:
  ACROSS = True
  DOWN = False
  
  def __init__(self, number, direction, question, answer):
    self.number = number
    self.direction = direction
    self.question = question # string
    self.answer = answer # string
    self.cells = [] # a list of Cell objects that the clue contains

  def finished(self):
  	for cell in self.cells:
  		if cell.content == None:
  			return False
  	return True