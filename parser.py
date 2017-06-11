import puz
from clue import Clue
from cell import Cell

# date format = yy.mm.dd
def save_puzzle(date):
  filename = date + ".puz"
  url = "http://www.jacobshufro.com/xwords2/puzs/" + filename
  response = requests.get(url)

  with open("puzs/" + filename, 'w') as f:
    the_file.write(response.text)
    
def create_clues_across():
	p = puz.read('example.puz')
	numbering = p.clue_numbering()
	cluesAcross = []
	for clue in numbering.across:
		answer = ''.join(
	        p.solution[clue['cell'] + i]
	        for i in range(clue['len']))
		cluesAcross.append(Clue(clue['num'], True, clue['clue'], answer, False))
	return cluesAcross

def create_clues_down():
	p = puz.read('example.puz')
	numbering = p.clue_numbering()
	cluesDown = []
	for clue in numbering.down:
		answer = ''.join(
	        p.solution[clue['cell'] + i]
	        for i in range(clue['len']))
		cluesDown.append(Clue(clue['num'], False, clue['clue'], answer, False))
	return cluesDown

def create_state():
	p = puz.read('example.puz')
	state = [[None for i in range(p.height)] for i in range(p.height)]
	for row in range(p.height):
		for col in range(p.height):
			value = p.fill[row*p.width + col]
			if value == "." :
				state[row][col] = Cell("BLACK", False, None, None)
			elif (row == 0 or col == 0 or state[row][col - 1].variety == "BLACK" or state[row - 1][col].variety == "BLACK"):
				state[row][col] = Cell("WHITE", True, None, p.solution[row*p.width + col])
			else :
				state[row][col] = Cell("WHITE", False, None, p.solution[row*p.width + col])
	return state
