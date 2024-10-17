# 10-10-2024
# Alexander Myska, Oliver Strauss, Brandon Knautz
from operator import index
from random import Random

# This class will be used to make grids, this time by looking for words first

from Cell import *
from DataBaseConvert import findWord
from Grid import *
from display import *
import random

# Creates edges and a bridge for a grid, and returns the Grid
def createEdges(size: int) -> Grid:
    while True: # This will repeat until a valid grid is created
        g = Grid(size, size)
        partitions = 0
        allEdges = g.getEdges()

        while (partitions < 2):
            randomSide = random.choice(allEdges)
            partitionIndex = random.randrange(3, size - 3)
            partitionCell = randomSide[partitionIndex]
            g.addBlockedHere(partitionCell.x, partitionCell.y)
            allEdges.remove(randomSide)
            partitions += 1

        g = generateBridge(g)

        # Loop over the edges, give them words
            # allEdges needs to be re-declared because we have since edited the edges
        allEdges = g.getEdges()
        cellLists = list()
        for edge in allEdges:
            thisWord = list()
            for j in range(0, len(edge)):
                a = edge[j]
                if (j == 0):
                    thisWord.append(a)
                    continue

                b = edge[j - 1]

                # Converts the binary return value from compare to a string
                dist = a.compare(b)

                if (dist > 0b0111111): # The number differs by x
                    if (dist > 0b1011111): # The number also differs by y
                        continue
                    else: # Only the x-coordinates are different
                        if not (dist > 0b1000001):  # Distance is not greater than 1; continue with the current list
                            thisWord.append(a)
                        else: # Distance was greater than 1; new word starts here
                            cellLists.append(thisWord)
                            thisWord = list()
                            thisWord.append(a)

                elif (dist > 0b0011111): # The number differs by y only
                    if not (dist > 0b0100001): # Distance is not greater than 1; continue with the current list
                        thisWord.append(a)
                    else: # Distance was greater than 1; new word starts here
                        cellLists.append(thisWord)
                        thisWord = list()
                        thisWord.append(a)

                # In all other cases, the cells we compared were the same

            cellLists.append(thisWord)

        for thisWord in cellLists:
            for i in range(0, len(thisWord)):
                thisWord[i] = g.grid[thisWord[i].x][thisWord[i].y]

            word = getWord(thisWord)
            if not (isinstance(thisWord[0], IndexCell)):
                ic = IndexCell(thisWord[0].x, thisWord[0].y)
                g.addIndexCell(ic)
            else:
                ic = thisWord[0]
            thisWord[0] = ic
            ic.setBody(thisWord, word)

        return g

# Create a bridge, and give it a word
def generateBridge(g: Grid) -> Grid:
    bridge = list()

    allEdges = g.getEdges()
    bridgeSide = random.randrange(0, 2)
    opposite = 3 - bridgeSide

    evenIndices = list()
    for i in range(2, g.size - 2, 2):
        evenIndices.append(i)

    randNum = random.choice(evenIndices)

    if (bridgeSide == 0): # Look at columns
        while not ((g.grid[0][randNum] in allEdges[bridgeSide]) and (g.grid[g.size - 1][randNum] in allEdges[opposite])):
            evenIndices.remove(randNum)
            randNum = random.choice(evenIndices)
        for i in range(0, g.size):
            bridge.append(g.grid[i][randNum])

    else: # Look at rows
        while not ((g.grid[randNum][0] in allEdges[bridgeSide]) and (g.grid[randNum][g.size - 1] in allEdges[opposite])):
            evenIndices.remove(randNum)
            randNum = random.choice(evenIndices)
        for i in range(0, g.size):
            bridge.append(g.grid[randNum][i])

    bridgeWord = getWord(bridge)

    ic = IndexCell(bridge[0].x, bridge[0].y)
    g.addIndexCell(ic)
    bridge[0] = ic
    ic.setBody(bridge, bridgeWord)

    # =====================================================
    # DEBUGGING LINES
    # print(bridgeWord)
    # =====================================================

    return g

# Fills the rest of the Grid with words
def fill(grid: Grid) -> Grid:
    g = grid
    size = g.size
    wordSize = size - 2
    maxAllowed = 0
    indexCellList = g.indexCells
    """
    cellsFilled = 0
    for i in range(0, size):
        for j in range(0, size):
            if (g.grid[i][j].letter != ""):
                cellsFilled += 1
    """
    cellsNeeded = floor(size**2 * 0.50)

    dupeList = indexCellList.copy()

    while (wordSize > 2): # Loop until about 70% of the grid has letters

        while (len(dupeList) > 0 and maxAllowed < 2):
            randomIndexCell = random.choice(dupeList)
            randomBody = randomIndexCell.body
            randomDir = not randomIndexCell.getDirection()
            for current in randomBody:
                if (isinstance(current, IndexCell)):
                    continue

                if (diagonalCheck(g, current, randomDir) and sizeCheck(g, current, randomDir, wordSize) and lastLetterCheck(g, current, randomDir, wordSize + 1)):

                    # ====================================================
                    placeWord = getWord(randomBody)
                    ic = IndexCell(randomBody[0].x, randomBody[0].y)
                    g.addIndexCell(ic)
                    # print("IC added: {0}".format(ic)) # Debug line
                    randomBody[0] = ic
                    ic.setBody(randomBody, placeWord)
                    # This code needs to be changed in the following ways to make it functional:
                    # Because getWord() finds a word that works for the collection of cells
                    #   passed into it, we cannot pass in randomBody. Instead, we need to create
                    #   a whole new list of cells, starting at "current", and moving in the correct
                    #   direction until the list is of size wordSize.
                    #
                    # IndexCell(randomBody[0].x, randomBody[0].y) should be rewritten as
                    #   IndexCell(newList[0].x, newList[0].y), where newList is the list of
                    #   cells that correspond to where we are trying to place the word, like
                    #   I just talked about.
                    #
                    # newList[0] = ic
                    # setBody(newList, placeWord)
                    # ====================================================

                    maxAllowed += 1

            dupeList.remove(randomIndexCell)

        wordSize -= 1
        maxAllowed = 0
        dupeList = g.indexCells

        # Run diagonal check
            # Try to create a word of length wordSize, perpendicular to the bridge
        # Run diagonal check
            # Try to create a word of length wordSize, parallel to the bridge
        # If wordSize is > 3, wordSize -= 2
        # Minimum wordSize is 3

    # After all letters are in place, any Cell without a letter becomes a BlockedCell
    # Return the completed grid

    return g

# Checks a Cell diagonal to c
    # returns true if the Cell does not have a letter, and false otherwise
def diagonalCheck(g: Grid, c: Cell, isAcross: bool) -> bool:
    if ((c.x + 1 < g.size) and (c.y + 1 < g.size)):  # Cell down-right from c
        other = g.grid[c.x + 1][c.y + 1]
        if (other.letter != ""):
            return False

    if (isAcross): # True: do check for across
        if ((c.x - 1 >= 0) and (c.y + 1< g.size)): # Cell up-right from c
            other = g.grid[c.x - 1][c.y + 1]
            if (other.letter != ""):
                return False
    else: # False: do check for down
        if ((c.x + 1 < g.size) and (c.y - 1 >= 0)):  # Cell down-left from c
            other = g.grid[c.x + 1][c.y - 1]
            if (other.letter != ""):
                return False

    return True # Return True if all other checks pass

def sizeCheck(g: Grid, cell: LetterCell, isAcross: bool, wordSize: int)-> bool:
    if (isAcross):
        return cell.y + wordSize < g.size
    else:
        return cell.x + wordSize < g.size

def lastLetterCheck(g: Grid, cell: LetterCell, isAcross: bool, wordSize: int) -> bool:
    if (isAcross and cell.y + wordSize < g.size):
        if (isinstance(g.grid[cell.x][cell.y + wordSize], BlockedCell)):
            return True
        return g.grid[cell.x][cell.y + wordSize].letter == ""
    elif (cell.x + wordSize < g.size):
        if (isinstance(g.grid[cell.x + wordSize], BlockedCell)):
            return True
        return g.grid[cell.x + wordSize][cell.y].letter == ""
    else:
        return False

# Method that initializes a completed Grid (words, black spaces, word list)
def initGrid(size: int) -> Grid:
    g = createEdges(size)
    g = fill(g)
    for i in range(size):
        for j in range(size):
            if (isinstance(g.grid[i][j], IndexCell)):
                g.words.append(g.grid[i][j].word)
    return g

# Returns a word to be placed in a Grid
def getWord(letterCells) -> str:
    gotWords,found = findWord(letterCells)
    randIndex = random.randrange(0, len(gotWords))
    return gotWords[randIndex]

def main():
    initGrid(9)

if __name__ == "__main__":
    main()