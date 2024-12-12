# Created: 9-29-2024
# Last updated: 12-5-2024
# Alexander Myska, Oliver Strauss, and Brandon Knautz

# This file contains the grid object, which holds the Cells
# and words that make up the puzzle.

from BackEnd.Cell import *

# This class represents a Grid of squares with either letters and black squares
class Grid:
    """
    A grid representation of the crossword, holds the words, the actual grid, and the index cells for each word

    Fields:

    size - the size of the grid (size x size)
    words - list of words that are included in the grid
    grid - list of lists that represents the grid
    """
    size = None
    words = None
    indexCells = None

    def __init__(self, size: int) -> None:
        """
        Initializes a grid of length and width "size"
        @param size: size of the grid
        """
        self.size = size
        self.words = list()
        self.grid = list()
        self.indexCells = list()
        self.blockedCells = list()

        #Goes through and creates each cell as a letter cell with no letter attached
        for i in range(size):
            gridLine = list()
            for j in range(size):
                gridLine.append(LetterCell(i, j))
            self.grid.append(gridLine)

    def convert(self):
        indexList = list()

        for i in range(0, len(self.indexCells)):
            cell = self.indexCells[i]
            if (isinstance(cell, HybridCell)):
                cellData2 = [cell.x, cell.y, cell.down.word]
                indexList.append(cellData2)
            else:
                cellData = [cell.x, cell.y, cell.word]
                indexList.append(cellData)

        jsonData = {
            "grid_data": [
                {"row": row, "column": column, "word": word}
                for row, column, word in indexList
            ]
        }

        jsonData = jsonData['grid_data']

        for i in range(len(indexList)):
            cell = indexList[i]
            if isinstance(cell, HybridCell):
                indexList.append(cell.down)

        print(jsonData)

        for i in range(0, len(self.indexCells)):
            for j in range(0, len(jsonData)):
                if (self.indexCells[i].word == jsonData[j]['word']):
                    jsonData[j]["direction"] = self.indexCells[i].getDirection()

        # Sorts the index cells in jsonData by position
        jsonData = sorted(jsonData, key=lambda x: (x["row"], x["column"]))

        return jsonData

    def __repr__(self) -> str:
        """
        a string representation of the grid
        @return a string representation of the grid
        """
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

    # Creates a BlockedCell at the given coordinates
    def addBlockedHere(self, x: int, y: int) -> None:
        """
        Creates a BlockedCell at the given coordinates
        @param x: x coordinate of where the blocked cell is wanting to be added
        @param y: y coordinate of where the blocked cell is wanting to be added
        """
        self.grid[x][y] = BlockedCell(x, y)

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

    def getNumAdjacents(self, x: int, y: int) -> int:
        numAdjacents = 0
        if (x - 1 >= 0 and self.grid[x - 1][y].letter != ""): # Checks the cell above this cell
            numAdjacents += 1
        if (x + 1 < self.size and self.grid[x + 1][y].letter != ""): # Checks the cell below this cell
            numAdjacents += 1
        if (y - 1 >= 0 and self.grid[x][y - 1].letter != ""): # Checks the cell to the left of this cell
            numAdjacents += 1
        if (y + 1 < self.size and self.grid[x][y + 1].letter != ""): # Checks the cell to the right of this cell
            numAdjacents += 1
        return numAdjacents

class CustomGrid(Grid):
    """
    Grids are an object representation of the crossword. Holds the grid, the words, and Index Cells.
    CustomGrids take in a 2D list to create themselves instead of being procedurally generated.
    This version of Grids is only used for debugging and testing.
    """
    def __init__(self, size : int, grid : list[list[str]]) -> None:
        """ Initializes a CustomGrid. """
        super().__init__(size)
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                self.grid[i][j].letter = grid[i][j]

def main() -> Grid:
    cells = [
        ["*", "*", "*", "*", "*"],
        ["A", "B", "O", "U", "T"],
        ["*", "*", "*", "*", "*"],
        ["*", "U", "S", "!", "*"],
        ["*", "*", "*", "*", "*"],
    ]
    g = CustomGrid(5, cells)
    print(g)
    return g

if __name__ == "__main__":
    main()