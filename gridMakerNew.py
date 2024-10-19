# Created: 10-10-2024
# Last updated: 10-19-2024
# Alexander Myska, Oliver Strauss, and Brandon Knautz

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

            if (isinstance(thisWord[0], IndexCell)):
                currentDir = thisWord[0].getDirection()
                hc = HybridCell(thisWord[0].x, thisWord[0].y)
                if (currentDir): # True: word is across
                    hc.across = thisWord[0]
                    word = getWord(thisWord)
                    ic = IndexCell(thisWord[0].x, thisWord[0].y)
                    g.addIndexCell(hc)
                    thisWord[0] = ic
                    ic.setBody(thisWord, word)
                    hc.down = ic

                else: # False: word is down
                    hc.down = thisWord[0]
                    word = getWord(thisWord)
                    ic = IndexCell(thisWord[0].x, thisWord[0].y)
                    g.addIndexCell(hc.across)
                    thisWord[0] = ic
                    ic.setBody(thisWord, word)
                    hc.across = ic

                hc.setLetter(thisWord[0].letter)

            if not (isinstance(thisWord[0], IndexCell)):
                word = getWord(thisWord)
                ic = IndexCell(thisWord[0].x, thisWord[0].y)
                g.addIndexCell(ic)
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

    return g

# Fills the rest of the Grid with words
def fill(grid: Grid) -> Grid:
    g = grid
    size = g.size
    wordSize = size - 2
    maxAllowed = 0
    """
    cellsFilled = 0
    for i in range(0, size):
        for j in range(0, size):
            if (g.grid[i][j].letter != ""):
                cellsFilled += 1
    """
    cellsNeeded = floor(size**2 * 0.50)

    dupeList = g.indexCells.copy()

    while (wordSize > 2): # Loop until about 70% of the grid has letters

        while (len(dupeList) > 0 and maxAllowed < size - wordSize - 1):
            randomIndexCell = random.choice(dupeList)
            randomBody = randomIndexCell.body
            perpDir = not randomIndexCell.getDirection()
            for current in randomBody:
                if (isinstance(current, IndexCell)):
                    continue

                if (sizeCheck(g, current, perpDir, wordSize) and diagonalCheck(g, current, perpDir, wordSize) and lastLetterCheck(g, current, perpDir, wordSize)):
                    newWord = list()
                    if (perpDir): # True: word should go across
                        for i in range(0, wordSize):
                            newWord.append(g.grid[current.x][current.y + i])

                    else: # False: word should go down
                        for i in range(0, wordSize):
                            newWord.append(g.grid[current.x + i][current.y])

                    # We need to add a check in case we need to make any Hybrid Cells

                    placeWord = getWord(newWord)
                    if (placeWord == ""):
                        continue

                    ic = IndexCell(newWord[0].x, newWord[0].y)
                    g.addIndexCell(ic)
                    newWord[0] = ic
                    ic.setBody(newWord, placeWord)

                    maxAllowed += 1
                    break

            dupeList.remove(randomIndexCell)

        wordSize -= 1
        maxAllowed = 0
        dupeList = g.indexCells.copy()

    return g

# Checks a Cell diagonal to c
    # returns true if the Cell does not have a letter, and false otherwise
def diagonalCheck(g: Grid, c: LetterCell, isAcross: bool, wordSize: int) -> bool:
    if ((c.x + 1 < g.size) and (c.y + 1 < g.size)):  # Cell down-right from c
        other = g.grid[c.x + 1][c.y + 1]
        if (isinstance(other, LetterCell) and other.letter != ""):
            return False

    if (isAcross): # True: do check for across
        if ((c.x - 1 >= 0) and (c.y + 1< g.size)): # Cell up-right from c
            other = g.grid[c.x - 1][c.y + 1]
            if (isinstance(other, LetterCell) and other.letter != ""):
                return False
    else: # False: do check for down
        if ((c.x + 1 < g.size) and (c.y - 1 >= 0)):  # Cell down-left from c
            other = g.grid[c.x + 1][c.y - 1]
            if (isinstance(other, LetterCell) and other.letter != ""):
                return False

    return True # Return True if all other checks pass

def sizeCheck(g: Grid, cell: LetterCell, isAcross: bool, wordSize: int)-> bool:
    if (isAcross):
        return cell.y + wordSize - 1< g.size
    else:
        return cell.x + wordSize - 1< g.size

def lastLetterCheck(g: Grid, cell: LetterCell, isAcross: bool, wordSize: int) -> bool:
    if (isAcross and cell.y + wordSize < g.size):
        if not (g.grid[cell.x][cell.y + wordSize].letter in ["*", ""]):
            return False
        if not (g.grid[cell.x - 1][cell.y + wordSize - 1].letter in ["*", ""]):
            return False
        if not (g.grid[cell.x + 1][cell.y + wordSize - 1].letter in ["*", ""]):
            return False

    elif (cell.x + wordSize < g.size):
        if not (g.grid[cell.x + wordSize][cell.y].letter in ["*", ""]):
            return False
        if not (g.grid[cell.x + wordSize - 1][cell.y + 1].letter in ["*", ""]):
            return False
        if not (g.grid[cell.x + wordSize - 1][cell.y - 1].letter in ["*", ""]):
            return False

    return True

# Finalizes the grid by placing black spaces where no letters are placed
def finalize(g: Grid) -> Grid:
    for i in range(0, g.size):
        for j in range(0, g.size):
            if (g.grid[i][j].letter == ""):
                g.addBlockedHere(i, j)
    return g

# Method that initializes a completed Grid (words, black spaces, word list)
def initGrid(size: int) -> Grid:
    # First, we create the edges and bridge
    g = createEdges(size)

    # Second, we fill in the grid with words
    g = fill(g)
    for i in range(0, size): # These loops make sure all the IndexCells' words are in the Grid's wordList
        for j in range(0, size):
            if isinstance(g.grid[i][j], HybridCell):
                g.words.append(g.grid[i][j].across.word)
                g.words.append(g.grid[i][j].down.word)
            elif isinstance(g.grid[i][j], IndexCell):
                g.words.append(g.grid[i][j].word)

    # Lastly, we finalize the grid by placing all the black spaces
    g = finalize(g)
    return g

# Returns a word to be placed in a Grid
def getWord(letterCells) -> str:
    gotWords, found = findWord(letterCells)
    randIndex = random.randrange(0, len(gotWords))
    return gotWords[randIndex]

def main():
    initGrid(9)

if __name__ == "__main__":
    main()