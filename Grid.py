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
    def __init__(self, size: int, filepath = None) -> None:
        self.size = size
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
                if (j + 1 < self.size):
                    output += " "
            if (i + 1 < self.size):
                output += "\n"
        return output

    # Test method to be used to create arbitrary scenarios
    def addBlockedCell(self, x: int, y: int) -> None:
        self.grid[x][y] = BlockedCell(x, y)

    # Test method to be used to create arbitrary scenarios
    def addIndexCell(self, x: int, y: int, dir: bool) -> None:
        self.grid[x][y] = IndexCell(x, y, dir)

    # Test method to be used to create arbitrary scenarios
    def addHybridCell(self, x: int, y: int) -> None:
        self.grid[x][y] = HybridCell(x, y)

    # Helper method for initIndexCells()
        # return - int length the length of this IndexCell's word
    def findLength(self, ic: IndexCell) -> int:
        length = 1
        if (ic.dir):  # True: the word is across
            if (ic.y + length < self.size):
                while (ic.y + length < self.size):
                    if not (isinstance(self.grid[ic.x][ic.y + length], BlockedCell)):
                        length += 1
                    else:
                        break

        else:  # False: the word is down
            if (ic.x + length < self.size):
                while (ic.x + length < self.size):
                    if not (isinstance(self.grid[ic.x + length][ic.y], BlockedCell)):
                        length += 1
                    else:
                        break

        return length

    # Helper method for initIndexCells()
        # return - list[LetterCell] the body of this IndexCell's word
    def findBody(self, ic: IndexCell) -> list[LetterCell]:
        body = list()
        if (ic.dir): # True: the word is across
            i = 0
            while (ic.y + i < self.size):
                if not (isinstance(self.grid[ic.x][ic.y + i], BlockedCell)):
                    body.append(self.grid[ic.x][ic.y + i])
                    i += 1
                else:
                    break

        else: # False: the word is down
            i = 0
            while (ic.x + i < self.size):
                if not (isinstance(self.grid[ic.x + i][ic.y], BlockedCell)):
                    body.append(self.grid[ic.x + i][ic.y])
                    i += 1
                else:
                    break

        return body

    # Helper method for initIndexCells()
        # return - int intersections the number of intersections this IndexCell's word will have with other words
    def findIntersections(self, ic: IndexCell) -> int:
        total = 0
        for cell in ic.body:
            if (cell.x + 1 < self.size):
                if not (isinstance(self.grid[cell.x + 1][cell.y],BlockedCell) or (self.grid[cell.x + 1][cell.y] in ic.body)):
                    total += 1
                    continue
            if (cell.x - 1 >= 0):
                if not (isinstance(self.grid[cell.x - 1][cell.y],BlockedCell) or (self.grid[cell.x - 1][cell.y] in ic.body)):
                    total += 1
                    continue
            if (cell.y + 1 < self.size):
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
    def initIndexCells(self) -> None:
        for i in range(self.size):
            for j in range(self.size):
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

    # Sorts the IndexCells in the array from most to least intersections
    # If the argument "ascending" is set to True, it will be least to most intersections
        # return - list[IndexCell] sorted list of IndexCells by intersections
    def sortIndexCells(self, ascending : bool = False) -> list[IndexCell]:
        cells = list()
        for i in range(self.size):
            for j in range(self.size):
                currentCell = self.grid[i][j]
                if (isinstance(currentCell, HybridCell)):
                    cells.append(currentCell.across)
                    cells.append(currentCell.down)
                elif (isinstance(currentCell, IndexCell)):
                    cells.append(currentCell)

        # After gathering the IndexCells, sort the array
        if (ascending): # True: List will be least to most intersections
            for i in range(0, len(cells)):
                min_index = i

                for j in range(i + 1, len(cells)):
                    if (cells[j].intersections < cells[min_index].intersections):
                        min_index = j

                (cells[i], cells[min_index]) = (cells[min_index], cells[i])
        else: # False: List will be most to least intersections
            for i in range(0, len(cells)):
                max_index = i

                for j in range(i + 1, len(cells)):
                    if (cells[j].intersections > cells[max_index].intersections):
                        max_index = j

                (cells[i], cells[max_index]) = (cells[max_index], cells[i])

        return cells

    def getEdges(self):
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

    # Helper method for createWords()
    def addWord(self) -> None:
        pass

    # Helper method for createWords()
    def addWordContains(self, required: list) -> None:
        pass

    # Will assign a word to each of the IndexCells given, in order
    def createWords(self, indexCells: list) -> None:
        pass