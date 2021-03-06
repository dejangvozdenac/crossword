from cell import Cell
from clue import Clue
from room import Room
from state import State
from submission import Submission

import os
import datetime

import puz
import parser
import pytz
from flask import Flask, render_template, request, redirect, url_for
# from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
# db = SQLAlchemy(app)

rooms = {}

@app.route("/new_puzzle", methods=["GET", "POST"])
def new_puzzle():
  if request.method == "GET":
    now_utc = datetime.datetime.now(pytz.timezone('UTC'))
    now_eastern = now_utc.astimezone(pytz.timezone('US/Eastern'))
    eastern_today_str = now_eastern.strftime("%y.%m.%d")

    return render_template('new_puzzle.html', today=eastern_today_str, room_name=request.args["room_name"])

  elif request.method == "POST":
    date = request.form["date"]
    room_name = request.form["room_name"]

    puzzle_date = datetime.datetime.strptime(date, "%y.%m.%d")
    human_puzzle_date = puzzle_date.strftime("%m-%d-%y")

    global rooms
    clues = parser.create_clues(date)
    puzzle = parser.create_puzzle(date)
    grid = State(puzzle, clues)
    rooms[room_name] = Room(clues, grid, human_puzzle_date)

    return redirect(url_for("room", room_name=room_name, date=human_puzzle_date))

@app.route("/")
def index():
  room_name = request.args.get("room_name")
  if room_name:
    return redirect(url_for("room",
                            room_name=room_name,
                            date=rooms[room_name].puzzle_date))

  return redirect(url_for("join"))

@app.route("/join", methods=["GET", "POST"])
def join():
  if request.method == "GET":
    return render_template("join_room.html")
  elif request.method == "POST":
    room_name = request.form['room_name']
    if room_name not in rooms:
      rooms[room_name] = True
    return redirect(url_for("room", room_name=room_name))

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
    return redirect(url_for("new_puzzle", room_name=room_name))

  # 3. The room has been joined and there is an ongoing puzzle.
  across_clues = rooms[room_name].clues["across"]
  finished_across_clues = list(filter(lambda clue: clue.finished(), across_clues))
  unfinished_across_clues = list(filter(lambda clue: not clue.finished(), across_clues))
  
  down_clues = rooms[room_name].clues["down"]
  finished_down_clues = list(filter(lambda clue: clue.finished(), down_clues))
  unfinished_down_clues = list(filter(lambda clue: not clue.finished(), down_clues))

  return render_template("index.html",
                         state=rooms[room_name].state,
                         across_clues=across_clues,
                         finished_across_clues=finished_across_clues,
                         unfinished_across_clues=unfinished_across_clues,
                         down_clues=down_clues,
                         finished_down_clues=finished_down_clues,
                         unfinished_down_clues=unfinished_down_clues,
                         room_name=room_name,
                         date=rooms[room_name].puzzle_date)

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
      state.submit(Submission.ADD_LETTER, clue, solution=solution, offset=int(position))
    else:
      state.submit(Submission.ADD_WORD, clue, solution=solution)
  elif command_type == "Delete":
    if position:
        state.submit(Submission.DELETE_LETTER, clue, offset=int(position))
    else:
      state.submit(Submission.DELETE_WORD, clue)
  elif command_type == "Check":
    state.check_solution()
  elif command_type == "Uncheck":
    state.uncheck_solution()
  elif command_type == "New Puzzle":
    return redirect(url_for("new_puzzle", room_name=room_name))
  elif command_type == "Switch Room":
    return redirect(url_for("join"))

  return redirect(url_for("index", room_name=room_name))

if __name__ == "__main__":
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port)