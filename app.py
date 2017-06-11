import puz
import parser
from cell import Cell
from clue import Clue
from flask import Flask, render_template, request
import requests
app = Flask(__name__)

@app.route("/")
def index():
  cluesAcross = parser.create_clues_across()
  cluesDown = parser.create_clues_down()
  state = parser.create_state()

  return render_template('index.html', state=state, cluesAcross=cluesAcross, cluesDown=cluesDown)

@app.route("/command/", methods=["POST"])
def command():
  name = request.form['yourname']
  email = request.form['youremail']

  return redirect(url_for("index"))

if __name__ == "__main__":
  app.run(debug=True)