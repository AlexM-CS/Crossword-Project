# Created: 9-19-2024
# Last updated: 2-12-2025
# Alexander Myska, Oliver Strauss, and Brandon Knautz

# This file is used for testing only.
# As the project evolved and changed, we removed obsolete tests or ones that would
# no longer work as a result of large-scale changes, which is why there is little organization.

# External imports:
import time

# When running from here, use these imports:
from gridMakerNew import *
from display import *

# When running from main, use these imports:
# from BackEnd.gridMakerNew import *

# Special version of main() to get needed data for frontEnd
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
            g = initGridOld(11)
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
    g = initGridNew(11)
    return g

def test11():
    g = generateBridge(9)
    print(g.getEdges())

def test3():
    while True:
        hundredGridsTime = 0
        numGrids = 0
        while (numGrids < 100):
            startTime = time.time_ns()
            g = initGridNew(11)
            print(g)
            endTime = round((time.time_ns() - startTime) / 1000000000, 5)
            print(f"Time: {endTime} seconds")
            hundredGridsTime += endTime
            numGrids += 1
        print(f"Total Time: {round(hundredGridsTime, 5)} seconds")
        input()

def test2():
    startTime = time.time_ns()
    g = initGridNew(11)
    print(g)
    print(g.words)
    print(f"Time: {round((time.time_ns() - startTime) / 1000000000, 5)}")
    displayGrid(g)

def test5():
    g = initGrid(9)
    print(g)
    print(g.indexCells)
    displayGrid(g)

def main():
    test5()

if (__name__ == '__main__'):
    main()