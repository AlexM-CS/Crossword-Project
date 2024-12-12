# Created: 12-10-2024
# Last updated: 12-11-2024
# Alexander Myska, Oliver Strauss, and Brandon Knautz

# This file runs the BackEnd of the Crossword Project.

import random

from BackEnd.gridMakerNew import initGrid
from BackEnd.Grid import *
from BackEnd.OpenAITest.OpenAIAPITest import get_hints

def run(size: int, debug : bool = False):
    """ Runs the BackEnd, and returns data that will be used in the display. """

    # First, we make the grid
    g = initGrid(size)

    # Next, convert the grid a format that can be used by the FrontEnd
    jsonGrid = g.convert()

    # If debug mode is enabled, generate dummy hints so we save money lol
    if (debug):
        hints = []
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', "r", "s", "t",
                   "u", "v", "w", "x", "y", "z"]
        for cell in g.indexCells:
            randlet = random.choice(letters)
            if (isinstance(cell, HybridCell)):
                hints.append(("Hint_" + randlet))

                letters.remove(randlet)
                randlet = random.choice(letters)
                hints.append(("Hint_" + randlet))
            else:
                hints.append(("Hint_" + randlet))

            letters.remove(randlet)

    else:
        # Generate the hints for the list of sorted IndexCells
        sortedCells = sorted(g.indexCells, key=lambda cell: (cell.x, cell.y))
        words = list()


        for cell in sortedCells:
            if(isinstance(cell, HybridCell)):
                words.append(cell.down.word)
                words.append(cell.across.word)
            else:
                words.append(cell.word)
        hints = get_hints(words)

    # Add hints to each of the words in jsonGrid
    for i in range(len(hints)):
        jsonGrid[i]["hint"] = hints[i]

    return g, jsonGrid, hints

if __name__ == "__main__":
    run(9)