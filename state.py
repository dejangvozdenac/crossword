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

	def parse_number(self, number, is_across):
		for row in range(len(self.array)):
			for col in range(len(self.array)):
				if self.array[row][col].numbered == number:
					if is_across and (col == 0 or self.array[row][col-1].variety == "BLACK"):
						return row, col
					elif not is_across and (row == 0 or self.array[row-1][col].variety == "BLACK"):
						return row, col
					else:
						return None, None

	def parse_submission(self, place):
		number, direction = place.split()
		
		try:
			number = int(number)
		except Exception, e:
			return

		is_across = (direction.lower() == "a")
		row, col = self.parse_number(number, is_across)
		return row, col, is_across

	def submit_letter_exact(self, row, col, letter):
		if self.array[row][col].variety == "WHITE":
			self.array[row][col].letter = letter

	def delete_letter_exact(self, row, col):
		if self.array[row][col].variety == "WHITE":
			self.array[row][col].letter = None

	def submit_letter(self, place, offset, letter):
		row, col, is_across = self.parse_submission(place)

		if row is None:
			return

		if is_across:
			self.submit_letter_exact(row, col + offset - 1, letter)
		else:
			self.submit_letter_exact(row + offset - 1, col, letter)

	def delete_letter(self, place, offset):
		row, col, is_across = self.parse_submission(place)

		if row is None:
			return

		if is_across:
			self.submit_letter_exact(row, col + offset - 1, None)
		else:
			self.submit_letter_exact(row + offset - 1, col, None)

	def submit_word(self, place, word):
		row, col, is_across = self.parse_submission(place)

		if row is None:
			return

		for i in range(len(word)):
			self.submit_letter_exact(row, col, word[i])
			if is_across:
				col += 1
			else:
				row += 1

	def delete_word(self, place):
		row, col, is_across = self.parse_submission(place)

		if row is None:
			return

		while (row < len(self.array) and col < len(self.array) and self.array[row][col].variety != "BLACK"):
			self.delete_letter_exact(row, col)
			if is_across:
				col += 1
			else:
				row += 1

	def check_solution(self):
		for row in range(len(self.array)):
			for col in range(len(self.array)):
				if self.array[row][col].letter != self.array[row][col].answer:
					return False
		return True