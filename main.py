import puz
from clue import Clue
from cell import Cell

p = puz.read('example.puz')

numbering = p.clue_numbering()
cluesAcross = []
cluesDown = []

for clue in numbering.across:
	answer = ''.join(
        p.solution[clue['cell'] + i]
        for i in range(clue['len']))
	cluesAcross.append(Clue(clue['num'], True, clue['clue'], answer, False))

for clue in numbering.down:
	answer = ''.join(
        p.solution[clue['cell'] + i]
        for i in range(clue['len']))
	cluesDown.append(Clue(clue['num'], False, clue['clue'], answer, False))


state = [[None for i in range(p.height)] for i in range(p.height)]

for row in range(p.height):
	for col in range(p.height):
		value = p.fill[row*p.width + col]
		if value == "." :
			state[row][col] = Cell("BLACK", False, None, None)
		elif (row == 0 or col == 0 or state[row-1][col-1].variety == "BLACK") :
			state[row][col] = Cell("WHITE", True, None, p.solution[row*p.width + col])
		else :
			state[row][col] = Cell("WHITE", False, None, p.solution[row*p.width + col])