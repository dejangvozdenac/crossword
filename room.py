from clue import Clue

class Room:
  def __init__(self, clues, state):
    self.clues = {}
    self.clues["across"] = [x for x in clues if x.direction == Clue.ACROSS]
    self.clues["down"]   = [x for x in clues if x.direction == Clue.DOWN]
    self.state = state