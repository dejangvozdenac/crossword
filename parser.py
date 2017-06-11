import puz
import os.path
from clue import Clue
from cell import Cell
from state import State

# date format = yy.mm.dd
def save_puzzle(date):
  filename = date + ".puz"
  url = "http://www.jacobshufro.com/xwords2/puzs/" + filename
  response = requests.get(url)

  with open("puzs/" + filename, 'w') as f:
    the_file.write(response.text)
    
def create_clues_across(date):
	path_name = "puzs/" + date + ".puz"
	if not os.path.isfile(path_name):
		save_puzzle(date)
	p = puz.read(path_name)

	numbering = p.clue_numbering()
	cluesAcross = []
	for clue in numbering.across:
		answer = ''.join(
	        p.solution[clue['cell'] + i]
	        for i in range(clue['len']))
		cluesAcross.append(Clue(clue['num'], True, clue['clue'], answer, False))
	return cluesAcross

def create_clues_down(date):
	path_name = "puzs/" + date + ".puz"
	if not os.path.isfile(path_name):
		save_puzzle(date)
	p = puz.read(path_name)

	numbering = p.clue_numbering()
	cluesDown = []
	for clue in numbering.down:
		answer = ''.join(
	        p.solution[clue['cell'] + i]
	        for i in range(clue['len']))
		cluesDown.append(Clue(clue['num'], False, clue['clue'], answer, False))
	return cluesDown

def create_state(date):
	path_name = "puzs/" + date + ".puz"
	if not os.path.isfile(path_name):
		save_puzzle(date)
	p = puz.read(path_name)
	
	state = State(p)
	return state