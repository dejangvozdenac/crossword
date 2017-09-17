import requests
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
  
  with open("puzs/" + filename, 'wb') as f:
    f.write(response.content)
    

def create_clues(date):
	clues = []
	add_clues_across(clues, date)
	add_clues_down(clues, date)

	return clues

def add_clues_across(clues, date):
	path_name = "puzs/" + date + ".puz"
	if not os.path.isfile(path_name):
		save_puzzle(date)
	p = puz.read(path_name)

	numbering = p.clue_numbering()
	for clue in numbering.across:
		answer = ''.join(
	        p.solution[clue['cell'] + i]
	        for i in range(clue['len']))
		clues.append(Clue(clue['num'], Clue.ACROSS, clue['clue'], answer))
	return clues

def add_clues_down(clues, date):
	path_name = "puzs/" + date + ".puz"
	if not os.path.isfile(path_name):
		save_puzzle(date)
	p = puz.read(path_name)

	numbering = p.clue_numbering()
	for clue in numbering.down:
		answer = ''.join(
	        p.solution[clue['cell'] + i]
	        for i in range(clue['len']))
		clues.append(Clue(clue['num'], Clue.DOWN, clue['clue'], answer))
	return clues

def create_puzzle(date):
	path_name = "puzs/" + date + ".puz"
	if not os.path.isfile(path_name):
		save_puzzle(date)
	p = puz.read(path_name)
	
	return p