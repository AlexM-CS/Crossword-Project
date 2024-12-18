# Created: 9-29-2024
# Last updated: 12-13-2024
# Alexander Myska, Oliver Strauss, and Brandon Knautz

# This file contains the Grid object, which holds the Cells
# and words that make up the puzzle.

# When running from here, use these imports:
# from Cell import *

# When running from main, use these imports:
from BackEnd.Cell import *

class Grid:
    """
    Description:
    A Grid representation of the crossword.
    Holds the words, the actual grid, and the IndexCells for each word.

    Fields:
    int size - the size of the grid (size x size)
    list[str] words - list of words that are included in the grid
    list[list[Cell]] grid - 2D list of Cells that represents the grid
    list[IndexCell] indexCells - the list of IndexCells inside this grid
    list[BlockedCell] blockedCells - the list of BlockedCells inside this grid
    """
    size = None
    words = None
    grid = None
    indexCells = None
    blockedCells = None

    def __init__(self, size: int) -> None:
        """
        Credit: Alexander Myska
        Initializes a grid of length and width "size"
        @param size: size of the grid
        """
        self.size = size
        self.words = list()
        self.grid = list()
        self.indexCells = list()
        self.blockedCells = list()

        # Creates a Grid full of undefined LetterCells
        for i in range(size):
            gridLine = list()
            for j in range(size):
                gridLine.append(LetterCell(i, j))
            self.grid.append(gridLine)

    def convertIndexCells(self) -> list[dict]:
        """
        Credit: Oliver Strauss
        Converts this Grid's IndexCells into a list to be passed to the front end
        @return: the list of dictionaries representing the Grid's IndexCells
        """
        indexList = list()


        for i in range(0, len(self.indexCells)):
            cell = self.indexCells[i]

            if (isinstance(cell, HybridCell)):
                # If the cell is a Hybrid, we need to add the coordinates,
                # word, and direction for both words here

                cellData = [cell.x, cell.y, cell.across.word, cell.across.getDirection()]
                cellData2 = [cell.x, cell.y, cell.down.word, cell.down.getDirection()]
                indexList.append(cellData)
                indexList.append(cellData2)
            else:
                # Otherwise, add the coordinates, word, and direction for the word here
                cellData = [cell.x, cell.y, cell.word, cell.getDirection()]
                indexList.append(cellData)

        jsonData = [
            {"row" : row, "column" : column, "word" : word, "direction" : direction}
            for row, column, word, direction in indexList
        ]

        # Sorts the index cells in jsonData by position
        jsonData = sorted(jsonData, key=lambda x: (x["row"], x["column"]))



        return jsonData

    def __repr__(self) -> str:
        """
        Credit: Alexander Myska, Oliver Strauss, and Brandon Knautz
        A string representation of the Grid to be used for testing.
        @return a string representation of the Grid
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

    def addBlockedHere(self, x: int, y: int) -> None:
        """
        Credit: Alexander Myska
        Creates a BlockedCell at the given coordinates.
        @param x: x coordinate of where the BlockedCell should be added
        @param y: y coordinate of where the BlockedCell should be added
        """
        self.grid[x][y] = BlockedCell(x, y)
        self.blockedCells.append([x, y])

    def addIndexHere(self, x: int, y: int) -> None:
        """
        Credit: Alexander Myska
        Creates an IndexCell at the given coordinates.
        For testing only.
        @param x: the x coordinate of where the IndexCell should be added
        @param y: the y coordinate of where the IndexCell should be added
        """
        self.grid[x][y] = IndexCell(x, y)
        self.indexCells.append(self.grid[x][y])

    def addHybridHere(self, x: int, y: int) -> None:
        """
        Credit: Alexander Myska
        Creates a HybridCell at the given coordinates.
        For testing only.
        @param x: the x coordinate of where the HybridCell should be added
        @param y: the y coordinate of where the HybridCell should be added
        """
        self.grid[x][y] = HybridCell(x, y)
        self.indexCells.append(self.grid[x][y])

    def addBlockedCell(self, b : BlockedCell) -> None:
        """
        Credit: Alexander Myska
        Adds a BlockedCell to the Grid.
        For testing only.
        @param b: the BlockedCell to add
        """
        self.grid[b.x][b.y] = b
        self.blockedCells.append([b.x, b.y])

    def addIndexCell(self, i: IndexCell) -> None:
        """
        Credit: Alexander Myska
        Adds an IndexCell to the Grid.
        If the given IndexCell is a Hybrid, we remove its fields from
        self.indexCells to prevent duplicates.
        @param i: the IndexCell to add
        """
        if (isinstance(i, HybridCell)):
            if (i.across in self.indexCells):
                self.indexCells.remove(i.across)
            if (i.down in self.indexCells):
                self.indexCells.remove(i.down)
        self.grid[i.x][i.y] = i
        self.indexCells.append(i)

    def addHybridCell(self, h: HybridCell) -> None:
        """
        Credit: Alexander Myska
        Adds a HybridCell to the Grid.
        For testing only.
        @param h: the HybridCell to add
        """
        self.grid[h.x][h.y] = h
        self.indexCells.append(h)

    def getEdges(self) -> list[list[LetterCell]]:
        """
        Credit: Alexander Myska
        Returns a 2D list representing the edges of the Grid.
        Edges that contain BlockedCells will be split into multiple lists.
        @return: a sorted (by length, descending) 2D list representing the edges
        """
        output = list()
        edge1 = list()
        edge2 = list()
        row = 0
        col = 0

        # First, get the top and bottom rows:
        while (col < self.size):
            if (isinstance(self.grid[0][col], BlockedCell)): # Top row
                output.append(edge1)
                edge1 = list()
            else:
                edge1.append(self.grid[0][col])

            if (isinstance(self.grid[self.size - 1][col], BlockedCell)): # Bottom row
                output.append(edge2)
                edge2 = list()
            else:
                edge2.append(self.grid[self.size - 1][col])

            col += 1

        # Append the edges we just finished, and redeclare them
        output.append(edge1)
        output.append(edge2)
        edge1 = list()
        edge2 = list()

        # Next, get the left and right columns:
        while (row < self.size):
            if (isinstance(self.grid[row][0], BlockedCell)): # Left column
                output.append(edge1)
                edge1 = list()
            else:
                edge1.append(self.grid[row][0])

            if (isinstance(self.grid[row][self.size - 1], BlockedCell)): # Right column
                output.append(edge2)
                edge2 = list()
            else:
                edge2.append(self.grid[row][self.size - 1])

            row += 1

        # Append the edges we just finished
        output.append(edge1)
        output.append(edge2)

        # Finally, we will sort the edges by size, in order of largest to smallest:
        return sorted(output, key = len, reverse = True)

    def getNumAdjacents(self, x: int, y: int) -> int:
        """
        Credit: Alexander Myska
        Returns the number of adjacent cells with letters
        @param x: the x coordinate to check
        @param y: the y coordinate to check
        @return: the number of adjacent cells with letters
        """
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
        """
        Credit: Alexander Myska
        Initializes a CustomGrid.
        """
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