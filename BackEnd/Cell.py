# Created: 9-29-2024
# Last Updated: 12-11-2024
# Alexander Myska, Oliver Strauss, and Brandon Knautz

# This file contains the Cell classes that will be used as the
# body for the Grid.

from math import *

class Cell:
    """
    A Parent Cell class to be used as a base for the other Cell Types.

    Fields:
    int x - the Cell's x-coordinate
    int y - the Cell's y-coordinate
    str name - "C" for normal Cells
    """
    x = None
    y = None
    name = "C"

    def __init__(self, x: int, y: int) -> None:
        """
        Initializes a Cell.
        @param x: row of the grid that this cell belongs to
        @param y: column of the grid that this cell belongs to
        @return None
        """
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        """
        String representation of this Cell
        @return string representation of this Cell
        """
        return f"{self.name}({self.x},{self.y})"

    def compare(self, other) -> int:
        """
        Compares this Cell's position to another's position.
        @param other: the Cell to compare with
        @return: binary int that represents the distance
        """
        dif_x = abs(self.x - other.x)
        dif_y = abs(self.y - other.y)

        if (dif_x > 0 and dif_y > 0): # Word differs by x and y
            output = 0b1100000
        elif (dif_x > 0): # Word differs only by x
            output = 0b1000000
        elif (dif_y > 0): # Word differs only by y
            output = 0b0100000
        else: # The two cells have the same coordinates
            return 0b0000000

        # The last 5 bits are the magnitude of the distance
        totalDist = floor(sqrt(dif_x**2 + dif_y**2))
        output ^= totalDist

        return output

class BlockedCell(Cell):
    """
    A Cell that cannot contain letters, displayed as black or "*".

    Fields:
    str name - "B" for Blocked Cells
    """
    name = "B"
    letter = "*"

    def __init__(self, x: int, y: int) -> None:
        """
        Initializes a BlockedCell.
        @return None
        """
        super().__init__(x, y)

class LetterCell(Cell):
    """
    A LetterCell contains a letter and is part of a word.

    Fields:
    str name - "L" for LetterCells
    str letter - the letter held by this LetterCell
    """
    name = "L"
    letter = None

    def __init__(self, x: int, y: int) -> None:
        """
        Initializes a LetterCell.
        """
        super().__init__(x, y)
        self.letter = ""

    def __repr__(self) -> str:
        """
        String representation of this LetterCell.
        @return: string representation of this LetterCell.
        """
        return f"{self.name}({self.x},{self.y},{self.letter})"

    # Sets the letter for this LetterCell to be param
    def setLetter(self, param: str) -> None:
        """
        Sets the letter held by this LetterCell
        @param param: the letter to be held by this LetterCell
        @return: None
        """
        self.letter = param

class IndexCell(LetterCell):
    """
    A Cell that contains a letter and is the beginning of a word.

    Fields:
    str name - "I" for IndexCells
    list[Cell] body - the "body" of this IndexCell
    int wordLength - the length of this IndexCell's word
    """
    name = "I"
    body = None
    word = None
    wordLength = None

    def __init__(self, x: int, y: int) -> None:
        """
        Initializes an IndexCell.
        """
        super().__init__(x, y)
        self.body = list()
        self.word = ""
        self.wordLength = 0

    def setWord(self, word: str) -> None:
        """
        Sets the letters in this IndexCell's body.
        @param word:
        @return:
        """
        self.word = word
        self.wordLength = len(word)
        for i in range(0, len(word)):
            self.body[i].setLetter(self.word[i])

    def setBody(self, body: list, word: str) -> None:
        """
        Sets the body of this IndexCell to be a list of LetterCells
        @param body:
        @param word:
        @return:
        """
        self.body = body
        self.setWord(word)

    # Gets the direction of this body
        # True if across, False if down
    def getDirection(self) -> bool:
        """
        Gets the direction of this IndexCell's body. True means across, False means down.
        @return: the direction of this IndexCell's body.
        """
        if (len(self.body) == 0):
            return False
        return self.body[0].compare(self.body[-1]) < 0b1000000

class HybridCell(IndexCell):
    """
    HybridCells are Cells where two different words start,
    one across and one down.

    Fields:
    str name - "H" for HybridCells
    IndexCell across - the across IndexCell that starts here
    IndexCell down - the down IndexCell that starts here
    """
    name = "H"

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.letter = ""
        self.across = super().__init__(x, y)
        self.down = super().__init__(x, y)