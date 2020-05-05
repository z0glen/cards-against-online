<h1>Cards Against Online</h1>

An online player inspired by the Cards Against Humanity game.

<h2>Setup</h2>

- run `$ pip install -r requirements.txt` to install all requirements
- from the root directory, run `$ flask run` to start the test server

<h2>Design Notes</h2>

- Sign in required to play, only one active game at a time (for now)
- Players must provide a username and the predefined password to join
- Players can join in the middle of an active game, they will start in the next round and be at a disadvantage for points
- Game will end when a player reaches a defined maximum points, or when there are no active players
- The game must manually be started via a UI event, which will trigger the dealing of cards
- Instructions are always accessible via a UI event
- Each player will receive five red cards
- The order of players is randomly shuffled once for judging, a green card is chosen and the round begins
