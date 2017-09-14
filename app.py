import os
import datetime

import puz
import parser

from cell import Cell
from clue import Clue
from room import Room

# from flask import Flask, render_template, request, redirect, url_for
# from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
# db = SQLAlchemy(app)

rooms = {}

@app.route("/new_puzzle", methods=["GET", "POST"])
def new_puzzle():
  if request.method == "GET":
    today = datetime.date.today().strftime("%y.%m.%d")
    return render_template('new_puzzle.html', today=today, room=request.args["room"])

  elif request.method == "POST":
    date = request.form['date']
    room_name = request.form['room']

    global rooms
    across_clues = parser.create_clues_across(date)
    down_clues = parser.create_clues_down(date)
    state = parser.create_state(date)
    check = None
    rooms[room_name] = Room(across_clues, down_clues, state, check)

    return redirect(room_name)

@app.route("/")
def index():
  if request.args.get("room_name"):
    return redirect(request.args["room_name"])

  return redirect(url_for("join"))

@app.route("/join", methods=["GET", "POST"])
def join():
  if request.method == "GET":
    return render_template("join_room.html")
  elif request.method == "POST":
    room_name = request.form['room_name']
    if room_name not in rooms:
      rooms[room_name] = True
    return redirect(room_name)

@app.route("/<room_name>/")
def room(room_name):
  global rooms

  # TODO(Jay): this is sort of jank right now. It will be fixed once we have persistence.
  # There exists 3 cases:
  # 1. The room has never been joined before. "room_name" is not in "rooms".
  if room_name not in rooms:
    return redirect(url_for("join"))

  # 2. The room has been joined, but there is no current puzzle. "room_name" is in "rooms", but the value of the key is True, not a Room.
  # if puzzle is not set up
  if not isinstance(rooms[room_name], Room):
    return redirect(url_for("new_puzzle", room=room_name))

  # 3. The room has been joined and there is an ongoing puzzle.
  return render_template("index.html", state=rooms[room_name].state, cluesAcross=rooms[room_name].clues["across"], cluesDown=rooms[room_name].clues["down"], check=rooms[room_name].check, room_name=room_name)

@app.route("/command/", methods=["POST"])
def command():
  global rooms

  room_name = request.args.get("room_name")
  if not room_name or room_name not in rooms:
    raise Exception("Jay fucked up!") # TODO(jay): remove this after testing

  # variables from the state of the room
  state = rooms[room_name].state
  clues_across = rooms[room_name].clues["across"]
  clues_down = rooms[room_name].clues["down"]
  
  # variables from the POST request
  clue = request.form['clue']
  position = request.form['position']
  solution = request.form['solution'].upper()
  command_type = request.form['command_type']

  if command_type == "Fill":
    if position:
      state.submit_letter(clue, int(position), solution, clues_across, clues_down)
    else:
      state.submit_word(clue, solution, clues_across, clues_down)
  elif command_type == "Delete":
    if position:
        state.delete_letter(clue, int(position), clues_across, clues_down)
    else:
      state.delete_word(clue, clues_across, clues_down)
  elif command_type == "Check":
    rooms[room_name].check_displayed = False
    if state.check_solution():
      rooms[room_name].check = True
    else:
      rooms[room_name].check = False
  elif command_type == "Uncheck":
    rooms[room_name].check_displayed = True
    rooms[room_name].check = None
    state.uncheck_solution()
  elif command_type == "New Puzzle":
    return redirect(url_for("new_puzzle"))
  elif command_type == "Switch Room":
    return redirect(url_for("join"))

  if rooms[room_name].check != None:
    state.check_solution()

  return redirect(url_for("index", room_name=room_name))

if __name__ == "__main__":
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port)