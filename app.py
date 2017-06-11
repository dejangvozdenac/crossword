import puz
import parser
from cell import Cell
from clue import Clue
from flask import Flask, render_template, request, redirect, url_for
import requests
app = Flask(__name__)

cluesAcross = parser.create_clues_across()
cluesDown = parser.create_clues_down()
state = parser.create_state()

@app.route("/new_puzzle", methods=["GET", "POST"])
def new_puzzle():
  if request.method == "GET":
    return render_template('new_puzzle.html')
  elif request.method == "POST":
    date = request.form['date']
    return redirect(url_for("index", date=date))

@app.route("/")
def index(date=None):
  global state, cluesAcross, cluesDown
  return render_template('index.html', state=state, cluesAcross=cluesAcross, cluesDown=cluesDown)

@app.route("/command/", methods=["POST"])
def command():
  global state
  clue = request.form['clue']
  position = request.form['position']
  solution = request.form['solution'].upper()
  fill = (request.form['fill'] == "fill")

  if fill:
    if position:
        state.submit_letter(clue, int(position), solution)
    else:
      state.submit_word(clue, solution)
  else:
    if position:
        state.delete_letter(clue, int(position))
    else:
      state.delete_word(clue)

  return redirect(url_for("index"))

if __name__ == "__main__":
  app.run(debug=True)