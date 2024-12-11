# Created: 12-10-2024
# Alexander Myska, Oliver Strauss, and Brandon Knautz

import random

from BackEnd.gridMakerNew import initGrid, genHints
from BackEnd.Grid import *
from BackEnd.OpenAITest.OpenAIAPITest import get_hints

def run(size: int):
    g = initGrid(size)
    jsonGrid = g.convert()

    cellies = sorted(g.indexCells, key=lambda cell: (cell.x, cell.y))

    hints = []
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', "r", "s", "t", "u",
               "v", "w", "x", "y", "z"]
    for cell in g.indexCells:
        randlet = random.choice(letters)
        hints.append(("Hint_" + randlet))
        letters.remove(randlet)

    for i in range(len(hints)):
        jsonGrid[i]["hint"] = hints[i]

    return g, jsonGrid, hints

if __name__ == "__main__":
    run(9)