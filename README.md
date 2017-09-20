# Crossword
Hosted at: dejan-crossword.herokuapp.com

## Notes:
Without persistence, clues, checked, etc (variables which have to do with the state of a room) has been factored to a Room class. Now, the app holds a map of room names to Rooms in memory.

There exists 3 cases:
1. The room has never been joined before. "room_name" is not in "rooms".
  if room_name not in rooms:
    return redirect(url_for("join"))
2. The room has been joined, but there is no current puzzle. "room_name" is in "rooms", but the value of the key is True, not a Room.
3. The room has been joined and there is an ongoing puzzle.
