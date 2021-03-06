class Cell:
  # values that Cell.color can take:
  BLACK = "."
  WHITE = "-"

  def __init__(self, x, y, color, number=None, content=None, answer=None, circled=False, clue_across=None, clue_down=None):
    self.color = color
    self.number = number # the clue number of the cell, or None if cell is not numbered
    self.content = content # length 1 string
    self.answer = answer # length 1 string
    self.circled = circled # boolean
    self.coordinate = {}
    self.coordinate["X"] = x
    self.coordinate["Y"] = y
    self.clue_across = clue_across
    self.clue_down = clue_down

  def is_correct(self):
    return self.content == self.answer