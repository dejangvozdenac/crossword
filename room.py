from clue import Clue

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://jiggoha:pass_word@localhost/hobby_dev_crossword"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Room(db.Model):
  def __init__(self, clues_across, clues_down, state, check):
    self.clues = {}
    self.clues["across"] = [x for x in clues if x.direction == Clue.ACROSS]
    self.clues["down"]   = [x for x in clues if x.direction == Clue.DOWN]
    self.state = state