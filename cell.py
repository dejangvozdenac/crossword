class Cell:
  # values that Cell.color can take:
  Cell.BLACK = False
  Cell.WHITE = True

  def __init__(self, variety, numbered, content, answer, circled):
    self.variety = variety
    self.numbered = numbered # boolean
    self.content = content # length 1 string
    self.answer = answer # length 1 string
    self.circled = circled # boolean