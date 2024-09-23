import random
from _ast import pattern
from copy import deepcopy
from random import Random

from pygame.examples import grid

from display import displayMap, displayGrid


#Initalizes seed grid
def makeSeedGrid():
    rows = 11  # Total rows
    pattern = []
    row1 = ["_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_"]
    row2 = ["_", "*", "_", "*", "_", "*", "_", "*", "_", "*", "_"]
    for i in range(rows):
        if i % 2 == 0:
            pattern.append(row1)
        else:
            pattern.append(row2)
    return pattern


#Prints each row of given grid
def printGrid(grid):
    for row in grid:
        print(row)


#Helper method to check vertical axis of grid
def check_value_vertical(matrix, value, index):
    rows = len(matrix)
    cols = index

    for row in range(rows):
            if matrix[row][cols] == value:
                return True  # Value found
    return False


#Takes updated grid and adds initial blank tiles on edges
def updateEdges(grid):

    #Checks row to see if it has blank tile
    '''
    if "*" not in grid[0]:
        grid[0][random.randint(1, len(grid[0])-1)] = "*"

    if "*" not in grid[len(grid)-1]:
        grid[0][random.randint(1, len(grid[0])-1)] = "*"


    #Checks columns to see if it has blank tiles
    if not check_value_vertical(grid, "*",0):
        grid[random.randint(1, len(grid[0])-1)][0] = "*"
    if not check_value_vertical(grid, "*", len(grid[0])-1):
        grid[random.randint(1, len(grid[0])-1)][len(grid[0])-1] = "*"

    return grid
    '''
    randCoordinate = random.randrange(3, len(grid) - 4)
    grid[0][randCoordinate] = "*"
    grid[len(grid)-1][len(grid) - 1 - randCoordinate] = "*"
    grid[len(grid) - 1 - randCoordinate][0] = "*"
    grid[randCoordinate][len(grid)-1] = "*"

    return grid





#Takes  grid and adds initial blank tiles
def addBlanks(grid):
    newGrid = [row.copy() for row in grid]  # Deep copy the grid

    #Dictionary that dictates direction tile is placed
    x, y = 0, 0
    dirs = {1: (-1, 0),
            2: (1, 0),
            3: (0, -1),
            4: (0, 1)}

    for i in range(1,len(grid),2):

        for j in range(1,len(grid[i]),2):
            #Random val that dictates direction tiles placed
            valChance = random.randint(1,4)

            x,y = dirs[valChance]

            #print(x,y)
            #Random val that to decide if a tile is placed or not
            valChance = random.randint(1,100)
            if valChance > 70:
                newGrid[i+y][j+x] = "*"

    printGrid(newGrid)

    newGrid = updateEdges(newGrid)
    '''
    wordDex = []
    wordNum = 1
    for row in range(0, len(newGrid)):
        for column in range(0, len(newGrid[row])):
            
            addWord = True
            if wordNum == 1:
                pass
            else:
                for eachWord in wordDex:
                    if eachWord.checkCoord((row, column)):
                        addWord = False
            if addWord:
                currentWord = WordBlank(wordNum)
                x1 = row
                y1 = column
                while (x1 + 1 < len(newGrid)):
                    x1 += 1
                    if newGrid[x1][column] == "*":
                        currentWord.addcoord((x1, column))
                x1 = row
                while (x1 - 1 >= 0):
                    x1 -= 1
                    if newGrid[x1][column] == "*":
                        currentWord.addcoord((x1, column))

                while (y1 + 1 < len(newGrid[0])):
                    y1 += 1
                    if newGrid[row][y1] == "*":
                        currentWord.addcoord((row, y1))
                y1 = column
                while (y1 - 1 >= 0):
                    y1 -= 1
                    if newGrid[row][y1] == "*":
                        currentWord.addcoord((row, y1))
                wordNum+=1
    '''






    return newGrid



def markAcrossAndDownTiles(grid):
    for row in range(len(grid)):
        for column in range(len(grid[0])):
            if grid[row][column] != "*":
                if column == len(grid[0]) - 1:
                    pass
                elif column == 0:
                    if grid[row][column+1] != "*":
                        grid[row][column] = "A"
                elif grid[row][column-1] == "*" and (grid[row][column+1] != "*" or column+1 == len(grid[0])):
                    grid[row][column] = "A"
                if row == len(grid) - 1:
                    pass
                elif row == 0:
                    if grid[row+1][column] != "*":
                        if grid[row][column] == "A":
                            grid[row][column] = "H"
                        else:
                            grid[row][column] = "D"
                elif grid[row-1][column] == "*" and (grid[row + 1][column] != "*" or row + 1 == len(grid)):
                    if grid[row][column] == "A":
                        grid[row][column] = "H"
                    else:
                        grid[row][column] = "D"

def getAcrossAndDownTileIndexes(grid):
    down = []
    across = []
    for row in range(len(grid)):
        for column in range(len(grid[0])):
            if grid[row][column] == "H":
                down.append((row, column))
                across.append((row, column))
            if grid[row][column] == "D":
                down.append((row, column))
            if grid[row][column] == "A":
                across.append((row, column))
    return across, down



#class representive of each blank word spot in the crossword generation
class WordBlank:
    def __init__(self, wordNum):
        self.wordNum = wordNum
        self.coordinates = []

    def addcoord(self, spot):
        self.coordinates.append(spot)

    def checkCoord(self, spot):
        return spot in self.coordinates
    def decreaseWordNum(self):
        self.wordNum-=1


#Takes grid and writes it to a file 
def write_to_file(filename,grid):
    lines = []
    for i in range(len(grid)):
        lines.append(" ".join(grid[i]))
    print(lines)

    # Open the file in write mode
    with open(filename, 'w') as file:
        for line in lines:
            file.write(line + '\n')  # Write each line followed by a newline

    # Example usage




def main():
    seedGrid = makeSeedGrid()
    printGrid(seedGrid)

    newGrid = addBlanks(seedGrid)
    printGrid(newGrid)
    write_to_file('output.txt', newGrid)


    othergrid = deepcopy(newGrid)
    markAcrossAndDownTiles(othergrid)
    write_to_file('output1.txt', othergrid)
    displayGrid(othergrid)










if (__name__ == "__main__"):
    main()
