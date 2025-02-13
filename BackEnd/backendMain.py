# Created: 12-10-2024
# Last updated: 2-12-2025
# Alexander Myska, Oliver Strauss, and Brandon Knautz

# This file runs the BackEnd of the Crossword Project.

# External imports:
import random

# When running from test file, use these imports:
# from gridMakerNew import initGrid
# from Grid import *
# from OpenAITest.OpenAIAPITest import get_hints

# When running from main, use these imports:
from BackEnd.gridMakerNew import initGrid
from BackEnd.Grid import *
from BackEnd.OpenAITest.OpenAIAPITest import get_hints

def run(size: int, debug : bool = False):
    """
    Credit: Alexander Myska and Oliver Strauss
    Runs the BackEnd, and returns data that will be used in the display.
    """

    # First, we make the grid
    g = initGrid(size)

    # Next, convert the grid a format that can be used by the FrontEnd
    jsonIndex = g.convertIndexCells()
    jsonBlocked = g.blockedCells
    # print(jsonBlocked) # DEBUG LINE

    if (debug): # If debug mode is enabled, generate dummy hints so we save money lol:
        hints = []
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', "r", "s", "t",
                   "u", "v", "w", "x", "y", "z"]
        count = 0
        for cell in g.indexCells:

            if (isinstance(cell, HybridCell)):
                hints.append(("Hint_" + letters[count]))

                count += 1

                hints.append(("Hint_" + letters[count]))
            else:
                hints.append(("Hint_" + letters[count]))

            count += 1

    else: # Otherwise, generate the hints for the list of sorted IndexCells
        sortedCells = sorted(g.indexCells, key=lambda cell: (cell.x, cell.y))

        words = list()
        for cell in sortedCells:
            if isinstance(cell, HybridCell):
                words.append(cell.across.word)
                words.append(cell.down.word)

            else:
                words.append(cell.word)

        hints = get_hints(words)


    # Add hints to each of the words in jsonGrid
    for i in range(len(hints)):
        if hints[i] != '':
            jsonIndex[i]["hint"] = hints[i]

    return jsonIndex, jsonBlocked, hints