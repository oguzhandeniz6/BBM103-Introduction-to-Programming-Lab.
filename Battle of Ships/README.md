# Battle-of-Ships
Hacettepe BBM103 - Introduction to Programming Lab. Assignment 4

Battleship (also known as Battleships or Sea Battle) is a strategy-type guessing game for
two players. It is played on ruled grids (paper or board) on which each player’s fleet of
warships is marked. The locations of the fleets are concealed from the other player. Players
alternate turns calling “shots” at the other player’s ships, and the game’s objective is to destroy
the opposing player’s fleet.

The game is played in four grids of squares 10x10, two for each player. The individual
squares in the grids are identified by letter and number. On one grid, the player arranges
ships and records the shots by the opponent. On the other grid, the player records their shots.

Before play begins, each player secretly arranges the ships on their hidden grid. Each ship
occupies several consecutive squares on the grid, arranged either horizontally or vertically.
The type of ship determines the number of squares for each ship. The ships cannot overlap
(i.e., only one can occupy any given square in the grid). The types and numbers of ships
allowed are the same for each player. The ships should be hidden from the players’ sight, and
it is not allowed to see each other’s pieces. The game is a discovery game in which players
must discover their opponents’ positions.

After the ships have been positioned, the game proceeds in a series of rounds. In each
round, the current player announces a target square in the opponent's grid to shoot. The
computer announces whether or not the square is occupied by a ship, then marks the hit or
miss on the grid.

When all of the squares of a ship have been hit, the computer announces the sinking
of the Carrier, Submarine, Destroyer, Patrol Boat, or titular Battleship. If all a player's ships
have been sunk, the game is over, and their opponent wins. If all ships of both players are
sunk by the end of the round, the game is a draw. This means if Player1 bombed all ships
and Player1 has only 1 ship left you need to ask 1 more move, before prompting the final info.

In order to run, you need to locate input files in the same directory as .py file.

You can run it like this: python3 Assignment4.py Player1.txt Player2.txt Player1.in Player2.in
