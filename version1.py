# Crossword Generator Project
# Date: 9-19-2024
# Authors: Alexander Myska, Oliver Strauss

import copy
from datetime import datetime
import random
from operator import length_hint


class Grid:
    # Initializes the Grid object with the following fields:
        # length - the grid's length in the x direction
        # height - the grid's height in the y direction
        # gridMap - a dict containing keys of x,y pairs and values of the letters stored there (initialized to None)
        # wordlist - a list containing the words currently on the grid
    # Also includes an optional argument filepath, to import a pre-made grid
    def __init__(self, rows: int, cols: int, *, filepath = None):
        try:
            self.length = rows
            self.height = cols
            self.gridMap = dict()
            self.wordlist = list()
            fileGrid = open(filepath, "r")

            for i in range(0, rows):
                line = fileGrid.readline().split(" ")
                for j in range(0, cols):
                    line[j] = line[j].strip()
                    self.gridMap[str(i) + "," + str(j)] = line[j]

        except TypeError:
            self.length = rows
            self.height = cols
            self.gridMap = dict()
            self.wordlist = list()

            for i in range(0, rows):
                for j in range(0, cols):
                    self.gridMap[str(i) + "," + str(j)] = "_"
                    
    # Overriding the string representation of the grid
    def __str__(self):
        returnString = "GRID:\n"
        values = list(self.gridMap.values())
        valueNum = 0
        for i in range(0, self.length):
            for j in range(0, self.height):
                returnString += values[valueNum]
                if (j < self.height - 1):
                    returnString += " "
                valueNum += 1
            if (i < self.length - 1):
                returnString += "\n"
        return returnString
    
    # Returns the length of the grid
    def getLength(self):
        return self.length
    
    # Returns the height of the grid
    def getHeight(self):
        return self.height
    
    # Returns the dict object that represents the grid
    def getGrid(self):
        return self.gridMap
    
    # Returns a list containing the words currently on the grid
    def getWordlist(self):
        return self.wordlist

    # Gets the letter currently at the coordinates x, y 
    def getLetter(self, row: int, col: int):
        return self.gridMap[str(row) + "," + str(col)]

    # Adds a word (and by extension, its letters) to the grid, if possible
    def addWord(self, word: str, direction: bool, beginRow: int, beginCol: int):
        if not (word.isalpha()):
            raise Exception("Words must be alphabetic characters only.")
        word = word.upper()
        if (direction): # True: the word will be DOWN
            for i in range(0, len(word)):
                current = self.gridMap[str(beginRow + i) + "," + str(beginCol)]
                if (beginRow + i >= self.length):
                    raise Exception("Words cannot fit out of bounds.")
                elif (current != word[i] and current != "_"):
                    raise Exception("Words cannot overwrite previous letters.")
            
            for i in range(0, len(word)): # If this line has been reached, the word can fit in this location
                self.gridMap[str(beginRow + i) + "," + str(beginCol)] = word[i]
                
            self.wordlist.append(word)
            
        else: # False: the word will be ACROSS
            for i in range(0, len(word)):
                current = self.gridMap[str(beginRow) + "," + str(beginCol + i)]
                if (beginCol + i >= self.length):
                    raise Exception("Words cannot fit out of bounds.")
                elif (current != word[i] and current != "_"):
                    raise Exception("Words cannot overwrite previous letters.")
            
            for i in range(0, len(word)): # If this line has been reached, the word can fit in this location
                self.gridMap[str(beginRow) + "," + str(beginCol + i)] = word[i]
                
            self.wordlist.append(word)

    # Adds a new blocked space to the grid
    def addBlocked(self, x: int, y: int):
        if (self.gridMap[str(x) + "," + str(y)] == "_"):
            self.gridMap[str(x) + "," + str(y)] = "*"

    # Changes a grid space's state to empty
    def addEmpty(self, x: int, y: int):
        self.gridMap[str(x) + "," + str(y)] = "_"

    # Checks to see where new words should be starting
    def findNextOpen(self):
        for row in range(0, self.length):
            for col in range(0, self.height):
                x = 0
                y = 0
                # First, we check for availability DOWN
                if (self.gridMap[str(row) + "," + str(col)] != "*") and (col + 1 < self.length):
                    x = 1
                    while (col + x < self.length):
                        if (self.gridMap[str(row) + "," + str(col + x)] == "_"):
                            x += 1
                        else:
                            break
                # Next, we check for availability DOWN
                if (self.gridMap[str(row) + "," + str(col)] != "*") and (row + 1 < self.height):
                    y = 1
                    while (row + 1 < self.height):
                        if (self.gridMap[str(row + y) + "," + str(col)] == "_"):
                            y += 1
                        else:
                            break
                # Finally, if either x or y is greater than 0, return
                # Returns a tuple in the format (int i, int j, int x, int y)
                    # i - target row
                    # j - target column
                    # x - length of the word ACROSS, or False if not available
                    # y - length of the word DOWN, or False if not available
                if (x > 1) or (y > 1):
                    if (x <= 1):
                        return (row, col, False, y)
                    elif (y <= 1):
                        return (row, col, x, False)
                    return (row, col, x, y)
            
class Generator:
    # Initializes the word generator with the following fields:
        # seed - the generator's starting seed for RNG
        # name - a name for the generator to display when printed out
        # data - a list of words for it to hold
    def __init__(self, name, letter: str):
        self.seed = datetime.now().timestamp()
        self.name = name
        self.data = open("../Crossword_Generator/Crossword Databases/{0}_words_converted.txt".format(letter), "r").read().split(" ")

    # Overriding the default string representation to show the properties of this generator
    def __str__(self):
        returnString = "Name:\n " + self.name.__str__() +"\nSeed:\n " + self.seed.__str__() + "\nData:\n " + self.data.__str__()
        return returnString
    
    # Selects a random word from the list of data, containing the specified chars at the specified indices
    def newWord(self, length: int, indices: list, chars: list):
        copiedData = copy.deepcopy(self.data)
        i = 0
        try:
            while (i < len(copiedData)):
                word = copiedData[i]
                for j in range(0, len(indices)):
                    if (word[indices[j]] != chars[indices[j]] or len(word) != length):
                        copiedData.remove(word)
                        i -= 1
                        break
                i += 1
        except IndexError:
            print("ERROR OCCURRED.")
            print(copiedData[i - 1])
            quit()
        
        random.seed(self.seed)
        i = random.randrange(0, len(copiedData))
        return copiedData[i]

def main():
    print("start\n")

    grid = Grid(11, 11, filepath="../Crossword-Project/output.txt")
    grid.addWord("ARE", False, 0, 0)
    print(grid)
    tup = grid.findNextOpen()
    if (tup[3] != False):
        gen = Generator("gen", grid.gridMap[str(tup[0]) + "," + str(tup[1])])
        print(gen.newWord(tup[3], [0], [grid.gridMap[str(tup[0]) + "," + str(tup[1])]]))

if (__name__ == "__main__"):
    main()