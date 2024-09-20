# Crossword Generator Project
# Date: 9-19-2024
# Authors: Alexander Myska, Oliver Strauss

import copy
from datetime import datetime
import random


class Grid:
    # Initializes the Grid object with the following fields:
        # length - the grid's length in the x direction
        # height - the grid's height in the y direction
        # gridMap - a dict containing keys of x,y pairs and values of the letters stored there (initialized to None)
        # wordlist - a list containing the words currently on the grid
    def __init__(self, rows: int, cols: int):
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
            
class Generator:
    # Initializes the word generator with a seed
    def __init__(self):
        self.seed = datetime.now().timestamp()
        self.data = ["RED","REGISTER","REJECT","RENT","ROPE","OTHER","OIL","ENTER","THREE","TREK","OBTUSE","OBESE","LAMP","LIGHTER","LOW","EXIT","EPITOME"]
    
    # Selects a random word from the list of data
    def newWord(self, length: int):
        copiedData = copy.deepcopy(self.data)
        i = 0
        while (i < len(copiedData)):
            word = copiedData[i]
            if (len(word) != length):
                copiedData.remove(word)
                i -= 1
            i += 1

        random.seed(self.seed)
        i = random.randrange(0, len(copiedData))
        return copiedData[i]
    
    # Selects a random word from the list of data, containing the specified chars at the specified indices
    def newWordContains(self, length: int, indices: list, chars: list):
        copiedData = copy.deepcopy(self.data)
        i = 0
        while (i < len(copiedData)):
            word = copiedData[i]
            for j in range(0, len(indices)):
                if (word[indices[j]] != chars[indices[j]] or len(word) != length):
                    copiedData.remove(word)
                    i -= 1
                    break
            i += 1
        
        random.seed(self.seed)
        i = random.randrange(0, len(copiedData))
        return copiedData[i]

def main():
    print("start\n")

    g = Grid(8, 8)
    g.addWord("RED", True, 0, 0)
    g.addWord("REGISTER", False, 0, 0)
    print(g)
    print()
    
    r = Generator()
    print(r.newWord(50))
    print(r.newWordContains(50, [0], ["R"]))

if (__name__ == "__main__"):
    main()