# Crossword

## Future features:
#### TODO
1) highlight currently selected clue on the grid
2) refactor the js
3) tabbing over to select next clue
4) rebus


#### In Progress
1) click on a square to mark it as a guess and to display it as a different color (hold shift then click) -- works but does not send it back to the server
2) persistence (TODO by Jay, since it is closely related to rooms)

#### Done
1) ~~circles~~ (automatic)
2) ~~rooms~~
3) ~refactor index.html~
4) ~redesign data structures~
5) ~when you highlight a clue it comes up in the special clue box at the top so you don't have to look for it~

## Notes:
Without persistence, clues, checked, etc (variables which have to do with the state of a room) has been factored to a Room class. Now, the app holds a map of room names to Rooms in memory.

There exists 3 cases:
1. The room has never been joined before. "room_name" is not in "rooms".
  if room_name not in rooms:
    return redirect(url_for("join"))
2. The room has been joined, but there is no current puzzle. "room_name" is in "rooms", but the value of the key is True, not a Room.
3. The room has been joined and there is an ongoing puzzle.
