# Created: 9-29-2024
# Last updated: 11-19-2024
# Alexander Myska, Oliver Strauss, and Brandon Knautz

# This file contains the grid object, which holds the Cells
# and words that make up the puzzle.

from BackEnd.Cell import *

# This class represents a Grid of squares with either letters and black squares
class Grid:
    # Initializes a Grid object with the following fields:
        # int size - the size of the grid (size x size)
        # list(str) words - list of words that are included in the grid
        # list(list(Cell)) grid - list of lists that represents the grid
        # str filepath - file that this init will read from (reference)
    def __init__(self, size: int, filepath = None) -> None:
        self.size = size
        self.words = list()
        self.grid = list()
        self.indexCells = list()
        self.blockedCells = list()

        # Check if we are importing a pre-made Grid
        if (type(filepath) == str):

            # ==============================================
            #        We should revisit this method
            # ==============================================

            # When the filepath is a string, the grid will be defined using a
            # specific file as a reference.
            # This branch of __init__ iterates through the given file and
            # creates Cells as it goes.
            self.filepath = filepath
            try:
                with open(filepath, 'r') as f:
                    for i, line in enumerate(f):
                        gridLine = list()
                        row = line.strip().split()
                        for j, val in enumerate(row):
                            if val == "*":
                                gridLine.append(BlockedCell(i, j))
                            elif val == "A":
                                gridLine.append(IndexCell(i, j, True))
                            elif val == "D":
                                gridLine.append(IndexCell(i, j, False))
                            elif val == "H":
                                gridLine.append(HybridCell(i, j))
                            else:
                                gridLine.append(LetterCell(i, j))
                        self.grid.append(gridLine)

            except FileNotFoundError:
                # Handles FileNotFoundError
                print("The file you are trying to read cannot be found.")
                print("Quitting...")

        else:
            # When the filepath is not a string, the grid will be defined
            # by its length and width, and filled with LetterCells.
            # This branch of __init__ iterates through length and width,
            # creating LetterCells as it goes.
            # This should be used for testing only.
            for i in range(size):
                gridLine = list()
                for j in range(size):
                    gridLine.append(LetterCell(i, j))
                self.grid.append(gridLine)

    # Overriding the default string representation
        # return - string representation of this object
    def __str__(self) -> str:
        output = "GRID:\n"
        for i in range(self.size):
            for j in range(self.size):
                currentCell = self.grid[i][j]
                if isinstance(currentCell, LetterCell):
                    output += currentCell.letter
                else:
                    output += "*"
                if (j + 1 < self.size):
                    output += " "
            if (i + 1 < self.size):
                output += "\n"
        return output

    # Use this method to re-create a Grid from a string
    def __repr__(self) -> str:
        this =  f"{self.size}"
        for ic in self.indexCells:
            this += f";{ic.__str__()}"
        return this

    # Creates a BlockedCell at the given coordinates
    def addBlockedHere(self, x: int, y: int) -> None:
        self.grid[x][y] = BlockedCell(x, y)

    # Adds a BlockedCell to the Grid
    def addBlockedCell(self, b: BlockedCell) -> None:
        self.grid[b.x][b.y] = b

    # Creates an IndexCell at the given coordinates
    def addIndexHere(self, x: int, y: int) -> None:
        self.grid[x][y] = IndexCell(x, y)
        self.indexCells.append(self.grid[x][y])

    # Adds an IndexCell to the Grid
    def addIndexCell(self, i: IndexCell) -> None:
        self.grid[i.x][i.y] = i
        self.indexCells.append(i)

    # Creates a HybridCell at the given coordinates
    def addHybridHere(self, x: int, y: int) -> None:
        self.grid[x][y] = HybridCell(x, y)

    # Adds a HybridCell to the Grid
    def addHybridCell(self, h: HybridCell) -> None:
        self.grid[h.x][h.y] = h

    # Returns a list of lists representing the edges of the Grid, where each sublist is a group of Cells
    # representing individual letters
        # return - a list of lists representing the edges
    def getEdges(self) -> list[list[LetterCell]]:
        # Top, left, right, bottom
        output = [list(), list(), list(), list()]
        topRow = 0
        bottomRow = self.size - 1
        col = 0
        while (col < self.size):
            if (isinstance(self.grid[topRow][col], LetterCell)):
                output[0].append(self.grid[topRow][col])
            if (isinstance(self.grid[bottomRow][col], LetterCell)):
                output[3].append(self.grid[bottomRow][col])
            col += 1
        row = 0
        leftCol = 0
        rightCol = self.size - 1
        while (row < self.size):
            if (isinstance(self.grid[row][leftCol], LetterCell)):
                output[1].append(self.grid[row][leftCol])
            if (isinstance(self.grid[row][rightCol], LetterCell)):
                output[2].append(self.grid[row][rightCol])
            row += 1
        return output

    def getNumNeighbors(self, x: int, y: int) -> int:
        numNeighbors = 0
        if (x - 1 >= 0 and self.grid[x - 1][y].letter != ""): # Checks the cell above this cell
            numNeighbors += 1
        if (x + 1 < self.size and self.grid[x + 1][y].letter != ""): # Checks the cell below this cell
            numNeighbors += 1
        if (y - 1 >= 0 and self.grid[x][y - 1].letter != ""): # Checks the cell to the left of this cell
            numNeighbors += 1
        if (y + 1 >= 0 and self.grid[x][y + 1].letter != ""): # Checks the cell to the right of this cell
            numNeighbors += 1
        return numNeighbors

    # Helper method for createWords()
    def addWord(self) -> None:
        pass

    # Helper method for createWords()
    def addWordContains(self, required: list) -> None:
        pass

    # Will assign a word to each of the IndexCells given, in order
    def createWords(self, indexCells: list) -> None:
        pass