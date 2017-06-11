from cell import Cell
import puz

class State:
	def __init__(self, puzzle):
		self.array = [[None for i in range(puzzle.height)] for i in range(puzzle.height)]
		number = 1
		for row in range(puzzle.height):
			for col in range(puzzle.height):
				value = puzzle.fill[row*puzzle.width + col]
				if value == "." :
					self.array[row][col] = Cell("BLACK", None, None, None)
				elif (row == 0 or col == 0 or self.array[row][col - 1].variety == "BLACK" or self.array[row - 1][col].variety == "BLACK"):
					self.array[row][col] = Cell("WHITE", number, None, puzzle.solution[row*puzzle.width + col])
					number += 1
				else :
					self.array[row][col] = Cell("WHITE", None, None, puzzle.solution[row*puzzle.width + col])

	def parse_number(self, number):
		for row in range(len(self.array)):
			for col in range(len(self.array)):
				if self.array[row][col].numbered == number:
					return row, col

	def submit_letter_exact(self, row, col, letter):
		if self.array[row][col].variety == "WHITE":
			self.array[row][col].letter = letter

	def submit_letter(self, place, offset, letter):
		spl = place.split()
		number = int(spl[0])
		across = (spl[1] == "a")
		row, col = self.parse_number(number)
		if across:
			self.submit_letter_exact(row, col + offset - 1, letter)
		else:
			self.submit_letter_exact(row + offset - 1, col, letter)

	def submit_word(self, place, word):
		spl = place.split()
		number = int(spl[0])
		across = (spl[1] == "a")
		row, col = self.parse_number(number)
		for i in range(len(word)):
			self.submit_letter_exact(row, col, word[i])
			if across:
				col += 1
			else:
				row += 1

	def check_solution(self, ):
		for row in range(len(self.array)):
			for col in range(len(self.array)):
				if self.array[row][col].letter != self.array[row][col].solution:
					return False
		return True