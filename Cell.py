# 9-29-2024
# Alexander Myska, Oliver Strauss, Brandon Knautz

# This file contains the Cell classes that will be used as the
# body for the Grid.

# A Parent Cell class to be used as a base for the other Cells
class Cell:
    # Initializes a Cell with the following fields:
        # int x - row of the grid that this cell belongs to
        # int y - column of the grid that this cell belongs to
        #return - None
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    # Overriding the default string representation
        # return - string representation of this object
    def __str__(self):
        return "C({0},{1})".format(self.x, self.y)

# A Cell that cannot contain letters, displayed as black or "*"
class BlockedCell(Cell):
    # Parent init
        # return - None
    def __init__(self, x: int, y: int):
        super().__init__(x, y)

    # Overriding the default string representation
        # return - string representation of this object
    def __str__(self):
        return "B({0},{1})".format(self.x, self.y)

# A Cell that contains a letter and is part of a word
class LetterCell(Cell):
    # Initializes a LetterCell with the following fields:
        # int x - row of the grid that this cell belongs to
        # int y - column of the grid that this cell belongs t0
        # str letter - the letter assigned to this cell (defaults to "")
        # return - None
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.letter = ""

    # Overriding the default string representation
        # return - string representation of this object
    def __str__(self):
        return "L({0},{1},{2})".format(self.x, self.y,self.letter)

# A Cell that contains a letter, and is the start of a word
class IndexCell(LetterCell):
    # Initializes an IndexCell with the following fields:
        # int x - row of the grid that this cell belongs to
        # int y - column of the grid that this cell belongs to
        # str letter - the letter assigned to this cell (defaults to "")
        # list(LetterCell) body - contains the cells that hold the letters for this word
        # str word - the word that this cell is the start of
        # int intersections - the number of words that intersect this word's body
        # int length - the length of this word
        # bool dir - the direction of the word of this cell
        # return - None
    def __init__(self, x: int, y: int, dir: bool):
        super().__init__(x, y)
        self.body = list()
        self.word = ""
        self.intersections = 0
        self.wordLength = 0
        self.dir = dir # Note: across = True, down = False

    # Overriding the default string representation
        # return - string representation of this object
    def __str__(self):
        return "I({0},{1},{2},{3})".format(self.x, self.y,self.letter,self.dir)

# A Cell that is the beginning of two words
class HybridCell(IndexCell):
    # Initializes a HybridCell with the following fields:
        # x - row of the grid that this cell belongs to
        # y - column of the grid that this cell belongs to
        # letter - the letter assigned to this cell (defaults to "")
        # IndexCell across - the sideways IndexCell that starts here
        # IndexCell down - the downward IndexCell that starts here
        # return - None
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.letter = ""
        self.across = super().__init__(x, y, True)
        self.down = super().__init__(x, y, False)

    # Overriding the default string representation
        # return - string representation of this object
    def __str__(self):
        return "H({0},{1},{2})".format(self.x, self.y,self.letter)