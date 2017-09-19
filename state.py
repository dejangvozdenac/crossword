from cell import Cell
from clue import Clue
from submission import Submission
import puz

class State:
	def __init__(self, puzzle, clues):
		self.height = puzzle.height
		self.width = puzzle.width
		self.show_incorrect_cells = False
		self.clues_across = [x for x in clues if x.direction == Clue.ACROSS]
		self.clues_down   = [x for x in clues if x.direction == Clue.DOWN]
		self.grid = [[None for i in range(self.width)] for j in range(self.height)]

		circle_idxs = puzzle.markup().get_markup_squares()

		self._populate_grid(puzzle, circle_idxs)
		self._connect_with_clues(puzzle)

	#private helper method
	def _populate_grid(self, puzzle, circle_idxs):
		number = 1 # IRL indexes by 1
		for row in range(self.height):
			for col in range(self.width):
				flat_array_idx = row * self.width + col

				color = puzzle.fill[flat_array_idx]
				if color == Cell.BLACK:
					self.grid[row][col] = Cell(color=Cell.BLACK, x=col, y=row)
					continue

				circled = True if flat_array_idx in circle_idxs else False

				if self._cell_starts_across_clue(row, col) or self._cell_starts_down_clue(row, col):
					self.grid[row][col] = Cell(color=Cell.WHITE,
																		 x=col,
																		 y=row,
																		 number=number,
																		 answer=puzzle.solution[flat_array_idx],
																		 circled=circled)
					number += 1
				else:
					self.grid[row][col] = Cell(color=Cell.WHITE,
																		 x=col,
																		 y=row,
																		 answer=puzzle.solution[flat_array_idx],
																		 circled=circled)

	def _connect_with_clues(self, puzzle):
		hor_clues_count = 0
		ver_clues_count = 0

		for row in range(self.height):
			for col in range(self.width):
				hor_clue_index = None
				ver_clue_index = None

				if puzzle.fill[row*self.width + col] == Cell.BLACK:
					continue

				if self._cell_starts_across_clue(row, col):
					hor_clue_index = hor_clues_count
					hor_clues_count += 1
				else:
					hor_clue_index = self._get_clue_index(row, col - 1, Clue.ACROSS)

				if self._cell_starts_down_clue(row, col):
					ver_clue_index = ver_clues_count
					ver_clues_count += 1
				else:
					ver_clue_index = self._get_clue_index(row - 1, col, Clue.DOWN)
				
				self.grid[row][col].clue_across = self.clues_across[hor_clue_index]
				self.clues_across[hor_clue_index].cells.append(self.grid[row][col])
				self.grid[row][col].clue_down = self.clues_down[ver_clue_index]
				self.clues_down[ver_clue_index].cells.append(self.grid[row][col])

	# private helper method
	def _cell_starts_across_clue(self, row, col):
		return (col == 0 or self.grid[row][col - 1].color == Cell.BLACK)

	# private helper method
	def _cell_starts_down_clue(self, row, col):
		return (row == 0 or self.grid[row - 1][col].color == Cell.BLACK)

	def _get_clue_index(self, row, col, direction):
		if self.grid[row][col].color == Cell.BLACK:
			return None

		if direction == Clue.ACROSS:
			return self.clues_across.index(self.grid[row][col].clue_across)
		else:
			return self.clues_down.index(self.grid[row][col].clue_down)

	def parse_number(self, number, is_across):
		for row in range(self.height):
			for col in range(self.width):
				if self.grid[row][col].number == number:
					if is_across and self._cell_starts_across_clue(row, col):
						return row, col
					elif not is_across and self._cell_starts_down_clue(row, col):
						return row, col
					else:
						return None, None

	def parse_submission(self, place):
		number, direction = place.split()

		number = int(number)

		is_across = (direction.lower() == "a")
		row, col = self.parse_number(number, is_across)
		return row, col, is_across

	def submit_letter_exact(self, row, col, letter):
		if (letter == ' '):
			self.delete_letter_exact(row, col)
		elif row < self.height and col < self.width and self.grid[row][col].color != Cell.BLACK:
			old_letter = self.grid[row][col].content
			self.grid[row][col].content = letter
			if (old_letter != ' ' and old_letter != None):
				return

	def delete_letter_exact(self, row, col):
		if self.grid[row][col].color != Cell.BLACK:
			old_letter = self.grid[row][col]
			self.grid[row][col].content = None
			if (old_letter == ' ' or old_letter == None):
				return

	def submit_letter(self, row, col, offset, letter, is_across):
		if is_across:
			self.submit_letter_exact(row, col + offset - 1, letter)
		else:
			self.submit_letter_exact(row + offset - 1, col, letter)

	def delete_letter(self, row, col, offset, is_across):
		if is_across:
			self.submit_letter_exact(row, col + offset - 1, None)
		else:
			self.submit_letter_exact(row + offset - 1, col, None)

	def submit_word(self, row, col, word, is_across):
		for i in range(len(word)):

			if row >= self.height or col >= self.width or self.grid[row][col].color == Cell.BLACK:
				return 

			self.submit_letter_exact(row, col, word[i])
			if is_across:
				col += 1
			else:
				row += 1

	def delete_word(self, row, col, is_across):
		while row < self.height and col < self.width and self.grid[row][col].color != Cell.BLACK:
			self.delete_letter_exact(row, col)
			if is_across:
				col += 1
			else:
				row += 1

	def submit(self, submission_type, clue, solution = None, offset = None):
		try:
			row, col, is_across = self.parse_submission(clue)
		except Exception, e:
			return

		if row is None:
			return

		if submission_type == Submission.ADD_LETTER:
			self.submit_letter(row, col, offset, solution, is_across)
		if submission_type == Submission.ADD_WORD:
			self.submit_word(row, col, solution, is_across)
		if submission_type == Submission.DELETE_LETTER:
			self.delete_letter(row, col, offset, is_across)
		if submission_type == Submission.DELETE_WORD:
			self.delete_word(row, col, is_across)

	def check_solution(self):
		self.show_incorrect_cells = True

	def uncheck_solution(self):
		self.show_incorrect_cells = False