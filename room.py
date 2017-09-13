class Room:
  def __init__(self, clues_across, clues_down, state, check):
    self.clues = {}
    self.clues["across"] = clues_across
    self.clues["down"] = clues_down
    self.state = state
    self.check = check
    self.check_displayed = True