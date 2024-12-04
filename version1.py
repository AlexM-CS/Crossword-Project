# Created: 9-19-2024
# Last updated: 11-19-2024
# Alexander Myska, Oliver Strauss, and Brandon Knautz

import time

from Cell import *
from Grid import *
from display import *
from gridMakerNew import *

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
        except:
            continue
        finally:
            numGrids += 1
            print(f"Success Rate: {success} / {numGrids}")

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