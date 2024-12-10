# Created: 9-19-2024
# Last updated: 12-5-2024
# Alexander Myska, Oliver Strauss, and Brandon Knautz

# This file is used for testing only.

from BackEnd.gridMakerNew import *


#Special version of main() to get needed data for frontEnd
def returnMain(size):
    crashes = 0
    while True:
        try:
            g, indexCells,hints = initGrid(size)
            print(g)
            break
        except:
            crashes += 1
            print("Error: {0}".format(crashes))
    return g,indexCells,hints

# Tests the success rate of full grids
def test9():
    numGrids = 0
    success = 0
    while True:
        try:
            g = initGrid(11)
            print(g.words)
            displayGrid(g)
            success += 1
        except RuntimeError as e:
            print(e)
            continue
        except ValueError as e:
            print(e)
            continue
        finally:
            numGrids += 1
            print(f"Success Rate: {success} / {numGrids}")

# Tests the success rate of full grids
def test10():
    numGrids = 0
    success = 0
    while True:
        g = initGrid(11)
        print(g)
        print(g.words)
        input()

# Tests getEdges
def test7():
    g = initGrid(9)
    return g

def test8():
    while True:
        try:
            g = createEdges(11)
        except:
            continue

def main():
    test9()

if (__name__ == '__main__'):
    main()