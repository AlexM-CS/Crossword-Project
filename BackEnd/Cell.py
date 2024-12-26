# Created: 9-29-2024
# Last Updated: 12-12-2024
# Alexander Myska, Oliver Strauss, and Brandon Knautz

# This file contains the Cell classes that will be used as the
# body for the Grid.

# External imports:
import random

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
        Credit: Alexander Myska, Oliver Strauss, and Brandon Knautz
        Initializes a Cell.
        @param x: row of the grid that this cell belongs to
        @param y: column of the grid that this cell belongs to
        """
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        """
        Credit: Alexander Myska and Brandon Knautz
        String representation of this Cell
        @return string representation of this Cell
        """
        return f"{self.name}({self.x},{self.y})"

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
        Credit: Alexander Myska, Oliver Strauss, and Brandon Knautz
        Initializes a BlockedCell.
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

    def __init__(self, x: int, y: int, letter : str = "") -> None:
        """
        Credit: Alexander Myska, Oliver Strauss, and Brandon Knautz
        Initializes a LetterCell.
        @param letter: the letter of this LetterCell, if any
        """
        super().__init__(x, y)
        self.letter = letter

    def __repr__(self) -> str:
        """
        Credit: Alexander Myska and Brandon Knautz
        String representation of this LetterCell.
        @return: string representation of this LetterCell.
        """
        return f"{self.name}({self.x},{self.y},{self.letter})"

    def setLetter(self, letter : str) -> None:
        """
        Credit: Alexander Myska
        Sets the letter held by this LetterCell
        @param letter: the letter to be held by this LetterCell
        """
        self.letter = letter

class IndexCell(LetterCell):
    """
    A Cell that contains a letter and is the beginning of a word.

    Fields:
    str name - "I" for IndexCells
    list[Cell] body - the "body" of this IndexCell
    str word - the word stored by this IndexCell
    int wordLength - the length of this IndexCell's word
    """
    name = "I"
    body = None
    word = None
    wordLength = None

    def __init__(self, x: int, y: int, letter : str = "") -> None:
        """
        Credit: Alexander Myska, Oliver Strauss, and Brandon Knautz
        Initializes an IndexCell.
        """
        super().__init__(x, y, letter)
        self.body = list()
        self.word = ""
        self.wordLength = 0

    def setWord(self, word: str) -> None:
        """
        Sets the letters in this IndexCell's body.
        @param word: the word stored by this IndexCell
        """
        self.word = word
        self.wordLength = len(word)
        for i in range(0, len(word)):
            self.body[i].setLetter(self.word[i])

    def setBody(self, body: list, word: str) -> None:
        """
        Sets the body of this IndexCell to be a list of LetterCells
        @param body: the body of this IndexCell
        @param word: the word stored by this IndexCell
        @return:
        """
        self.body = body
        self.setWord(word)

    def getDirection(self) -> bool:
        """
        Gets the direction of this IndexCell's body. True means across, False means down.
        @return: the direction of this IndexCell's body.
        """
        if (len(self.body) == 0):
            raise ValueError("This IndexCell's body is undefined")

        first = self.body[0]
        last = self.body[-1]

        if (first.x < last.x): # The Cell's x-coordinates differ
            return False
        elif (first.y < last.y): # The Cell's y-coordinates differ
            return True
        else: # This IndexCell's body is only one Cell; raise an exception
            raise ValueError("This IndexCell's body is only one Cell")

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
    across = None
    down = None

    def __init__(self, x: int, y: int, letter : str = "") -> None:
        self.x = x
        self.y = y
        self.letter = ""
        self.across = super().__init__(x, y, letter)
        self.down = super().__init__(x, y, letter)

    def getDirection(self) -> bool:
        """
        Returns the direction of one of its IndexCells, randomly
        @return: True if across, False if down
        """
        choices = [self.across, self.down]
        cell = random.choice(choices)
        return cell.getDirection()
