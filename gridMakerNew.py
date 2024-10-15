# 10-10-2024
# Alexander Myska, Oliver Strauss, Brandon Knautz
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
def fill(grid, size: int) -> Grid:
    # Set int wordSize = size - 2

    while True: # Loop until about 70% of the grid has letters
        pass
        # Run diagonal check
            # Try to create a word of length wordSize, perpendicular to the bridge
        # Run diagonal check
            # Try to create a word of length wordSize, parallel to the bridge
        # If wordSize is > 3, wordSize -= 2
        # Minimum wordSize is 3

    # After all letters are in place, any Cell without a letter becomes a BlockedCell
    # Return the completed grid

    pass

# Method that initializes a Grid with words
def initGrid() -> Grid:
    pass

# Returns a word to be placed in a Grid
def getWord(letterCells) -> str:
    gotWords,found = findWord(letterCells)
    randIndex = random.randrange(0, len(gotWords))
    return gotWords[randIndex]

def main():
    createEdges(9)

if __name__ == "__main__":
    main()