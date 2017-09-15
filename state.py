from cell import Cell
import puz

class State:
	def __init__(self, puzzle):
		circle_idxs = puzzle.markup().get_markup_squares()

		self.grid = [[None for i in range(puzzle.width)] for j in range(puzzle.height)]
		self.height = puzzle.height
		self.width = puzzle.width

		self.hor_clues = [[None for i in range(puzzle.width)] for j in range(puzzle.height)]
		self.ver_clues = [[None for i in range(puzzle.width)] for j in range(puzzle.height)]
		hor_clues_count = 0
		ver_clues_count = 0

		number = 1 # IRL indexes by 1
		for row in range(puzzle.height):
			for col in range(puzzle.width):
				flat_array_idx = row * puzzle.width + col

				color = puzzle.fill[flat_array_idx]
				if color == Cell.BLACK:
					self.grid[row][col] = Cell(variety="BLACK")
					continue

				circled = False
				if flat_array_idx in circle_idxs:
					circled = True

				cell_starts_across_clue = self._cell_starts_across_clue(row, col)
				cell_starts_down_clue = self._cell_starts_down_clue(row, col)

				white = True
				if (col == 0 or self.grid[row][col - 1].variety == "BLACK"):
					self.grid[row][col] = Cell(variety="WHITE",
																		 number=number,
																		 answer=puzzle.solution[flat_array_idx],
																		 circled=circled)
					number += 1
					self.hor_clues[row][col] = hor_clues_count
					hor_clues_count += 1
					white = False
				if (row == 0 or self.grid[row - 1][col].variety == "BLACK") :
					if (white) :
						self.grid[row][col] = Cell(variety="WHITE",
																			 number=number,
																			 answer=puzzle.solution[flat_array_idx],
																			 circled=circled)
						number += 1
					self.ver_clues[row][col] = ver_clues_count
					ver_clues_count += 1
					white = False

				if (white) :
					self.grid[row][col] = Cell(variety="WHITE",
																		 answer=puzzle.solution[flat_array_idx],
																		 circled=circled)

		self.hor_clues_rem = [0 for i in range(hor_clues_count)]
		self.ver_clues_rem = [0 for i in range(ver_clues_count)]
		self.hor_clues_capacity = [0 for i in range(hor_clues_count)]
		self.ver_clues_capacity = [0 for i in range(ver_clues_count)]
		for row in range(puzzle.height):
			for col in range(puzzle.width):
				color = puzzle.fill[row*puzzle.width + col]
				if color == Cell.BLACK:
					continue

				if (col != 0 and self.grid[row][col - 1].variety != "BLACK") :
					self.hor_clues[row][col] = self.hor_clues[row][col - 1]
				if (row != 0 and self.grid[row - 1][col].variety != "BLACK") :
					self.ver_clues[row][col] = self.ver_clues[row - 1][col]
				
				self.hor_clues_rem[self.hor_clues[row][col]] += 1
				self.ver_clues_rem[self.ver_clues[row][col]] += 1

				self.hor_clues_capacity[self.hor_clues[row][col]] += 1
				self.ver_clues_capacity[self.ver_clues[row][col]] += 1

	# private helper method
	def _cell_starts_across_clue(self, row, col):
		return col == 0 or self.grid[row][col - 1].variety == "BLACK"

	# private helper method
	def _cell_starts_down_clue(self, row, col):
		return row == 0 or self.grid[row - 1][col].variety == "BLACK"

	def parse_number(self, number, is_across):
		for row in range(self.height):
			for col in range(self.width):
				if self.grid[row][col].number == number:
					if is_across and (col == 0 or self.grid[row][col-1].variety == "BLACK"):
						return row, col
					elif not is_across and (row == 0 or self.grid[row-1][col].variety == "BLACK"):
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

	def submit_letter_exact(self, row, col, letter, cluesAcross, cluesDown):
		if (letter == ' '):
			self.delete_letter_exact(row, col, cluesAcross, cluesDown)
		elif self.grid[row][col].variety != "BLACK":
			old_letter = self.grid[row][col].content
			self.grid[row][col].content = letter
			if (old_letter != ' ' and old_letter != None):
				return

			if (self.hor_clues_rem[self.hor_clues[row][col]] > 0):
				self.hor_clues_rem[self.hor_clues[row][col]] -= 1
			if (self.hor_clues_rem[self.hor_clues[row][col]] == 0):
				cluesAcross[self.hor_clues[row][col]].finished = True

			if (self.ver_clues_rem[self.ver_clues[row][col]] > 0):
				self.ver_clues_rem[self.ver_clues[row][col]] -= 1
			if (self.ver_clues_rem[self.ver_clues[row][col]] == 0):
				cluesDown[self.ver_clues[row][col]].finished = True



	def delete_letter_exact(self, row, col, cluesAcross, cluesDown):
		if self.grid[row][col].variety != "BLACK":
			old_letter = self.grid[row][col]
			self.grid[row][col].content = None
			if (old_letter == ' ' or old_letter == None):
				return

			if (self.hor_clues_rem[self.hor_clues[row][col]] < self.hor_clues_capacity[self.hor_clues[row][col]]):
				self.hor_clues_rem[self.hor_clues[row][col]] += 1
			if (self.hor_clues_rem[self.hor_clues[row][col]] != 0):
				cluesAcross[self.hor_clues[row][col]].finished = False

			if (self.ver_clues_rem[self.ver_clues[row][col]] < self.ver_clues_capacity[self.ver_clues[row][col]]):
				self.ver_clues_rem[self.ver_clues[row][col]] += 1
			if (self.ver_clues_rem[self.ver_clues[row][col]] != 0):
				cluesDown[self.ver_clues[row][col]].finished = False

	def submit_letter(self, place, offset, letter, cluesAcross, cluesDown):
		row, col, is_across = self.parse_submission(place)

		if row is None:
			return

		if is_across:
			self.submit_letter_exact(row, col + offset - 1, letter, cluesAcross, cluesDown)
		else:
			self.submit_letter_exact(row + offset - 1, col, letter, cluesAcross, cluesDown)

	def delete_letter(self, place, offset, cluesAcross, cluesDown):
		row, col, is_across = self.parse_submission(place)

		if row is None:
			return

		if is_across:
			self.submit_letter_exact(row, col + offset - 1, None, cluesAcross, cluesDown)
		else:
			self.submit_letter_exact(row + offset - 1, col, None, cluesAcross, cluesDown)

	def submit_word(self, place, word, cluesAcross, cluesDown):
		row, col, is_across = self.parse_submission(place)

		if row is None:
			return

		for i in range(len(word)):
			self.submit_letter_exact(row, col, word[i], cluesAcross, cluesDown)
			if is_across:
				col += 1
			else:
				row += 1

	def delete_word(self, place, cluesAcross, cluesDown):
		row, col, is_across = self.parse_submission(place)

		if row is None:
			return

		while row < self.height and col < self.width and self.grid[row][col].variety != "BLACK":
			self.delete_letter_exact(row, col, cluesAcross, cluesDown)
			if is_across:
				col += 1
			else:
				row += 1

	def check_solution(self):
		result = True
		for row in range(self.height):
			for col in range(self.width):
				if self.grid[row][col].content != self.grid[row][col].answer:
					self.grid[row][col].variety = "WHITE_INCORRECT"
					result = False
				elif self.grid[row][col].variety != "BLACK":
					self.grid[row][col].variety = "WHITE"

		return result

	def uncheck_solution(self):
		for row in range(self.height):
			for col in range(self.width):
				if self.grid[row][col].variety == "WHITE_INCORRECT":
					self.grid[row][col].variety = "WHITE"

	def get_ver_clue(self, x, y):
		return self.ver_clues[x][y]

	def get_hor_clue(self, x, y):
		return self.hor_clues[x][y]