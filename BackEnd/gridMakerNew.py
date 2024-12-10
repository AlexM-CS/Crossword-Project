# Created: 10-10-2024
# Last updated: 11-19-2024
# Alexander Myska, Oliver Strauss, and Brandon Knautz
import sys
from random import Random
from typing import Any, Tuple, Dict, List
from xmlrpc.client import Binary

from flask import json
from OpenAITest import *

# This class will be used to make grids, this time by looking for words first

from BackEnd.DataBaseConvert import findWord
from BackEnd.Grid import Grid
from BackEnd.display import *
import random

from OpenAITest.OpenAI_hint_retrival import get_hints


# Creates edges and a bridge for a grid, and returns the Grid
def createEdges(size: int) -> Grid:
    while True:  # This will repeat until a valid grid is created
        global blockedCells
        g = Grid(size, size)
        partitions = list()
        allEdges = g.getEdges()

        while (len(partitions) < 2):
            randomSide = random.choice(allEdges)
            partitionIndex = random.randrange(3, size - 3)
            partitionCell = randomSide[partitionIndex]
            g.addBlockedHere(partitionCell.x, partitionCell.y)
            g.blockedCells.append([partitionCell.x, partitionCell.y])
            allEdges.remove(randomSide)
            partitions.append(partitionCell)

        g = generateBridge(g, partitions)

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

                if (dist > 0b0111111):  # The number differs by x
                    if (dist > 0b1011111):  # The number also differs by y
                        continue
                    else:  # Only the x-coordinates are different
                        if not (dist > 0b1000001):  # Distance is not greater than 1; continue with the current list
                            thisWord.append(a)
                        else:  # Distance was greater than 1; new word starts here
                            cellLists.append(thisWord)
                            thisWord = list()
                            thisWord.append(a)

                elif (dist > 0b0011111):  # The number differs by y only
                    if not (dist > 0b0100001):  # Distance is not greater than 1; continue with the current list
                        thisWord.append(a)
                    else:  # Distance was greater than 1; new word starts here
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
                if (currentDir):  # True: word is across
                    hc.across = thisWord[0]
                    word = getWord(thisWord)
                    ic = IndexCell(thisWord[0].x, thisWord[0].y)
                    g.addIndexCell(hc)
                    thisWord[0] = ic
                    ic.setBody(thisWord, word)
                    hc.down = ic

                else:  # False: word is down
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


# New way to generate bridges that guarantees the whole grid is connected
def generateBridge(g: Grid, partitions: list[Cell]) -> Grid:
    x1 = partitions[0].x
    y1 = partitions[0].y
    x2 = partitions[1].x
    y2 = partitions[1].y

    validBridges = list()

    if ((x1 == 0 and x2 == g.size - 1) or (x2 == 0 and x1 == g.size - 1)):  # H-Split
        # In the case of an H-Split, we should choose any row between:
        # 2 and size - 2
        for i in range(2, g.size - 2):
            validBridges.append((i, True))

    elif ((y1 == 0 and y2 == g.size - 1) or (y2 == 0 and y1 == g.size - 1)):  # V-Split
        # In the case of an V-Split, we should choose any column between:
        # 2 and size - 2
        for i in range(2, g.size - 2):
            validBridges.append((i, False))

    elif ((x1 == 0 and y2 == 0) or (x2 == 0 and y1 == 0)):  # 270-L
        # In the case of a 270-L, we can choose between the following:
        # Rows: 2 and x2/x1
        # Columns: 2 and y2/y1
        if (x1 == 0):
            for i in range(2, x2):
                validBridges.append((i, True))

            for j in range(2, y1):
                validBridges.append((j, False))

        else:
            for i in range(2, x1):
                validBridges.append((i, True))

            for j in range(2, y2):
                validBridges.append((j, False))

    elif ((x1 == 0 and y2 == g.size - 1) or (x2 == 0 and y1 == g.size - 1)):  # 180-L
        # In the case of a 180-L, we can choose between the following:
        # Rows: 2 and size - x1/x2 - 1
        # Columns: y2/y1 + 1 and size - 2
        if (x1 == 0):
            for i in range(2, x2):
                validBridges.append((i, True))

            for j in range(y1 + 1, g.size - 2):
                validBridges.append((j, False))

        else:
            for i in range(2, x1):
                validBridges.append((i, True))

            for j in range(y2 + 1, g.size - 2):
                validBridges.append((j, False))

    elif ((y1 == g.size - 1 and x2 == g.size - 1) or (y2 == g.size - 1 and x1 == g.size - 1)):  # 90-L
        # In the case of a 90-L, we can choose between the following:
        # Rows: x2/x1 + 1 and size - 2
        # Columns: y1/y2 + 1 and size - 2
        if (y1 == g.size - 1):
            for i in range(x1 + 1, g.size - 2):
                validBridges.append((i, True))

            for j in range(y2 + 1, g.size - 2):
                validBridges.append((j, False))

        else:
            for i in range(x2 + 1, g.size - 2):
                validBridges.append((i, True))

            for j in range(y1 + 1, g.size - 2):
                validBridges.append((j, False))

    elif ((y1 == 0 and x2 == g.size - 1) or (y2 == 0 and x1 == g.size - 1)):  # 0-L
        # In the case of a 90-L, we can choose between the following:
        # Rows: x2/x1 + 1 and size - 2
        # Columns: 2 and size - y1/y2 - 1
        if (y1 == 0):
            for i in range(x1 + 1, g.size - 2):
                validBridges.append((i, True))

            for j in range(2, y2):
                validBridges.append((j, False))

        else:
            for i in range(x2 + 1, g.size - 2):
                validBridges.append((i, True))

            for j in range(2, y1):
                validBridges.append((j, False))

    else:  # Something unexpected happened
        raise RuntimeError

    # Loops over the list of valid bridges and chooses one that could work
    randChoice = random.choice(validBridges)
    bridge = list()
    if (randChoice[1]):  # The bridge is across
        for i in range(0, g.size):
            bridge.append(g.grid[randChoice[0]][i])

    else:  # The bridge is down
        for j in range(0, g.size):
            bridge.append(g.grid[j][randChoice[0]])

    bridgeWord = getWord(bridge)

    ic = IndexCell(bridge[0].x, bridge[0].y)
    g.addIndexCell(ic)
    bridge[0] = ic
    ic.setBody(bridge, bridgeWord)

    return g


# Fills the rest of the Grid with words
def fill(grid: Grid, last: int) -> Grid:
    g = grid
    size = g.size
    wordSize = size - 2
    maxAllowed = 0

    cellsNeeded = floor(size ** 2 * 0.66)

    dupeList = g.indexCells.copy()

    while (wordSize > 2):

        while (len(dupeList) > 0 and maxAllowed < size - wordSize - 1):
            randomIndexCell = random.choice(dupeList)
            randomBody = randomIndexCell.body
            perpDir = not randomIndexCell.getDirection()
            for current in randomBody:
                if (isinstance(current, IndexCell)):
                    continue

                if (sizeCheck(g, current, perpDir, wordSize) and diagonalCheck(g, current, perpDir) and lastLetterCheck(
                        g, current, perpDir, wordSize) and occupiedCheck(g, current, perpDir, wordSize)):
                    newWord = list()
                    if (perpDir):  # True: word should go across
                        for i in range(0, wordSize):
                            newWord.append(g.grid[current.x][current.y + i])

                    else:  # False: word should go down
                        for i in range(0, wordSize):
                            newWord.append(g.grid[current.x + i][current.y])

                    allowed = True
                    for cell in newWord:
                        if (g.getNumNeighbors(cell.x, cell.y) > 2):
                            allowed = False

                    # We need to add a check in case we need to make any Hybrid Cells
                    placeWord = getWord(newWord)
                    if (placeWord == "" or not allowed):
                        continue

                    ic = IndexCell(newWord[0].x, newWord[0].y)
                    g.addIndexCell(ic)
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
            raise RuntimeError
        g = fill(g, cellsFilled)

    return g


# Checks a Cell diagonal to c
# returns true if the Cell does not have a letter, and false otherwise
def diagonalCheck(g: Grid, c: LetterCell, isAcross: bool) -> bool:
    if ((c.x + 1 < g.size) and (c.y + 1 < g.size)):  # Cell down-right from c
        other = g.grid[c.x + 1][c.y + 1]
        if (isinstance(other, LetterCell) and other.letter != ""):
            return False

    if (isAcross):  # True: do check for across
        if ((c.x - 1 >= 0) and (c.y + 1 < g.size)):  # Cell up-right from c
            other = g.grid[c.x - 1][c.y + 1]
            if (isinstance(other, LetterCell) and other.letter != ""):
                return False
    else:  # False: do check for down
        if ((c.x + 1 < g.size) and (c.y - 1 >= 0)):  # Cell down-left from c
            other = g.grid[c.x + 1][c.y - 1]
            if (isinstance(other, LetterCell) and other.letter != ""):
                return False

    return True  # Return True if all other checks pass


def sizeCheck(g: Grid, cell: LetterCell, isAcross: bool, wordSize: int) -> bool:
    if (isAcross):
        return cell.y + wordSize - 1 < g.size
    else:
        return cell.x + wordSize - 1 < g.size


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


def occupiedCheck(g: Grid, cell: LetterCell, isAcross: bool, wordSize: int) -> bool:
    currentCell = cell

    if (isAcross):
        for i in range(1, wordSize):
            if (g.grid[currentCell.x][currentCell.y + i - 1].letter != "" and g.grid[currentCell.x][
                currentCell.y + i].letter != ""):
                return False
    else:
        for i in range(1, wordSize):
            if (g.grid[currentCell.x + i - 1][currentCell.y].letter != "" and g.grid[currentCell.x + i][
                currentCell.y].letter != ""):
                return False

    return True


# Finalizes the grid by placing black spaces where no letters are placed
# also returns array of blocked cells to be used in front end
def finalize(g: Grid) -> Grid:
    for i in range(0, g.size):
        for j in range(0, g.size):
            if (g.grid[i][j].letter == ""):
                g.blockedCells.append([i, j])
                g.addBlockedHere(i, j)
    return g


# Method that initializes a completed Grid (words, black spaces, word list)

def initGrid(size: int) -> tuple[Any, dict[str, list[dict[str, Any]]], list[str]]:
    # First, we create the edges and bridge
    g = createEdges(size)

    # Second, we fill in the grid with words
    g = fill(g, 0)
    for i in range(0, size):  # These loops make sure all the IndexCells' words are in the Grid's wordList
        for j in range(0, size):
            if isinstance(g.grid[i][j], HybridCell):
                g.words.append(g.grid[i][j].across.word)
                g.words.append(g.grid[i][j].down.word)
            elif isinstance(g.grid[i][j], IndexCell):
                g.words.append(g.grid[i][j].word)

    # Lastly, we finalize the grid by placing all the black spaces
    g = finalize(g)

    # Converts list of IndexCells to Dictionary of IndexCells
    newIndexes = convertIndexList(g.indexCells)
    sortedCells = sortIndexes(g.indexCells)
    print(sortedCells)


    hints = genHints(sortedCells)
    #hints = generateDummyHints(sortedCells)

    # newIndexes = g.indexCells
    return g, newIndexes, hints


def sortIndexes(indexCells):
    print(indexCells)
    cellies =  sorted(indexCells, key=lambda cell: (cell.x, cell.y))
    return cellies



def generateDummyHints(indexCells):
    hints = []
    letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q',"r","s","t","u","v","w","x","y","z"]
    for cell in indexCells:
        randlet = random.choice(letters)
        hints.append(("Hint_" + randlet))
        letters.remove(randlet)
    return hints

def genHints(indexCells):
    words = []
    for cell in indexCells:
        if (isinstance(cell, HybridCell)):

            if cell.across.word not in words:
                words.append(cell.across.word)
            if cell.down.word not in words:
                words.append(cell.down.word)
        else:
            if cell.word not in words:
                words.append(cell.word)

    print(words)
    print(len(words))
    hints = get_hints(words)
    print(hints)
    print(len(hints))
    return hints


# hints = []
# letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
# for i in range(len(grid.indexCells)):
#   hints.append(("Hint_" + letters[i].upper()))
# return hints


# Creates dict of IndexCells
def convertIndexList(indexs):
    twoDIndexList = []

    for i in range(len(indexs)):
        celly = indexs[i]
        if isinstance(celly, HybridCell):
            cellData2 = [celly.x, celly.y, celly.down.word]
            twoDIndexList.append(cellData2)
        else:
            cellData = [celly.x, celly.y, celly.word]
            twoDIndexList.append(cellData)

    json_data = {
        "grid_data": [
            {"row": row, "column": column, "word": word}
            for row, column, word in twoDIndexList
        ]
    }

    return json_data


# Returns a word to be placed in a Grid
def getWord(letterCells) -> str:
    gotWords, found = findWord(letterCells)
    randIndex = random.randrange(0, len(gotWords))
    return gotWords[randIndex]


def main():
    initGrid(9)


if __name__ == "__main__":
    main()