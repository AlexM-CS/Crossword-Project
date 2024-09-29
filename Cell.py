from version1 import WordList


class Cell:
    # Initializes a Cell with the following fields:
        # x - row of the grid that this cell belongs to
        # y - column of the grid that this cell belongs to
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self):
        return "C({0},{1})".format(self.x, self.y)


class BlockedCell(Cell):
    # Parent init
    def __init__(self, x: int, y: int):
        super().__init__(x, y)

    def __str__(self):
        return "E({0},{1})\n".format(self.x, self.y)


class WordCell(Cell):
    # Initializes a WordCell with the following fields:
        # x - row of the grid that this cell belongs to
        # y - column of the grid that this cell belongs to
        # letter - the letter assigned to this cell
    def __init__(self, x: int, y: int, letter: str, word: WordList):
        super().__init__(x, y)
        self.letter = letter
        self.word = word

    def __str__(self):
        return "W({0},{1},{2)\n".format(self.x, self.y,self.letter)

class IndexCell(WordCell):
    # Parent init
        # index - number for this cell
        # dir - boolean that determines direction (True = DOWN, False = ACROSS)
    def __init__(self, x: int, y: int, letter: str, dir: bool):
        super().__init__(x, y, letter)
        word = ""
        body = list()
        length = 0

        # This maybe should change in the future, if the cell has both
        # an across and down word starting from here
        self.dir = dir

    # Overriding the default string representation
    def __str__(self):
        return "I({0},{1},{2},{3})\n".format(self.x, self.y,self.letter,self.dir)


class HybridCell(WordCell):
    def __init__():