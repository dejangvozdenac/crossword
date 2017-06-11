import os
import puz
import parser
from cell import Cell
from clue import Clue
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

cluesAcross = None
cluesDown = None
state = None
correct = False

@app.route("/new_puzzle", methods=["GET", "POST"])
def new_puzzle():
  if request.method == "GET":
    return render_template('new_puzzle.html')

  elif request.method == "POST":
    date = request.form['date']

    global cluesAcross, cluesDown, state
    cluesAcross = parser.create_clues_across(date)
    cluesDown = parser.create_clues_down(date)
    state = parser.create_state(date)

    return redirect(url_for("index"))

@app.route("/")
def index():
  global state, cluesAcross, cluesDown, correct
  return render_template('index.html', state=state, cluesAcross=cluesAcross, cluesDown=cluesDown, correct=correct)

@app.route("/hello")
def hello():
  return "hello"

@app.route("/command/", methods=["POST"])
def command():
  global state, correct
  clue = request.form['clue']
  position = request.form['position']
  solution = request.form['solution'].upper()
  command_type = request.form['command_type']

  if command_type == "fill":
    if position:
      state.submit_letter(clue, int(position), solution)
    else:
      state.submit_word(clue, solution)
  elif command_type == "delete":
    if position:
        state.delete_letter(clue, int(position))
    else:
      state.delete_word(clue)
  elif command_type == "check":
    if state.check_solution():
      correct = True

  return redirect(url_for("index"))

if __name__ == "__main__":
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port)