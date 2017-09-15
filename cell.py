class Cell:
  # values that Cell.color can take:
  BLACK = False
  WHITE = True

  def __init__(self, variety, number, content, answer, circled):
    self.variety = variety
    self.number = number # the clue number of the cell, or None if cell is not numbered
    self.content = content # length 1 string
    self.answer = answer # length 1 string
    self.circled = circled # boolean