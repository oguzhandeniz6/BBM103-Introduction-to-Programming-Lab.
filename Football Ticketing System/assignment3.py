import sys

def readFile(filename):
    with open(filename, mode="r", encoding="utf-8") as file:  # mode= Read, encoding= UTF-8 (for Turkish characters)
        lineList = file.read().splitlines()
    file.close()
    return lineList


def writeOutput(Str, output):
    print(Str)  # Print to console
    output.write(Str + "\n")  # Write to text file


def createCategory(std, categoryCode, dimension, output):
    dim = dimension.split("x")
    # 2D list comprehension for seats in category. Set empty with "X" by default.
    std[categoryCode] = [["X" for i in range(int(dim[0]))] for j in range(int(dim[1]))]
    # dictionary[categoryCode] = 2D list representation of category.
    seatSize = str(int(dim[0]) * int(dim[1]))
    writeOutput("The category 'category-" + categoryCode + "' having " + seatSize + " seats has been created", output)
    return std


def sellTicket(std, customer, output):
    code = customer[2].split("-")[1]  # Category Code: 1A, 2F, 6D etc...
    seats = customer[3:]  # Seats: B4, C9-12, A1 etc...

    price = "X"  # Set price
    if customer[1] == "full":
        price = "F"  # If full, price is F
    elif customer[1] == "student":
        price = "S"  # If student, price is S
    elif customer[1] == "season":
        price = "T"  # If season, price is T

    for seat in seats:  # For every seat that customer bought (1 or more)
        if seat.__contains__("-"):  # If "seat" contains an interval like C9-12
            interval = seat.split("-")
            letterCode, first, last = interval[0][0], int(interval[0][1:]), int(interval[1])  # Split to C, 9, 12

            if last >= len(std[code][ord(letterCode) - ord('A')]):  # If index error
                writeOutput("Error: The category '" + customer[2] + "' has less column than the specified index "
                            + seat + "!", output)
                continue

            valid = True  # Boolean control for occupied seats
            for i in range(first, last + 1):
                if std[code][ord(letterCode) - ord('A')][i] != "X":  # If a seat is occupied
                    valid = False
                    break
            if valid:  # Else, seats are empty
                for i in range(first, last + 1):
                    std[code][ord(letterCode) - ord('A')][i] = price  # Change "X" to "S", "F" or "T", depends on price
                writeOutput("Success: " + customer[0] + " has bought " + seat + " at category-" + code, output)
            else:  # If seat is taken
                writeOutput("Warning: The seats " + seat + " cannot be sold to " + customer[0] +
                            " due some of them have already been sold", output)

        else:  # Else, "seat" represents just one seat
            if int(seat[1:]) >= len(std[code][ord(seat[0]) - ord('A')]):  # If index error
                writeOutput("Error: The category '" + customer[2] + "' has less column than the specified index "
                            + seat + "!", output)
                continue

            if std[code][ord(seat[0]) - ord('A')][int(seat[1])] != "X":  # If a seat is occupied
                writeOutput("Warning: The seat " + seat + " cannot be sold to " + customer[0] +
                            " since it was already sold", output)
            else:
                std[code][ord(seat[0]) - ord('A')][int(seat[1])] = price  # Change "X" to price ("S","F" or "T")
                writeOutput("Success: " + customer[0] + " has bought " + seat + " at category-" + code, output)

    return std


def cancelTicket(std, infos, output):
    code = infos[0].split("-")[1]  # Category Code: 1A, 2F, 6D etc...
    seats = infos[1:]  # Seats: B4, C9-12, A1 etc...

    for seat in seats:  # For every seat that customer cancelled (1 or more)
        if seat.__contains__("-"):  # If seat contains an interval like C9-12
            interval = seat.split("-")
            letterCode, first, last = interval[0][0], int(interval[0][1:]), int(interval[1])  # Split to C, 9, 12

            if last >= len(std[code][ord(letterCode) - ord('A')]):  # If index error
                writeOutput("Error: The category 'category-" + infos[0] + "' has less column than the specified index "
                            + seat + "!", output)
                continue

            valid = True  # Boolean control for occupied seats
            for i in range(first, last + 1):
                if std[code][ord(letterCode) - ord('A')][i] == "X":  # If a seat is already empty
                    valid = False
                    break
            if valid:  # If seats are taken
                for i in range(first, last + 1):
                    std[code][ord(letterCode) - ord('A')][i] = "X"  # Change seat to "X" again, which is empty
                writeOutput("Success: The seat " + seat + " at '" + infos[0] +
                            "' has been canceled and now ready to sell again", output)
            else:  # Else, seat is empty
                writeOutput("Error: The seat " + seat + " at " + infos[0] +
                            " has already been free! Nothing to cancel", output)
        else:  # Else, "seat" represents just one seat
            if int(seat[1:]) >= len(std[code][ord(seat[0]) - ord('A')]):  # If index error
                writeOutput("Error: The category 'category-" + code + "' has less column than the specified index "
                            + seat + "!", output)
                continue

            if std[code][ord(seat[0]) - ord('A')][int(seat[1])] == "X":  # If a seat is already empty
                writeOutput("Error: The seat " + seat + " at '" + infos[0] +
                            "' has already been free! Nothing to cancel", output)
            else:
                std[code][ord(seat[0]) - ord('A')][int(seat[1])] = "X"  # Change seat to "X" again, which is empty
                writeOutput("Success: The seat " + seat + " at '" + infos[0] +
                            "' has been canceled and now ready to sell again", output)

    return std


def calculateBalance(std, categoryCode, output):
    category = std[categoryCode]  # Category Code: 1A, 2F, 6D etc...
    students, fulls, seasons = 0, 0, 0

    for row in category:
        for column in row:
            if column == "S":  # If student
                students += 1
            elif column == "F":  # Else if, full
                fulls += 1
            elif column == "T":  # Else if, season
                seasons += 1
    # Calculate revenue; 10 dollars for student, 20 dollars for full and 250 dollars for season
    revenue = (students * 10) + (fulls * 20) + (seasons * 250)
    headerLine = "category report of 'category-" + categoryCode + "'"
    writeOutput(headerLine, output)
    writeOutput("-" * len(headerLine), output)
    writeOutput("Sum of students = " + str(students) + ", Sum of full pay = " + str(fulls) + ", Sum of season ticket = "
                + str(seasons) + ", and Revenues = " + str(revenue) + " Dollars", output)


def showCategory(std, categoryCode, output):
    category = std[categoryCode].copy()  # Shallow copy of 2D category list
    category.reverse()  # Reverse it

    letIdx = 0
    writeOutput("Printing category layout of category-" + categoryCode + "\n", output)
    for row in category:
        letter = chr(ord('A') + len(category) - letIdx - 1)  # Find letter (C in C9) with ascii codes and indexes

        # In this part, I used a lot of *list (unpack list). It works with print() method and easier to read but
        # it does not work with file.write() method. So, I had to duplicate my code.
        print(letter + " ", end="")
        output.write(letter + " ")
        print(*row, sep="  ")
        for column in row:
            output.write(column + "  ")
        output.write("\n")
        letIdx += 1
    print("  ", end="")
    output.write("  ")
    if len(category[0]) > 10:  # For numbers below in chart
        print(*[i for i in range(10)], sep="  ", end=" ")
        print(*[i for i in range(10, len(category[0]))], sep=" ")
    else:
        print(*[i for i in range(len(category[0]))], sep=" ")
    for i in range(len(category[0])):
        if i < 9:
            output.write(str(i) + "  ")
        else:
            output.write(str(i) + " ")
    output.write("\n")


# Main starts here

operations = readFile(sys.argv[1])  # Read file to list
output = open("output.txt", mode="w")  # Write file to write

stadium = {}  # Stadium, as dictionary. Maps category codes to 2D category lists which represents seats

for operation in operations:
    op = operation.split(" ")

    if op[0] == "CREATECATEGORY":  # Create new category
        catCode = op[1].split("-")[1]
        if catCode in stadium:  # If exists
            writeOutput("Warning: Cannot create the category for the second time. The stadium "
                        "has already " + op[1], output)
        else:
            stadium = createCategory(stadium, catCode, op[2], output)
    elif op[0] == "SELLTICKET":  # Sell ticket
        catCode = op[3].split("-")[1]
        if catCode in stadium:
            stadium = sellTicket(stadium, op[1:], output)
        else:  # If there is no category with given code
            writeOutput("Warning: Tickets cannot be sold to the non-existing category. The stadium "
                        "does not have " + op[3] + ".", output)
    elif op[0] == "CANCELTICKET":  # Cancel ticket
        catCode = op[1].split("-")[1]
        if catCode in stadium:
            stadium = cancelTicket(stadium, op[1:], output)
        else:  # If there is no category with given code
            writeOutput("Warning: Tickets cannot be sold to the non-existing category. The stadium "
                        "does not have " + op[1] + ".", output)
    elif op[0] == "SHOWCATEGORY":  # Show Category
        catCode = op[1].split("-")[1]
        if catCode in stadium:
            showCategory(stadium, catCode, output)
        else:  # If there is no category with given code
            writeOutput("Warning: There is no category as " + op[1] + " in stadium. Category did not shown.", output)
    elif op[0] == "BALANCE":  # Print Balance
        catCode = op[1].split("-")[1]
        if catCode in stadium:
            calculateBalance(stadium, catCode, output)
        else:  # If there is no category with given code
            writeOutput("Warning: There is no category as " + op[1] + " in stadium. Balance did not calculated.",
                        output)
    else:  # If command is wrong
        writeOutput("Warning: Wrong command!", output)

output.close()
