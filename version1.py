# 9-30-2024
# Alexander Myska, Oliver Strauss, Brandon Knautz

# This class will be used to test our code for its intended behavior

from Cell import *
from Grid import *
from display import *

# Test the output of a grid toString
def test1():
    g = Grid(4, 4)
    print(g)
    # The previous line should print a grid of blank cells
    g.addBlockedCell(0, 0)
    g.addBlockedCell(1, 1)
    g.addBlockedCell(2, 2)
    g.addBlockedCell(3, 3)
    print(g)
    # The previous line should print a grid with a diagonal line
    # of blocked cells from top-left to bottom-right

# Test the output of various Cell toStrings
def test2():
    c = Cell(0, 0)
    print(c)
    c = BlockedCell(0, 0)
    print(c)
    c = LetterCell(0, 0)
    print(c)
    c = IndexCell(0, 0, True)
    print(c)
    c = HybridCell(0, 0)
    print(c)
    # The expected output should be this:
    # C(0,0)
    # B(0,0)
    # L(0,0,)
    # I(0,0,,True)
    # H(0,0,)

# Test the method findLength
def test3():
    g = Grid(7,7)
    g.addBlockedCell(0, 2)
    g.addBlockedCell(1, 1)
    g.addBlockedCell(1, 3)
    g.addBlockedCell(1, 5)
    g.addBlockedCell(2, 3)
    g.addBlockedCell(2, 5)
    g.addBlockedCell(3, 1)
    g.addBlockedCell(3, 3)
    g.addBlockedCell(3, 5)
    g.addBlockedCell(4, 1)
    g.addBlockedCell(4, 3)
    g.addBlockedCell(5, 1)
    g.addBlockedCell(5, 3)
    g.addBlockedCell(5, 5)
    g.addBlockedCell(6, 4)
    g.addIndexCell(0, 0, True)
    g.addIndexCell(0, 3, True)
    g.addIndexCell(2, 0, True)
    g.addIndexCell(1, 2, False)
    g.addIndexCell(0, 6, False)

    print(g)
    # The grid should look like this:
    # _ _ * _ _ _ _
    # _ * _ * _ * _
    # _ _ _ * _ * _
    # _ * _ * _ * _
    # _ * _ * _ _ _
    # _ * _ * _ * _
    # _ _ _ _ * _ _
    print()

    for i in range(0, g.length):
        for j in range(0, g.width):
            if (isinstance(g.grid[i][j], IndexCell)):
                currentCell = g.grid[i][j]
                print("Cell: '{0}' wordLength: '{1}'".format(currentCell, g.findLength(currentCell)))

    # Because of the way the grid is set up, the output should be this:
    # Cell: 'I(0,0,,True)' wordLength: '2'
    # Cell: 'I(0,3,,True)' wordLength: '4'
    # Cell: 'I(0,6,,False)' wordLength: '7'
    # Cell: 'I(1,2,,False)' wordLength: '6'
    # Cell: 'I(2,0,,True)' wordLength: '3'

# Test the method findBody
def test4():
    g = Grid(7, 7)
    g.addBlockedCell(0, 2)
    g.addBlockedCell(1, 1)
    g.addBlockedCell(1, 3)
    g.addBlockedCell(1, 5)
    g.addBlockedCell(2, 3)
    g.addBlockedCell(2, 5)
    g.addBlockedCell(3, 1)
    g.addBlockedCell(3, 3)
    g.addBlockedCell(3, 5)
    g.addBlockedCell(4, 1)
    g.addBlockedCell(4, 3)
    g.addBlockedCell(5, 1)
    g.addBlockedCell(5, 3)
    g.addBlockedCell(5, 5)
    g.addBlockedCell(6, 4)
    g.addIndexCell(0, 0, True)
    g.addIndexCell(0, 3, True)
    g.addIndexCell(2, 0, True)
    g.addIndexCell(1, 2, False)
    g.addIndexCell(0, 6, False)

    print(g)
    # The grid should look like this:
    # _ _ * _ _ _ _
    # _ * _ * _ * _
    # _ _ _ * _ * _
    # _ * _ * _ * _
    # _ * _ * _ _ _
    # _ * _ * _ * _
    # _ _ _ _ * _ _
    print()

    for i in range(0, g.length):
        for j in range(0, g.width):
            if (isinstance(g.grid[i][j], IndexCell)):
                currentCell = g.grid[i][j]
                currentBody = g.findBody(currentCell)
                for index in range(0, len(currentBody)):
                    currentBody[index] = currentBody[index].__str__()
                print(currentBody)

    # Because of the way the grid is set up, the output should be this:
    # ['I(0,0,,True)','L(0,1,)']
    # ['I(0,3,,True)','L(0,4,)','L(0,5,)','I(0,6,,False)']
    # ['I(0,6,,False)','L(1,6,)','L(2,6,)','L(3,6,)','L(4,6,)','L(5,6,)','L(6,6,)']
    # ['I(1,2,,False)','L(2,2,)','L(3,2,)','L(4,2,)','L(5,2,)','L(6,2,)']
    # ['I(2,0,,True)','L(2,1,)','L(2,2,)']

# Test the method findIntersections
def test5():
    pass

def main():
    test4()

if (__name__ == '__main__'):
    main()