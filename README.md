# Crossword

## Future features:
1) highlight currently selected clue on the grid
2) ~~click on a square to mark it as a guess and to display it as a different color~~ (hold shift then click)
3) persistence (TODO by Jay, since it is closely related to rooms)
4) ~~rooms~~ (done)
5) rebus
6) ~~circles~~ (automatic)

## Notes
Without persistence, clues, checked, etc (variables which have to do with the state of a room) has been factored to a Room class. Now, the app holds a map of room names to Rooms in memory.

There exists 3 cases:
1. The room has never been joined before. "room_name" is not in "rooms".
  if room_name not in rooms:
    return redirect(url_for("join"))
2. The room has been joined, but there is no current puzzle. "room_name" is in "rooms", but the value of the key is True, not a Room.
3. The room has been joined and there is an ongoing puzzle.
