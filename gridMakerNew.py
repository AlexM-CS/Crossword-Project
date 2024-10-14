# 10-10-2024
# Alexander Myska, Oliver Strauss, Brandon Knautz

# This class will be used to make grids, this time by looking for words first

from Cell import *
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
            c = randomSide[partitionIndex]
            g.grid[c.x][c.y] = BlockedCell(c.x, c.y)
            allEdges.remove(randomSide)
            partitions += 1

        g = generateBridge(g)

        # Loop over the edges, give them words

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
        for i in range(0, g.size - 1):
            bridge.append(g.grid[i][randNum])

    else: # Look at rows
        while not ((g.grid[randNum][0] in allEdges[bridgeSide]) and (g.grid[randNum][g.size - 1] in allEdges[opposite])):
            evenIndices.remove(randNum)
            randNum = random.choice(evenIndices)
        for i in range(0, g.size - 1):
            bridge.append(g.grid[randNum][i])

    # Create a word for the bridge
    for i in range(0, len(bridge)):
        bridge[i].setLetter("A")
    print(bridge)

    displayGrid(g)
    quit()

    return g

    # Generate a bridge between the disconnected parts

    # Loop over the edges and the bridge, and try to give them words
    # Check if all the edges have words now
    # If they do, break

    # Return a list of words that we will build off from

def fill(grid, size: int):
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

def initGrid():
    pass

def main():
    createEdges(9)

if __name__ == "__main__":
    main()