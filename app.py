import puz
from clue import Clue
from flask import Flask, render_template
import requests
app = Flask(__name__)

# date format = yy.mm.dd
def save_puzzle(date):
  filename = date + ".puz"
  url = "http://www.jacobshufro.com/xwords2/puzs/" + filename
  response = requests.get(url)

  with open("puzs/" + filename, 'w') as f:
    the_file.write(response.text)

@app.route("/")
def index():
  p = puz.read('example.puz')

  numbering = p.clue_numbering()
  cluesAcross = []
  cluesDown = []

  for clue in numbering.across:
    answer = ''.join(
          p.solution[clue['cell'] + i]
          for i in range(clue['len']))
    cluesAcross.append(Clue(clue['num'], True, clue['clue'], answer))

  for clue in numbering.down:
    answer = ''.join(
          p.solution[clue['cell'] + i]
          for i in range(clue['len']))
    cluesDown.append(Clue(clue['num'], False, clue['clue'], answer))


  state = [[None for i in range(p.height)] for i in range(p.height)]

  for row in range(p.height):
    for col in range(p.height):
      state[row][col] = p.fill[row*p.width + col]

  return render_template('index.html', state=state)

if __name__ == "__main__":
  app.run()