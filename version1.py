# Created: 9-19-2024
# Last updated: 10-17-2024
# Alexander Myska, Oliver Strauss, and Brandon Knautz

import time

# This class
from Cell import *
from Grid import *
from display import *
from gridMakerNew import *

# Tests getEdges
def test7():
    g = initGrid(11)
    return g

def main():
    crashes = 0
    while True:
        try:
            startTime = time.time()
            g = test7()
            endTime = time.time()
            print("Time to find a working grid: {0} seconds".format(round(endTime - startTime, 5)))
            print(g.words)
            displayGrid(g)

        except:
            crashes += 1
            print("Error: {0}".format(crashes))
            continue

if (__name__ == '__main__'):
    main()