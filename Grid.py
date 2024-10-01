# 9-29-2024
# Alexander Myska, Oliver Strauss, Brandon Knautz

# This file contains the grid object, which holds the Cells
# and words that make up the puzzle.

from Cell import *

class Grid:
    # Initializes a Grid object with the following fields:
        # int length - the number of rows in the grid
        # int width - the number of columns in the grid
        # list(str) words - list of words that are included in the grid
        # list(list(Cell)) - list of lists that represents the grid
        # str filepath - file that this init will read from (reference)
        # return - None
    def __init__(self, length: int, width: int, filepath = None):
        self.length = length
        self.width = width
        self.words = list()
        self.grid = list()

        if (type(filepath) == str):
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
            for i in range(length):
                gridLine = list()
                for j in range(width):
                    gridLine.append(LetterCell(i, j))
                self.grid.append(gridLine)

    # Overriding the default string representation
        # return - string representation of this object
    def __str__(self):
        output = "GRID:\n"
        for i in range(self.length):
            for j in range(self.width):
                currentCell = self.grid[i][j]
                if isinstance(currentCell, LetterCell):
                    output += "_"
                elif isinstance(currentCell, IndexCell):
                    if (currentCell.dir):
                        output += "A"
                    else:
                        output += "D"
                elif isinstance(currentCell, HybridCell):
                    output += "H"
                else:
                    output += "*"
                if (j + 1 < self.width):
                    output += " "
            if (i + 1 < self.length):
                output += "\n"
        return output

    # Test method to be used to create arbitrary scenarios
        # return - None
    def addBlockedCell(self, x: int, y: int):
        self.grid[x][y] = BlockedCell(x, y)

    # Test method to be used to create arbitrary scenarios
        # return - None
    def addIndexCell(self, x: int, y: int, dir: bool):
        self.grid[x][y] = IndexCell(x, y, dir)

    # Test method to be used to create arbitrary scenarios
        # return - None
    def addHybridCell(self, x: int, y: int):
        self.grid[x][y] = HybridCell(x, y)

    # Helper method for initIndexCells()
        # return - int length the length of this IndexCell's word
    def findLength(self, ic: IndexCell):
        length = 1
        if (ic.dir):  # True: the word is across
            if (ic.y + length < self.length):
                while (ic.y + length < self.length):
                    if not (isinstance(self.grid[ic.x][ic.y + length], BlockedCell)):
                        length += 1
                    else:
                        break

        else:  # False: the word is down
            if (ic.x + length < self.width):
                while (ic.x + length < self.width):
                    if not (isinstance(self.grid[ic.x + length][ic.y], BlockedCell)):
                        length += 1
                    else:
                        break

        return length

    # Helper method for initIndexCells()
        # return - list(LetterCell) the body of this IndexCell's word
    def findBody(self, ic: IndexCell):
        body = list()
        if (ic.dir): # True: the word is across
            i = 0
            while (ic.y + i < self.length):
                if not (isinstance(self.grid[ic.x][ic.y + i], BlockedCell)):
                    body.append(self.grid[ic.x][ic.y + i])
                    i += 1
                else:
                    break

        else: # False: the word is down
            i = 0
            while (ic.x + i < self.width):
                if not (isinstance(self.grid[ic.x + i][ic.y], BlockedCell)):
                    body.append(self.grid[ic.x + i][ic.y])
                    i += 1
                else:
                    break

        return body

    # Helper method for initIndexCells()
        # return - int intersections the number of intersections this IndexCell's word will have with other words
    def findIntersections(self, ic: IndexCell):
        total = 0
        for cell in ic.body:
            if (cell.x + 1 < self.length):
                if not (isinstance(self.grid[cell.x + 1][cell.y],BlockedCell) or (self.grid[cell.x + 1][cell.y] in ic.body)):
                    total += 1
                    continue
            if (cell.x - 1 >= 0):
                if not (isinstance(self.grid[cell.x - 1][cell.y],BlockedCell) or (self.grid[cell.x - 1][cell.y] in ic.body)):
                    total += 1
                    continue
            if (cell.y + 1 < self.width):
                if not (isinstance(self.grid[cell.x][cell.y + 1],BlockedCell) or (self.grid[cell.x][cell.y + 1] in ic.body)):
                    total += 1
                    continue
            if (cell.y - 1 >= 0):
                if not (isinstance(self.grid[cell.x][cell.y - 1],BlockedCell) or (self.grid[cell.x][cell.y - 1] in ic.body)):
                    total += 1
                    continue
        return total

    # Fills in various fields for each of the IndexCells in the grid
    # Specifically: list(LetterCell) body, int intersections, int length
        # return - None
    def initIndexCells(self):
        for i in range(self.length):
            for j in range(self.width):
                currentCell = self.grid[i][j]
                if (isinstance(currentCell,HybridCell)):
                    currentCell.across.wordLength = self.findLength(currentCell.across)
                    currentCell.across.body = self.findBody(currentCell.across)
                    currentCell.across.intersections = self.findIntersections(currentCell.across)
                    currentCell.down.wordLength = self.findLength(currentCell.down)
                    currentCell.down.body = self.findBody(currentCell.down)
                    currentCell.down.intersections = self.findIntersections(currentCell.down)
                elif (isinstance(currentCell,IndexCell)):
                    currentCell.wordLength = self.findLength(currentCell)
                    currentCell.body = self.findBody(currentCell)
                    currentCell.intersections = self.findIntersections(currentCell)

    # Helper method for createWords()
        # return - None
    def addWord(self):
        pass

    # Helper method for createWords()
        # return - None
    def addWordContains(self, required: list):
        pass

    # Will assign a word to each of the IndexCells given, in order
        # return - None
    def createWords(self, indexCells: list):
        pass