# Created: 9-19-2024
# Last updated: 12-13-2024
# Alexander Myska, Oliver Strauss, and Brandon Knautz

# This file is used for testing only.

# External imports:
import time

# When running from here, use these imports:
# from gridMakerNew import *

# When running from main, use these imports:
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
    startTime = time.time_ns()

    while True:
        try:
            g = initOld(11)
            success += 1
        except Exception as e:
            print(e)
        finally:
            numGrids += 1
            print(f"Success Rate: {success} / {numGrids}")
            if (numGrids > 9):
                print(f"{(time.time_ns() - startTime)} nanoseconds")
                print(f"{round((time.time_ns() - startTime) / 1000000000, 4)} seconds")
                quit()

# Tests the success rate of full grids
def test10():
    numGrids = 0
    success = 0
    while True:
        g = initGrid(9)
        print(g)
        print(g.indexCells)
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

def test11():
    g = generateBridge(9)
    createEdges(g)
    print(g.getEdges())

def main():
    test10()

if (__name__ == '__main__'):
    main()