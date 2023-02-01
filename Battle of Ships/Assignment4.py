import sys
from os import path


def readFile(filename):
    # Read file into list. "filename" is the name of file
    with open(filename, mode="r", encoding="utf-8") as file:  # Open file for reading
        lineList = file.read().splitlines()
    file.close()
    return lineList  # return a list that contains all lines individually


def createBoard(playertxt):
    # Simple matrix creation with given input. "playertxt" is a list, each element is a row information.
    returnBoard = []
    assert len(playertxt) == 10  # Game board is always 10x10
    for l in playertxt:
        sublist = l.split(";")
        assert len(sublist) == 10  # Game board is always 10x10
        returnBoard.append(sublist)
    return returnBoard


def controlShips(plships, shipCode, inp):
    # Keep track of ship status, "plships" is dictionary for status of player's ships.
    # "shipCode" is char, code of current ship. "inp" is list, input coords that players choice ("6,C")
    if shipCode != 'B' and shipCode != 'P':  # If ship is C, D or S (one per type)
        plships[shipCode] = plships[shipCode] - 1
    elif shipCode == 'B' or shipCode == 'P':  # If ship is B or P (multiple per type)
        control = inp[0] + "," + inp[1]
        for ship in plships[shipCode]:
            if control in ship:
                ship.remove(control)  # Remove corresponding index from ship (for example "6,C")
                break
    return plships  # return updated ship status dictionary for player


def playerTurn(inp, realBoard, shownBoard, letDict, ships):
    # For player to play his/her turn. "inp" is list, input coords that players choice ("6,C").
    # "realBoard" is matrix, keeps ship locations. "shownBoard" is matrix, keeps current game board.
    # "letDict" is dictionary, keeps valid letters for game board. "ships" is dictionary for status of player's ships.
    code = realBoard[int(inp[0]) - 1][letDict[inp[1]] - 1]  # Extract input location data from realBoard
    if code == '':  # If code is empty
        shownBoard[int(inp[0]) - 1][letDict[inp[1]] - 1] = 'O'  # It is a miss, place 'O' in shownBoard
    else:  # If code is not empty ('C' or 'B' or 'D' or 'S' or 'P')
        shownBoard[int(inp[0]) - 1][letDict[inp[1]] - 1] = 'X'  # It is a hit, place 'X' in shownBoard
        ships = controlShips(ships, code, inp)  # Keep track of ship status

    return shownBoard, ships  # return updated versions of shownBoard and ship status dictionary for player


def placeShips(optxt, plships):
    # For placing Battleships (B) and Patrol Boats (P) with given input, "OptionalPlayerX.txt"
    # "optxt" is list, "OptionalPlayerX.txt" seperated by lines. "plships" is dictionary for status of player's ships.
    for l in optxt:
        # used a lot of "temp"s, because I need to parse the given string and I couldn't came up with meaningful names.
        temp1 = l.split(":")  # temp1 = [code of ship (B1), placement of ship (6,B;right;)
        temp2 = temp1[1].split(";")  # temp2 = [first coords (6,B), extension direction (right)]
        temp3 = temp2[0].split(",")  # temp3 = [row (6), column (B)]
        shipCoords = [temp2[0]]  # shipCoords will hold coords of ship
        if l[0] == 'B':  # If ship is "Battleship" (B)
            for i in range(3):
                if temp2[1] == "right":  # If extension direction is right
                    temp3[1] = chr(ord(temp3[1]) + 1)  # Increase column value (letter 'B' to letter 'C') by one
                    shipCoords.append(temp3[0] + "," + temp3[1])
                elif temp2[1] == "down":  # If extension direction is down
                    temp3[0] = str(int(temp3[0]) + 1)  # Increase row value (digit '6' to digit '7') by one
                    shipCoords.append(temp3[0] + "," + temp3[1])
            plships['B'].append(shipCoords)  # append ship to player ships dictionary with calculated coords
        elif l[0] == 'P':  # If ship is "Patrol Boat" (P)
            if temp2[1] == "right":  # If extension direction is right
                temp3[1] = chr(ord(temp3[1]) + 1)  # Increase column value (letter 'B' to letter 'C') by one
                shipCoords.append(temp3[0] + "," + temp3[1])
            elif temp2[1] == "down":  # If extension direction is down
                temp3[0] = str(int(temp3[0]) + 1)  # Increase row value (digit '6' to digit '7') by one
                shipCoords.append(temp3[0] + "," + temp3[1])
            plships['P'].append(shipCoords)  # append ship to player ships dictionary with calculated coords

    return plships  # return updated ship status dictionary for player


def printShips(shipDict, ships1, ships2, output):
    # Print status of ships into .out file. "shipDict" is dictionary, for code => ship name mapping. (B = Battleship)
    # "ships1" is dictionary for status of player1's ships, "ships2" is same but for player2. "output" is for write.
    for key in shipDict:
        if key != 'B' and key != 'P':  # If ship is Carrier, Destroyer or Submarine (one ship per type)
            status1 = 'X' if ships1[key] == 0 else '-'  # Player1's ship status
            status2 = 'X' if ships2[key] == 0 else '-'  # Player2's ship status
            output.write(
                '{:<12}'.format(shipDict[key]) + status1 + ("\t" * 4) + '{:<12}'.format(shipDict[key]) + status2 + "\n")
        elif key == 'B':  # If ship is Battleship
            status1 = 'X' if ships1[key].count([]) > 0 else '-'  # Player1's Battleship 1 status (not in order)
            status2 = 'X' if ships1[key].count([]) > 1 else '-'  # Player1's Battleship 2 status (not in order)
            output.write('{:<12}'.format(shipDict[key]) + status1 + " " + status2 + " \t\t\t")
            status1 = 'X' if ships2[key].count([]) > 0 else '-'  # Player2's Battleship 1 status (not in order)
            status2 = 'X' if ships2[key].count([]) > 1 else '-'  # Player2's Battleship 2 status (not in order)
            output.write('{:<12}'.format(shipDict[key]) + status1 + " " + status2 + "\n")
        elif key == 'P':  # If ship is Patrol Boat
            status1 = 'X' if ships1[key].count([]) > 0 else '-'  # Player1's Patrol Boat 1 status (not in order)
            status2 = 'X' if ships1[key].count([]) > 1 else '-'  # Player1's Patrol Boat 2 status (not in order)
            status3 = 'X' if ships1[key].count([]) > 2 else '-'  # Player1's Patrol Boat 3 status (not in order)
            status4 = 'X' if ships1[key].count([]) > 3 else '-'  # Player1's Patrol Boat 4 status (not in order)
            output.write(
                '{:<12}'.format(shipDict[key]) + status1 + " " + status2 + " " + status3 + " " + status4 + " \t\t")
            status1 = 'X' if ships2[key].count([]) > 0 else '-'  # Player2's Patrol Boat 1 status (not in order)
            status2 = 'X' if ships2[key].count([]) > 1 else '-'  # Player2's Patrol Boat 2 status (not in order)
            status3 = 'X' if ships2[key].count([]) > 2 else '-'  # Player2's Patrol Boat 3 status (not in order)
            status4 = 'X' if ships2[key].count([]) > 3 else '-'  # Player2's Patrol Boat 4 status (not in order)
            output.write(
                '{:<12}'.format(shipDict[key]) + status1 + " " + status2 + " " + status3 + " " + status4 + "\n")


def printRound(player, inp, shown1, shown2, ships1, ships2, shipDict, rnds, output):
    # Print current round informations. "player" is string.  "inp" is list, input coords that players choice ("6,C").
    # "shown1" is matrix, current Player1's board which shown to Player2. "shown2" is same but Player2's board.
    # "ships1" is dictionary for status of player1's ships, "ships2" is same but for player2. "output" is for write.
    # "shipDict" is dictionary for name of ships, 'B' for Battleship. "rnds" is current round number.
    output.write("\n" + player + "'s Move\n\nRound : " + str(rnds) + ("\t" * 5) + "Grid Size: 10x10\n\n")
    output.write("Player1’s Hidden Board		Player2’s Hidden Board \n"
                 "  A B C D E F G H I J		  A B C D E F G H I J\n")
    # Write current board into output file.
    for row in range(10):
        number = '{:<2}'.format(str(row + 1))
        output.write(number)
        for col in range(10):
            output.write(shown1[row][col] + " ")
        output.write("\t\t" + number)
        for col in range(10):
            output.write(shown2[row][col] + " ")
        output.write("\n")

    output.write("\n")
    # Call printShips function, for printing current ship status.
    printShips(shipDict, ships1, ships2, output)

    output.write("\nEnter your move: " + inp[0] + "," + inp[1] + "\n")


def endControl(ships):
    # Check if game is over. "ships" is dictionary for status of player's ships.
    for key in ships:
        if key != 'B' and key != 'P':  # If Carrier or Destroyer or Submarine
            if ships[key] > 0:  # If it didn't sink: number of shipCodes (C, D, S) > 0
                return False  # Game is not over
        else:  # Else, Battleship or Patrol Boat
            if ships[key].count([]) != len(ships[key]):  # If it didn't sink: number of non-empty lists > 0
                return False  # Game is not over
    return True  # Game Over


def printFinal(player, real1, real2, shown1, shown2, ships1, ships2, shipDict, output):
    # Print the final version of game when game is over. "shipDict" is dictionary for ship names. "output" is for write.
    # "real1" is matrix, keeps ship locations of Player1. "real2" is same but for Player2.
    # "shown1" is matrix, current Player1's board which shown to Player2. "shown2" is same but Player2's board.
    # "ships1" is dictionary for status of player1's ships, "ships2" is same but for player2. "output" is for write.
    output.write("\n" + player + "\n\nFinal Information\n\n"
                                 "Player1’s Board				Player2’s Board\n  A B C D E F G H I J		  A B C D E F G H I J\n")
    # Write combined board into output file. Show ship parts which didn't shot.
    for row in range(10):
        number = '{:<2}'.format(str(row + 1))
        output.write(number)
        # for Player1
        for col in range(10):
            if shown1[row][col] == "-" and real1[row][col] != "":  # If ship part is didn't shot.
                output.write(real1[row][col] + " ")  # Print from realBoard
            else:  # Else (did shot or miss)
                output.write(shown1[row][col] + " ")  # Print from shownBoard
        output.write("\t\t" + number)
        # for Player2
        for col in range(10):
            if shown2[row][col] == "-" and real2[row][col] != "":  # If ship part is didn't shot.
                output.write(real2[row][col] + " ")  # Print from realBoard
            else:  # Else (did shot or miss)
                output.write(shown2[row][col] + " ")  # Print from shownBoard
        output.write("\n")

    output.write("\n")
    # Call printShips function, for printing current ship status.
    printShips(shipDict, ships1, ships2, output)


def controlInput(inp, letDict):
    # Control the validity of the input. # "inp" is list, input coords that players choice ("6,C").
    # "letDict" is dictionary, keeps valid letters for game board.
    if inp[0] == "" or inp[1] == "" or len(inp) > 2:  # Check for Index Error: "6," or ",A" or "6,A,5"
        raise IndexError
    if not inp[1].isalpha() or not inp[0].isdigit():  # Check for Value Error: "A,A" or "6,6" or "A,6" or "A6,6"
        raise ValueError
    assert 1 <= int(inp[0]) < 11 and inp[1] in letDict  # Check for Assertion Error: "6,K" or "11,A" (Game Rule)


#                       --------------------MAIN--------------------

outputFile = open("../../Desktop/Battleship.out", mode="w", encoding="UTF-8")  # Open file to write

# letterDict is valid letters for game board and their order. shipsDict is ship names with their initials as keys.
letterDict = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9, 'J': 10}
shipsDict = {'C': 'Carrier', 'B': 'Battleship', 'D': 'Destroyer', 'S': 'Submarine', 'P': 'Patrol Boat'}
fileNames = []

try:
    fileNames = [sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], "OptionalPlayer1.txt", "OptionalPlayer2.txt"]
    # read board files. p1txt is for "Player1.txt", p2txt is for "Player2.txt".
    p1txt = readFile(fileNames[0])
    p2txt = readFile(fileNames[1])
    # read player input files. p1in is for "Player1.in", p2in is for "Player2.in".
    p1in = readFile(fileNames[2])
    p2in = readFile(fileNames[3])
    # read optional files. p1op is for "OptionalPlayer1.txt", p2op is for "OptionalPlayer2.txt".
    p1op = readFile(fileNames[4])
    p2op = readFile(fileNames[5])
    # Create game boards for players. p1board is Player1's game board, p2board is Player2's game board.
    p1board = createBoard(p1txt)
    p2board = createBoard(p2txt)
    # Made a list that contains every input as seperate elements.
    p1inputs = p1in[0].split(";")
    p1inputs = p1inputs[: -1]
    p2inputs = p2in[0].split(";")
    p2inputs = p2inputs[: -1]
    # Create shown boards. p1boardtop2 is Player1's current board which shown to Player2. p2boardtop1 is exact opposite.
    p1boardtop2 = [["-" for j in range(10)] for i in range(10)]
    p2boardtop1 = [["-" for j in range(10)] for i in range(10)]
    # Create ship status dictionaries. p1ships is for Player1, p2ships is for Player2.
    p1ships = {"C": 5, "D": 3, "S": 3, "B": [], "P": []}
    p2ships = {"C": 5, "D": 3, "S": 3, "B": [], "P": []}
    # Place Battleships and Patrol Boats with given Optional File.
    p1ships = placeShips(p1op, p1ships)
    p2ships = placeShips(p2op, p2ships)

    outputFile.write("Battle of Ships Game\n")  # Title
    rounds = 1  # Keep track of round numbers

    #              -----------------MAIN GAME LOOP-----------------
    while len(p1inputs) > 0 or len(p2inputs) > 0:  # While Player's still has moves
        if len(p1inputs) > 0:  # If Player1 still has move
            while True:  # Search until a valid input is found.
                inp = p1inputs[0].split(',')  # Split "6,C" to ["6","C"]
                try:
                    controlInput(inp, letterDict)  # Check input validity, this function can raise Exceptions
                    break  # If no exception has been raised, input is valid. Stop searching for new input.
                except IndexError:
                    outputFile.write("\nIndexError: Wrong type of input '" + p1inputs[0] + "' for Player1.\n")
                except ValueError:
                    outputFile.write("\nValueError: Wrong type of input '" + p1inputs[0] + "' for Player1.\n")
                except AssertionError:
                    outputFile.write("\nAssertionError: Invalid Operation '" + p1inputs[0] + "' for Player1.\n")
                finally:
                    p1inputs.pop(0)  # pop first element whether exception is raised or not, this input is read.
            # First, print current round informations, then Player 1 plays his/her move.
            printRound("Player1", inp, p1boardtop2, p2boardtop1, p1ships, p2ships, shipsDict, rounds, outputFile)
            p2boardtop1, p2ships = playerTurn(inp, p2board, p2boardtop1, letterDict, p2ships)

        if len(p2inputs) > 0:  # If Player1 still has move
            while True:  # Search until a valid input is found.
                inp = p2inputs[0].split(',')  # Split "6,C" to ["6","C"]
                try:
                    controlInput(inp, letterDict)  # Check input validity, this function can raise Exceptions
                    break  # If no exception has been raised, input is valid. Stop searching for new input.
                except IndexError:
                    outputFile.write("\nIndexError: Wrong type of input '" + p2inputs[0] + "' for Player2.\n")
                except ValueError:
                    outputFile.write("\nValueError: Wrong type of input '" + p2inputs[0] + "' for Player2.\n")
                except AssertionError:
                    outputFile.write("\nAssertionError: Invalid Operation '" + p2inputs[0] + "' for Player2.\n")
                finally:
                    p2inputs.pop(0)  # pop first element whether exception is raised or not, this input is read.
            # First, print current round informations, then Player 2 plays his/her move.
            printRound("Player2", inp, p1boardtop2, p2boardtop1, p1ships, p2ships, shipsDict, rounds, outputFile)
            p1boardtop2, p1ships = playerTurn(inp, p1board, p1boardtop2, letterDict, p1ships)
        # Check if game is over or not
        control1 = endControl(p2ships)
        control2 = endControl(p1ships)

        if control1 and control2:
            printFinal("It is a Draw!", p1board, p2board, p1boardtop2, p2boardtop1, p1ships, p2ships, shipsDict,
                       outputFile)
            break
        elif control1:
            printFinal("Player1 Wins!", p1board, p2board, p1boardtop2, p2boardtop1, p1ships, p2ships, shipsDict,
                       outputFile)
            break
        elif control2:
            printFinal("Player2 Wins!", p1board, p2board, p1boardtop2, p2boardtop1, p1ships, p2ships, shipsDict,
                       outputFile)
            break
        rounds += 1

except IndexError:  # If some argument(s) is/are missing
    outputFile.write("IndexError: number of input files less than expected.")
except IOError:  # If the file could not be opened
    notExist = []  # File(s) names that could not be opened

    for file in fileNames:
        if not path.exists(file):  # If path doesn't exist
            notExist.append(file)

    outputFile.write("IOError: input file(s) ")
    for file in notExist:
        outputFile.write(file + " ")
    outputFile.write("is/are not reachable.")
except Exception:  # Any other exception
    outputFile.write("kaBOOM: run for your life!")
finally:
    outputFile.close()  # Close output file, whether there is and exception or not. script is over.
