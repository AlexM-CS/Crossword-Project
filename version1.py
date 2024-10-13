# 9-30-2024
# Alexander Myska, Oliver Strauss, Brandon Knautz

# This class will be used to test our code for its intended behavior

from Cell import *
from Grid import *
from display import *

def wait():
    input()

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
    # Because of the way the grid is set up, the output should be this:
    # * _ _ _
    # _ * _ _
    # _ _ * _
    # _ _ _ *

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
    # A _ * A _ _ D
    # _ * D * _ * _
    # A _ _ * _ * _
    # _ * _ * _ * _
    # _ * _ * _ _ _
    # _ * _ * _ * _
    # _ _ _ _ * _ _
    # (A and D will be "_" when printed)
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
    # A _ * A _ _ D
    # _ * D * _ * _
    # A _ _ * _ * _
    # _ * _ * _ * _
    # _ * _ * _ _ _
    # _ * _ * _ * _
    # _ _ _ _ * _ _
    # (A and D will be "_" when printed)
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
    # A _ * A _ _ D
    # _ * D * _ * _
    # A _ _ * _ * _
    # _ * _ * _ * _
    # _ * _ * _ _ _
    # _ * _ * _ * _
    # _ _ _ _ * _ _
    # (A and D will be "_" when printed)
    print()

    for i in range(0, g.length):
        for j in range(0, g.width):
            if (isinstance(g.grid[i][j], IndexCell)):
                currentCell = g.grid[i][j]
                currentCell.body = g.findBody(currentCell)
                print("Cell: '{0}' intersections: '{1}'".format(currentCell, g.findIntersections(currentCell)))

    # Because of the way the grid is set up, the output should be this:
    # Cell: 'I(0,0,,True)' intersections: '1'
    # Cell: 'I(0,3,,True)' intersections: '2'
    # Cell: 'I(0,6,,False)' intersections: '3'
    # Cell: 'I(1,2,,False)' intersections: '2'
    # Cell: 'I(2,0,,True)' intersections: '2'

# Test the method initIndexCells()
def test6():
    g = Grid(5, 5)
    g.addBlockedCell(0, 2)
    g.addBlockedCell(1, 1)
    g.addBlockedCell(1, 3)
    g.addBlockedCell(3, 1)
    g.addBlockedCell(3, 3)
    g.addBlockedCell(4, 2)
    g.addHybridCell(0, 0)
    g.addIndexCell(0, 3, True)
    g.addIndexCell(0, 4, False)
    g.addIndexCell(1, 2, False)
    g.addIndexCell(2, 0, True)
    g.addIndexCell(4, 0, True)
    g.addIndexCell(4, 3, True)

    print(g)
    # The grid should look like this:
    # H _ * A D
    # _ * D * _
    # A _ _ _ _
    # _ * _ * _
    # A _ * A _
    # (H, A, and D will be "_" when printed)
    print()

    g.initIndexCells()

    for i in range(g.length):
        for j in range(g.width):
            if (isinstance(g.grid[i][j], HybridCell)):
                currentCell = g.grid[i][j]
                for index in range(0, len(currentCell.across.body)):
                    currentCell.across.body[index] = currentCell.across.body[index].__str__()
                for index in range(0, len(currentCell.down.body)):
                    currentCell.down.body[index] = currentCell.down.body[index].__str__()
                print("Cell: '{0}'".format(currentCell))
                print("across: '{0}'".format(currentCell.across))
                print("across.wordLength: '{0}'".format(currentCell.across.wordLength))
                print("across.body: '{0}'".format(currentCell.across.body))
                print("across.intersections: '{0}'".format(currentCell.across.intersections))
                print("down: '{0}'".format(currentCell.down))
                print("down.wordLength: '{0}'".format(currentCell.down.wordLength))
                print("down.body: '{0}'".format(currentCell.down.body))
                print("down.intersections: '{0}'".format(currentCell.down.intersections))
                wait()

            elif (isinstance(g.grid[i][j], IndexCell)):
                currentCell = g.grid[i][j]
                for index in range(0, len(currentCell.body)):
                    currentCell.body[index] = currentCell.body[index].__str__()
                print("Cell: '{0}'".format(currentCell))
                print("wordLength: '{0}'".format(currentCell.wordLength))
                print("body: '{0}'".format(currentCell.body))
                print("intersections: '{0}'".format(currentCell.intersections))
                wait()

    # Because of the way the grid is set up, the output should be this:

    # Cell: 'H(0,0,)'
    # across 'I(0,0,,True)'
    # across.wordLength: '2'
    # across.body: '['H(0,0,)','L(0,1,)']'
    # across.intersections: '1'
    # down: 'I(0,0,,False)'
    # down.wordLength: '5'
    # down.body: '['H(0,0,)','L(1,0,)','I(2,0,,True)','L(3,0,)','I(4,0,,True)']'
    # down.intersections: '3'

    # Cell: 'I(0,3,,True)'
    # wordLength: '2'
    # body: '['I(0,3,,True)','I(0,4,,False)']'
    # intersections: '1'

    # Cell: 'I(0,4,,False)'
    # wordLength: '5'
    # body: '['I(0,4,,False)','L(1,4,)','L(2,4,)','L(3,4,)','L(4,4,)']'
    # intersections: '3'

    # Cell: 'I(1,2,,False)'
    # wordLength: '3'
    # body: '['I(1,2,,False)','L(2,2,)','L(3,2,)']'
    # intersections: '1'

    # Cell: 'I(2,0,,True)'
    # wordLength: '5'
    # body: '['I(2,0,,True)','L(2,1,)','L(2,2,)','L(2,3,)','L(2,4,)']'
    # intersections: '3'

    # Cell: 'I(4,0,,True)'
    # wordLength: '2'
    # body: '['I(4,0,,True)','L(4,1,)']'
    # intersections: '1'

    # Cell: 'I(4,3,,True)'
    # wordLength: '2'
    # body: '['I(4,3,,True)','L(4,4,)']'
    # intersections: '1'

def test7():
    g = Grid(5, 5)
    g.addBlockedCell(0, 2)
    g.addBlockedCell(1, 1)
    g.addBlockedCell(1, 3)
    g.addBlockedCell(3, 1)
    g.addBlockedCell(3, 3)
    g.addBlockedCell(4, 2)
    g.addHybridCell(0, 0)
    g.addIndexCell(0, 3, True)
    g.addIndexCell(0, 4, False)
    g.addIndexCell(1, 2, False)
    g.addIndexCell(2, 0, True)
    g.addIndexCell(4, 0, True)
    g.addIndexCell(4, 3, True)

    print(g)
    # The grid should look like this:
    # H _ * A D
    # _ * D * _
    # A _ _ _ _
    # _ * _ * _
    # A _ * A _
    # (H, A, and D will be "_" when printed)
    print()

    g.initIndexCells()
    sortedCells = g.sortIndexCells()
    for i in range(len(sortedCells)):
        sortedCells[i] = sortedCells[i].__str__()
    print(sortedCells)

    # Because of the way the grid is set up, the output should be this:
    # ['I(0,0,,False)','I(0,4,,False)','I(2,0,,True)','I(0,0,,True)','I(0,3,,True)','I(1,2,,False)','I(4,0,,True)','I(4,3,,True)']

def main():

    g = Grid(5, 5)
    displayGrid(g)
    test7()

if (__name__ == '__main__'):
    main()