class Cell(db.Model):
  # values that Cell.color can take:
  BLACK = "."
  WHITE = "-"

  # SQLAlchemy
  id = db.Column(db.Integer, primary_key=True)
  variety = db.Column(db.String(10), nullable=False),
  number = db.Column(db.String(10), nullable=False),
  content = db.Column(db.String(1), nullable=False),
  answer = db.Column(db.String(1), nullable=False),

  def __init__(self, variety, number=None, content=None, answer=None, circled=False):
    self.variety = variety
    self.number = number # the clue number of the cell, or None if cell is not numbered
    self.content = content # length 1 string
    self.answer = answer # length 1 string
    self.circled = circled # boolean