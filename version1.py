# Crossword Generator Project
# Date: 9-19-2024
# Authors: Alexander Myska, Oliver Strauss

class Grid:
    def __init__(self, x: int, y: int):
        self.length = x
        self.height = y
        self.gridMap = dict()
        self.wordlist = list()
        
        for i in range(0, x):
            for j in range(0, y):
                self.gridMap[str(x) + "," + str(y)] = " "
    
    def getLength(self):
        return self.length
    
    def getHeight(self):
        return self.height
    
    def getGrid(self):
        return self.gridMap
    
    def getWordlist(self):
        return self.wordlist

    def setLetter(self, letter: str, x: int, y: int):
        self.gridMap[str(x) + "," + str(y)] = letter
    
    def getLetter(self, x: int, y: int):
        return self.gridMap[str(x) + "," + str(y)]
    
    def addWord(self, word: str, direction: bool, beginX: int, beginY: int):
        if (direction): # True: the word will be ACROSS
            for i in range(0, len(word)):
                if (beginX + i >= self.length):
                    raise Exception("Words cannot fit out of bounds.")
                elif (self.gridMap[str(beginX + i) + "," + str(beginY)] != word[i]):
                    raise Exception("Words cannot overwrite previous letters.")
            
            for i in range(0, len(word)): # If this line has been reached, the word acn fit in this location
                self.gridMap[str(beginX + i) + "," + str(beginY)] = word[i]
                
            self.wordlist.append(word)
            
        else: # False: the word will be DOWN
            for i in range(0, len(word)):
                if (beginY + i >= self.length):
                    raise Exception("Words cannot fit out of bounds.")
                elif (self.gridMap[str(beginX) + "," + str(beginY + i)] != word[i]):
                    raise Exception("Words cannot overwrite previous letters.")
            
            for i in range(0, len(word)): # If this line has been reached, the word acn fit in this location
                self.gridMap[str(beginX) + "," + str(beginY + i)] = word[i]
                
            self.wordlist.append(word)