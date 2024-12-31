# Created: 10-10-2024
# Last updated: 12-13-2024
# Alexander Myska, Oliver Strauss, and Brandon Knautz

# This class will be used to make grids, this time by looking for words first

# External imports:
import copy
from math import floor
import random

# When running from here, use these imports:
from DataBaseConvert import findWord
from Grid import *
from Cell import *

# When running from main, use these imports:
# from BackEnd.DataBaseConvert import findWord
# from BackEnd.Grid import *
# from BackEnd.Cell import *

def generateBridge(size: int) -> tuple[Grid, str]:
    """
    Credit: Alexander Myska
    Generates a Grid with a bridge, guaranteeing that the entire
    Grid is connected.
    @param size: the size of Grid to create
    @return: the Grid created
    """

    # First, create the Grid and add partitions
    g = Grid(size)
    partitions = list()
    allEdges = g.getEdges(sort = False)

    # We need to add 2 partitions to the Grid
    while (len(partitions) < 2):
        # First, pick a random side, and a random index on that side
        randomSide = random.choice(allEdges)
        partitionIndex = random.randrange(3, size - 3)

        # Next, make the randomly chosen Cell into a BlockedCell
        partitionCell = randomSide[partitionIndex]
        g.addBlockedHere(partitionCell.x, partitionCell.y)

        # Remove this side so it is not chosen again
        allEdges.remove(randomSide)
        partitions.append(partitionCell)

    # After the partitions have been added, we need to identify the Grid's
    # shape, and generate a bridge accordingly.
    x1 = partitions[0].x
    y1 = partitions[0].y
    x2 = partitions[1].x
    y2 = partitions[1].y

    # This list will contain tuple with a number and boolean.
    # The boolean specifies if this bridge will be across or down; True is across, False is down.
    # The number specifies the coordinate where this bridge will be added.
    # For example, (4, False) means the bridge will be a vertical word starting at y = 4.
    validBridges = list()

    if ((x1 == 0 and x2 == g.size - 1) or (x2 == 0 and x1 == g.size - 1)): # H-Split
        # In the case of an H-Split, we should choose any row between:
        # 2 and size - 2
        for i in range(2, g.size - 2):
            validBridges.append((i, True, "HSPLIT"))

    elif ((y1 == 0 and y2 == g.size - 1) or (y2 == 0 and y1 == g.size - 1)): # V-Split
        # In the case of an V-Split, we should choose any column between:
        # 2 and size - 2
        for i in range(2, g.size - 2):
            validBridges.append((i, False, "VSPLIT"))

    elif ((x1 == 0 and y2 == g.size - 1) or (x2 == 0 and y1 == g.size - 1)): # 0-L
        # In the case of a 0-L, we can choose between the following:
        # Rows: 2 and size - x1/x2 - 1
        # Columns: y2/y1 + 1 and size - 2
        if (x1 == 0):
            for i in range(2, x2):
                validBridges.append((i, True, "0L"))

            for j in range(y1 + 1, g.size - 2):
                validBridges.append((j, False, "0L"))

        else:
            for i in range(2, x1):
                validBridges.append((i, True, "0L"))

            for j in range(y2 + 1, g.size - 2):
                validBridges.append((j, False, "0L"))

    elif ((x1 == 0 and y2 == 0) or (x2 == 0 and y1 == 0)): # 90-L
        # In the case of a 90-L, we can choose between the following:
        # Rows: 2 and x2/x1
        # Columns: 2 and y2/y1
        if (x1 == 0):
            for i in range(2, x2):
                validBridges.append((i, True, "90L"))

            for j in range(2, y1):
                validBridges.append((j, False, "90L"))

        else:
            for i in range(2, x1):
                validBridges.append((i, True, "90L"))

            for j in range(2, y2):
                validBridges.append((j, False, "90L"))

    elif ((y1 == 0 and x2 == g.size - 1) or (y2 == 0 and x1 == g.size - 1)): # 180-L
        # In the case of a 180-L, we can choose between the following:
        # Rows: x2/x1 + 1 and size - 2
        # Columns: 2 and size - y1/y2 - 1
        if (y1 == 0):
            for i in range(x1 + 1, g.size - 2):
                validBridges.append((i, True, "180L"))

            for j in range(2, y2):
                validBridges.append((j, False, "180L"))

        else:
            for i in range(x2 + 1, g.size - 2):
                validBridges.append((i, True, "180L"))

            for j in range(2, y1):
                validBridges.append((j, False, "180L"))

    elif ((y1 == g.size - 1 and x2 == g.size - 1) or (y2 == g.size - 1 and x1 == g.size - 1)): # 270-L
        # In the case of a 270-L, we can choose between the following:
        # Rows: x2/x1 + 1 and size - 2
        # Columns: y1/y2 + 1 and size - 2
        if (y1 == g.size - 1):
            for i in range(x1 + 1, g.size - 2):
                validBridges.append((i, True, "270L"))

            for j in range(y2 + 1, g.size - 2):
                validBridges.append((j, False, "270L"))

        else:
            for i in range(x2 + 1, g.size - 2):
                validBridges.append((i, True, "270L"))

            for j in range(y1 + 1, g.size - 2):
                validBridges.append((j, False, "270L"))

    else: # Something unexpected happened
        raise RuntimeError

    # Loops over the list of valid bridges and chooses one that could work
    randChoice = random.choice(validBridges)
    bridge = list()

    if (randChoice[1]): # The bridge is across
        for i in range(0, g.size):
            bridge.append(g.grid[randChoice[0]][i])

    else: # The bridge is down
        for j in range(0, g.size):
            bridge.append(g.grid[j][randChoice[0]])

    bridgeWord = getWord(bridge)

    ic = IndexCell(bridge[0].x, bridge[0].y)
    g.addIndexCell(ic)
    g.words.append(bridgeWord)
    bridge[0] = ic
    ic.setBody(bridge, bridgeWord)

    return g, randChoice[2]

def createEdgesNew(g: Grid, bridgeType: str) -> Grid:
    """
    Credit: Alexander Myska
    Adds words to the edges of the Grid.
    @param g: the original Grid to add words to
    @return: a modified Grid
    """
    edges = g.getEdges(sort = False)

    if (bridgeType == "HSPLIT"):
        newIndexCell(g, edges[4])
        edges[0][0] = edges[4][0]
        edges[1][0] = edges[4][-1]

        newIndexCell(g, edges[5])
        edges[2][-1] = edges[5][0]
        edges[3][-1] = edges[5][-1]

        newHybridCell(g, edges[0])
        edges[4][0] = edges[0][0]

        newIndexCell(g, edges[1])

        newIndexCell(g, edges[2])

        newIndexCell(g, edges[3])

    elif (bridgeType == "VSPLIT"):
        newIndexCell(g, edges[0])
        edges[2][0] = edges[0][0]
        edges[3][0] = edges[0][-1]

        newIndexCell(g, edges[1])
        edges[4][-1] = edges[1][0]
        edges[5][-1] = edges[1][-1]

        newHybridCell(g, edges[2])
        edges[0][0] = edges[2][0]

        newIndexCell(g, edges[3])

        newIndexCell(g, edges[4])

        newIndexCell(g, edges[5])

    elif (bridgeType == "270L"):
        newIndexCell(g, edges[1])
        edges[4][0] = edges[1][0]
        edges[3][0] = edges[1][-1]

        newHybridCell(g, edges[4])
        edges[1][0] = edges[4][0]
        edges[0][0] = edges[4][-1]

        newIndexCell(g, edges[0])

        newIndexCell(g, edges[2])
        edges[5][-1] = edges[2][-1]

        newIndexCell(g, edges[3])

        newIndexCell(g, edges[5])

    elif (bridgeType == "180L"):
        newIndexCell(g, edges[1])
        edges[3][0] = edges[1][0]
        edges[5][0] = edges[1][-1]

        newIndexCell(g, edges[5])
        edges[2][-1] = edges[5][-1]

        newIndexCell(g, edges[0])
        edges[4][-1] = edges[0][0]

        newIndexCell(g, edges[2])

        newHybridCell(g, edges[3])
        edges[1][0] = edges[3][0]

        newIndexCell(g, edges[4])

    elif (bridgeType == "90L"):
        newIndexCell(g, edges[2])
        edges[4][-1] = edges[2][0]
        edges[5][-1] = edges[2][-1]

        newIndexCell(g, edges[5])
        edges[1][-1] = edges[5][0]

        newIndexCell(g, edges[0])
        edges[3][0] = edges[0][0]

        newIndexCell(g, edges[1])

        newHybridCell(g, edges[3])
        edges[0][0] = edges[3][0]

        newIndexCell(g, edges[4])

    elif (bridgeType == "0L"):
        newIndexCell(g, edges[2])
        edges[4][-1] = edges[2][0]
        edges[5][-1] = edges[2][-1]

        newIndexCell(g, edges[4])
        edges[0][0] = edges[4][0]

        newHybridCell(g, edges[0])
        edges[0][0] = edges[4][0]

        newIndexCell(g, edges[1])
        edges[3][0] = edges[1][-1]

        newIndexCell(g, edges[3])

        newIndexCell(g, edges[5])

    else:
        raise ValueError("Invalid bridgeType")

    return g

def newIndexCell(g: Grid, thisWord: list[Cell]) -> None:
    """
    Adds an IndexCell to the Grid
    @param thisWord: the list of Cells
    """
    word = getWord(thisWord)
    if (word == ""):
        raise AttributeError(f"Edge not filled: Line 368")
    ic = IndexCell(thisWord[0].x, thisWord[0].y)
    g.addIndexCell(ic)
    g.words.append(word)
    thisWord[0] = ic
    ic.setBody(thisWord, word)

def newHybridCell(g: Grid, thisWord: list[Cell]) -> None:
    """
    Adds a HybridCell to Grid
    @param thisWord: the list of Cells
    """
    currentDir = thisWord[0].getDirection()
    hc = HybridCell(thisWord[0].x, thisWord[0].y)

    if (currentDir):  # True: word is across
        hc.across = thisWord[0]
        word = getWord(thisWord)
        if (word == ""):
            raise AttributeError(f"Edge not filled: Line 385")
        ic = IndexCell(thisWord[0].x, thisWord[0].y)
        g.addIndexCell(ic)
        g.words.append(word)
        thisWord[0] = ic
        ic.setBody(thisWord, word)
        hc.down = ic

    else:  # False: word is down
        hc.down = thisWord[0]
        word = getWord(thisWord)
        if (word == ""):
            raise AttributeError(f"Edge not filled: Line 395")
        ic = IndexCell(thisWord[0].x, thisWord[0].y)
        g.addIndexCell(ic)
        g.words.append(word)
        thisWord[0] = ic
        ic.setBody(thisWord, word)
        hc.across = ic

    hc.setLetter(thisWord[0].letter)

    thisWord[0] = hc

def fill(g: Grid, last: int) -> None:
    """
    Credit: Alexander Myska, Oliver Strauss, Brandon Knautz
    Fills in the Grid with words.
    @param g: the Grid to edit
    @param last: the number of letters previously filled in the Grid
    @return: the final, edited Grid
    """
    size = g.size
    wordSize = size - 2
    maxAllowed = 0

    cellsNeeded = floor(size**2 * 0.66)

    dupeList = g.indexCells.copy()

    while (wordSize > 2):

        while (len(dupeList) > 0 and maxAllowed < size - wordSize - 1):
            randomIndexCell = random.choice(dupeList)

            randomBody = randomIndexCell.body
            perpDir = not randomIndexCell.getDirection()
            for current in randomBody:
                if (isinstance(current, IndexCell)):
                    continue

                if (sizeCheck(g, current, perpDir, wordSize) and diagonalCheck(g, current, perpDir) and occupiedCheck(g, current, perpDir, wordSize) and lastLetterCheck(g, current, perpDir, wordSize) and perpendicularCheck(g, current, perpDir, wordSize)):
                    newWord = list()
                    if (perpDir): # True: word should go across
                        for i in range(0, wordSize):
                            newWord.append(g.grid[current.x][current.y + i])

                    else: # False: word should go down
                        for i in range(0, wordSize):
                            newWord.append(g.grid[current.x + i][current.y])

                    allowed = True
                    for cell in newWord:
                       if (g.getNumAdjacents(cell.x, cell.y) > 2):
                           allowed = False

                    # We need to add a check in case we need to make any Hybrid Cells
                    placeWord = getWord(newWord)
                    if (placeWord == "" or not allowed):
                        continue

                    ic = IndexCell(newWord[0].x, newWord[0].y)
                    g.addIndexCell(ic)
                    g.words.append(placeWord)
                    newWord[0] = ic
                    ic.setBody(newWord, placeWord)

                    maxAllowed += 1
                    break

            dupeList.remove(randomIndexCell)

        if (wordSize > 2):
            wordSize -= 1

        maxAllowed = 0
        dupeList = g.indexCells.copy()

    cellsFilled = 0
    for i in range(0, size):
        for j in range(0, size):
            if (g.grid[i][j].letter != ""):
                cellsFilled += 1

    if (cellsFilled < cellsNeeded):
        if (cellsFilled == last):
            raise RuntimeError("No new Cells created.")
        fill(g, cellsFilled)

def sizeCheck(g: Grid, cell: LetterCell, isAcross: bool, wordSize: int) -> bool:
    """
    # Credit: Alexander Myska, Oliver Strauss, and Brandon Knautz
    Checks if placing a word here would go out of the bounds of the Grid
    @param g: the Grid to use for this check
    @param cell: the Cell to start from
    @param isAcross: True if the direction is across, and False if the direction is Down
    @param wordSize: the size of the word trying to be added
    @return: True if this word could fit, and False otherwise
    """
    if (isAcross):
        return cell.y + wordSize - 1 < g.size
    else:
        return cell.x + wordSize - 1 < g.size

def diagonalCheck(g: Grid, c: LetterCell, isAcross: bool) -> bool:
    """
    # Credit: Alexander Myska, Oliver Strauss, and Brandon Knautz
    Checks the cells diagonal to the given LetterCell. If any of them have letters,
    we should not allow a word to be placed here. This is done to prevent "word blocks"
    @param g: the Grid to use for this check
    @param c: the Cell to start from
    @param isAcross: True if the direction is across, and False if the direction is Down
    @return: True if no cells diagonally have letters, and False otherwise
    """

    # Whether or not the cell is generating across or down, we always
    # need to check the cell down-right from c
    if ((c.x + 1 < g.size) and (c.y + 1 < g.size)):
        other = g.grid[c.x + 1][c.y + 1]
        if (isinstance(other, LetterCell) and other.letter != ""):
            return False

    if (isAcross): # True: do check for across
        if ((c.x - 1 >= 0) and (c.y + 1 < g.size)): # Cell up-right from c
            other = g.grid[c.x - 1][c.y + 1]
            if (isinstance(other, LetterCell) and other.letter != ""):
                return False
    else: # False: do check for down
        if ((c.x + 1 < g.size) and (c.y - 1 >= 0)):  # Cell down-left from c
            other = g.grid[c.x + 1][c.y - 1]
            if (isinstance(other, LetterCell) and other.letter != ""):
                return False

    return True

def occupiedCheck(g: Grid, cell: LetterCell, isAcross: bool, wordSize: int) -> bool:
    """
    # Credit: Alexander Myska
    Checks if two consecutive cells have a letter. If so, then a word is trying to
    be placed over an already existing word, which we should not allow.
    @param g: the Grid to use for this check
    @param cell: the Cell to start from
    @param isAcross: True if the direction is across, and False if the direction is Down
    @param wordSize: the size of the word trying to be added
    @return: True if no word already occupies this space, and False otherwise
    """
    if (isAcross): # True: do check for across
        for i in range(1, wordSize):
            if (g.grid[cell.x][cell.y + i - 1].letter != "" and g.grid[cell.x][cell.y + i].letter != ""):
                return False
    else: # False: do check for down
        for i in range(1, wordSize):
            if (g.grid[cell.x + i - 1][cell.y].letter != "" and g.grid[cell.x + i][cell.y].letter != ""):
                return False

    return True

def lastLetterCheck(g: Grid, cell: LetterCell, isAcross: bool, wordSize: int) -> bool:
    """
    # Credit: Alexander Myska and Brandon Knautz
    Checks is placing a word here would cause unintended intersection with another word.
    @param g: the Grid to use for this check
    @param cell: the Cell to start from
    @param isAcross: True if the direction is across, and False if the direction is Down
    @param wordSize: the size of the word trying to be added
    @return: True if no unintended intersections are created, and False otherwise
    """
    if (isAcross and cell.y + wordSize < g.size):
        if not (g.grid[cell.x][cell.y + wordSize].letter in ["*", ""]):
            return False
        if not (g.grid[cell.x - 1][cell.y + wordSize - 1].letter in ["*", ""]):
            return False
        if not (g.grid[cell.x + 1][cell.y + wordSize - 1].letter in ["*", ""]):
            return False

    elif (not isAcross and cell.x + wordSize < g.size):
        if not (g.grid[cell.x + wordSize][cell.y].letter in ["*", ""]):
            return False
        if not (g.grid[cell.x + wordSize - 1][cell.y + 1].letter in ["*", ""]):
            return False
        if not (g.grid[cell.x + wordSize - 1][cell.y - 1].letter in ["*", ""]):
            return False

    return True

def perpendicularCheck(g: Grid, cell: LetterCell, isAcross: bool, wordSize: int) -> bool:
    """
    # Credit: Alexander Myska
    Checks that every cell in this word's would-be body has either two empty neighbors or two named neighbors.
    A cell that has one of each should not be allowed, as doing so would create uninteded intersections.
    @param g: the Grid to use for this check
    @param cell: the Cell to start from
    @param isAcross: True if the direction is across, and False if the direction is Down
    @param wordSize: the size of the word trying to be added
    @return: True if no unintended intersections are created, and False otherwise
    """
    body = list()
    for i in range(0, wordSize):
        if (isAcross):
            body.append(g.grid[cell.x][cell.y + i])
        else:
            body.append(g.grid[cell.x + i][cell.y])

    if (isAcross):
        for eachCell in body:
            if ((g.grid[eachCell.x + 1][eachCell.y].letter != "" and g.grid[eachCell.x - 1][eachCell.y].letter == "")
                or (g.grid[eachCell.x - 1][eachCell.y].letter != "" and g.grid[eachCell.x + 1][eachCell.y].letter == "")):
                return False
    else:
        for eachCell in body:
            if ((g.grid[eachCell.x][eachCell.y + 1].letter != "" and g.grid[eachCell.x][eachCell.y - 1].letter == "")
                or (g.grid[eachCell.x][eachCell.y - 1].letter != "" and g.grid[eachCell.x][eachCell.y + 1].letter == "")):
                return False

    return True

def finalize(g: Grid) -> None:
    """
    Credit: Alexander Myska
    Finalizes the Grid by changing unnamed/empty LetterCells into BlockedCells.
    @param g: the Grid to edit
    @return:
    """
    for i in range(0, g.size):
        for j in range(0, g.size):
            if (g.grid[i][j].letter == ""):
                g.addBlockedHere(i, j)

def initGrid(size: int) -> Grid:
    """
    Initializes an entire Grid, and returns it to be used
    @param size: the size of the Grid to create
    @return: the created Grid
    """
    # First, we create the edges and bridge
    g, bridgeType = generateBridge(size)
    failedBridgeLimit = 40
    while True:
        try:
            g = createEdgesNew(g, bridgeType)
            # Second, we fill in the grid with words
            fill(g, 0)
            break
        except AttributeError: # If an edge cannot be properly filled, retry with the original Grid
            failedBridgeLimit -= 1
            if (failedBridgeLimit < 0): # If the Grid has failed to fill its edges properly too many times, restart
                failedBridgeLimit = 40
                g, bridgeType = generateBridge(size)
            continue
        except RuntimeError: # If the Grid cannot be properly filled in, restart
            failedBridgeLimit = 40
            g, bridgeType = generateBridge(size)
            continue

    # Lastly, we finalize the Grid by placing all the black spaces
    finalize(g)
    return g

def getWord(letterCells) -> str:
    """
    Credit: Alexander Myska
    @param letterCells: a list of LetterCells to find a word for
    @return: the word to place here, "" if no word is found
    """
    gotWords, found = findWord(letterCells)
    if (found):
        # If at least one word was found, return a random one
        return random.choice(gotWords)
    else: # Otherwise, return an empty string
        return ""

def main():
    g = initGrid(9)
    print(g)
    print(g.words)

if __name__ == "__main__":
    main()