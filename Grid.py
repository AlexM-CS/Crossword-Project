from version1 import IndexCell, EmptyCell, WordCell


class Grid:
    # Initializes the Grid object with the following fields:
        # length - the grid's length in the x direction
        # height - the grid's height in the y direction
        # gridMap - a dict containing keys of x,y pairs and values of the letters stored there (initialized to None)
        # wordlist - a list containing the words currently on the grid
    # Also includes an optional argument filepath, to import a pre-made grid
    def __init__(self, rows: int, cols: int, *, filepath = None):
        try:
            self.length = rows
            self.height = cols
            self.grid = list()
            self.wordlist = list()

            index = 0
            # Open the file in read mode
            with open(filepath, 'r') as f:
                # Iterate through each line with its index (i is the row index)
                for i, line in enumerate(f):
                    gridline = []  # Create an empty list for each line
                    # Split the line into elements (space-separated or comma-separated)
                    row = line.strip().split()
                    # Iterate through each value with its index (j is the column index)
                    for j, val in enumerate(row):
                        if val == "*":
                            gridline.append(EmptyCell(i, j))  # Pass the indices to EmptyCell
                        elif val == "A":
                            gridline.append(IndexCell(i, j, "_", "_", False, index))
                            index += 1
                        elif val == "D":
                            gridline.append(IndexCell(i, j, "_", "_", True, index))
                            index += 1
                        elif val == "H":
                            gridline.append(IndexCell(i, j, "_", "_", True, index))
                            index += 1
                            gridline.append(IndexCell(i, j, "_", "_", False, index))
                            index += 1
                        else:
                            gridline.append(WordCell(i, j, "_", "_", ))

                    self.grid.append(gridline)  # Add the gridline to the main grid

        except TypeError:
            self.length = rows
            self.height = cols
            self.gridMap = dict()
            self.wordlist = list()

            for i in range(0, rows):
                for j in range(0, cols):
                    self.gridMap[100 * i + j] = "_"