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
check = None
check_displayed = True

@app.route("/new_puzzle", methods=["GET", "POST"])
def new_puzzle():
  if request.method == "GET":
    return render_template('new_puzzle.html')

  elif request.method == "POST":
    date = request.form['date']

    global cluesAcross, cluesDown, state, check, check_displayed
    cluesAcross = parser.create_clues_across(date)
    cluesDown = parser.create_clues_down(date)
    state = parser.create_state(date)
    check = None
    check_displayed = True

    return redirect(url_for("index"))

@app.route("/")
def index():
  global state, cluesAcross, cluesDown, check, check_displayed

  # puzzle is not set up
  if not cluesAcross:
    return redirect(url_for("new_puzzle"))

  return render_template('index.html', state=state, cluesAcross=cluesAcross, cluesDown=cluesDown, check=check)

@app.route("/command/", methods=["POST"])
def command():
  global state, check, check_displayed
  
  if check_displayed is False:
    check_displayed = True
    check = None

  clue = request.form['clue']
  position = request.form['position']
  solution = request.form['solution'].upper()
  command_type = request.form['command_type']

  if command_type == "Fill":
    if position:
      state.submit_letter(clue, int(position), solution)
    else:
      state.submit_word(clue, solution)
  elif command_type == "Delete":
    if position:
        state.delete_letter(clue, int(position))
    else:
      state.delete_word(clue)
  elif command_type == "Check":
    check_displayed = False
    if state.check_solution():
      check = True
    else:
      check = False
  elif command_type == "New Puzzle":
    return redirect(url_for("new_puzzle"))

  return redirect(url_for("index"))

if __name__ == "__main__":
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port)