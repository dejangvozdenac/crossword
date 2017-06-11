from cell import Cell
import puz

class State:
  def __init__(self, puzzle):
    self.array = [[None for i in range(puzzle.height)] for i in range(puzzle.height)]
    for row in range(puzzle.height):
		for col in range(puzzle.height):
			value = puzzle.fill[row*puzzle.width + col]
			if value == "." :
				self.array[row][col] = Cell("BLACK", False, None, None)
			elif (row == 0 or col == 0 or self.array[row][col - 1].variety == "BLACK" or self.array[row - 1][col].variety == "BLACK"):
				self.array[row][col] = Cell("WHITE", True, None, puzzle.solution[row*puzzle.width + col])
			else :
				self.array[row][col] = Cell("WHITE", False, None, puzzle.solution[row*puzzle.width + col])