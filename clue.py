class Clue:
  # values that Clue.direction can take:
  ACROSS = True
  DOWN = False
  
  def __init__(self, number, across, question, answer, finished):
    self.number = number
    self.across = across
    self.question = question # string
    self.answer = answer # string
    self.finished = finished