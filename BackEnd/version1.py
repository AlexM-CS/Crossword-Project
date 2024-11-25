# Created: 9-19-2024
# Last updated: 11-19-2024
# Alexander Myska, Oliver Strauss, and Brandon Knautz

import time

from BackEnd.gridMakerNew import *

# Tests getEdges
def test7():
    g,indexCells = initGrid(9)

    print(indexCells)

    return g

def test8():
    while True:
        try:
            g = createEdges(9)
        except:
            continue


#Special version of main() to get needed data for frontEnd
def returnMain(size):
    crashes = 0
    while True:
        try:
            g, indexCells = initGrid(size)
            break
        except:
            crashes += 1
            print("Error: {0}".format(crashes))
    return g,indexCells





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
        except :
            crashes += 1
            print("Error: {0}".format(crashes))

if (__name__ == '__main__'):
    main()