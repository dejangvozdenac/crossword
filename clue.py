from cell import Cell

class Clue:
  # values that Clue.direction can take:
  ACROSS = True
  DOWN = False
  
  def __init__(self, number, direction, question, answer):
    self.number = number
    self.direction = direction
    self.question = question # string
    self.answer = answer # string
    self.cells = [] # a list of Cell objects that the clue contains

  def finished(self):
  	for cell in self.cells:
  		if cell.content == None:
  			return False
  	return True