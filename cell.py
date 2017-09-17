class Cell:
  # values that Cell.color can take:
  BLACK = "."
  WHITE = "-"
  WHITE_INCORRECT = "/"

  def __init__(self, x, y, variety, number=None, content=None, answer=None, circled=False, clue_across=None, clue_down=None):
    self.variety = variety
    self.number = number # the clue number of the cell, or None if cell is not numbered
    self.content = content # length 1 string
    self.answer = answer # length 1 string
    self.circled = circled # boolean
    self.coordinate = {}
    self.coordinate["X"] = x
    self.coordinate["Y"] = y
    self.clue_across = clue_across
    self.clue_down = clue_down