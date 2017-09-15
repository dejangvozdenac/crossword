class Cell:
  # values that Cell.color can take:
  BLACK = "."
  WHITE = "-"

  def __init__(self, variety, number=None, content=None, answer=None, circled=False):
    self.variety = variety
    self.number = number # the clue number of the cell, or None if cell is not numbered
    self.content = content # length 1 string
    self.answer = answer # length 1 string
    self.circled = circled # boolean