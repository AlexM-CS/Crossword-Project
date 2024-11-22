# Created: 9-19-2024
# Last updated: 11-19-2024
# Alexander Myska, Oliver Strauss, and Brandon Knautz

import time

from Cell import *
from Grid import *
from display import *
from gridMakerNew import *

# Tests getEdges
def test7():
    g = initGrid(9)
    return g

def test8():
    while True:
        try:
            g = createEdges(9)
        except:
            continue

def main():
    crashes = 0
    while True:
        try:
            startTime = time.time()
            g = test7()
            endTime = time.time()
            print("Time to find a working grid: " + str(round(endTime - startTime, 5)))
            print(g.words)
            displayGrid(g)
        except:
            crashes += 1
            print("Error: {0}".format(crashes))

if (__name__ == '__main__'):
    main()