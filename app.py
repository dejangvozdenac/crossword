import os
import puz
import parser
from cell import Cell
from clue import Clue
from flask import Flask, render_template, request, redirect, url_for
import datetime

app = Flask(__name__)

rooms = {}
cluesAcross = None
cluesDown = None
state = None
check = None
check_displayed = True

@app.route("/new_puzzle", methods=["GET", "POST"])
def new_puzzle():
  if request.method == "GET":
    today = datetime.date.today().strftime("%y.%m.%d")
    return render_template('new_puzzle.html', today=today, room=request.args["room"])

  elif request.method == "POST":
    date = request.form['date']
    room = request.form['room']

    global cluesAcross, cluesDown, state, check, check_displayed
    cluesAcross = parser.create_clues_across(date)
    cluesDown = parser.create_clues_down(date)
    state = parser.create_state(date)

    check = None
    check_displayed = True

    return redirect(room)

@app.route("/")
def index():
  if request.args.get("room"):
    return redirect(request.args["room"])

  return redirect(url_for("join"))

@app.route("/join", methods=["GET", "POST"])
def join():
  if request.method == "GET":
    return render_template("join_room.html")
  elif request.method == "POST":
    room = request.form['room']
    rooms[room] = "placeholder" # TODO initialization
    return redirect(room)

@app.route("/<room_name>/")
def room(room_name):
  global state, cluesAcross, cluesDown, check, check_displayed, rooms

  if room_name not in rooms:
    return redirect(url_for("join"))

  # if puzzle is not set up
  if not cluesAcross:
    return redirect(url_for("new_puzzle", room=room_name))

  return render_template("index.html", state=state, cluesAcross=cluesAcross, cluesDown=cluesDown, check=check, room=room_name)

@app.route("/command/", methods=["POST"])
def command():
  room = request.args.get("room")
  if not room:
    raise Exception("Jay fucked up!") # TODO(jay): remove this after testing

  global state, check, check_displayed
  
  clue = request.form['clue']
  position = request.form['position']
  solution = request.form['solution'].upper()
  command_type = request.form['command_type']

  if command_type == "Fill":
    if position:
      state.submit_letter(clue, int(position), solution, cluesAcross, cluesDown)
    else:
      state.submit_word(clue, solution, cluesAcross, cluesDown)
  elif command_type == "Delete":
    if position:
        state.delete_letter(clue, int(position), cluesAcross, cluesDown)
    else:
      state.delete_word(clue, cluesAcross, cluesDown)
  elif command_type == "Check":
    check_displayed = False
    if state.check_solution():
      check = True
    else:
      check = False
  elif command_type == "Uncheck":
    check_displayed = True
    check = None
    state.uncheck_solution()
  elif command_type == "New Puzzle":
    return redirect(url_for("new_puzzle"))
  elif command_type == "Switch Room":
    return redirect(url_for("join"))

  if check != None:
    state.check_solution()

  return redirect(url_for("index", room=room))

if __name__ == "__main__":
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port)