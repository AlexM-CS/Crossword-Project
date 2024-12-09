from json.decoder import JSONArray
from time import perf_counter

from flask import Flask, render_template, json
import requests

# import sys
# import os
# directory_path = "Crossword-Project-main/backend"
# sys.path.append(directory_path)

#WordBackend.run()

#print(backend.Grid(9, 9))
import BackEnd
import BackEnd.Cell

import BackEnd.gridMakerNew
import BackEnd.Grid
from BackEnd.Cell import HybridCell
from BackEnd.display import displayGrid
from BackEnd.gridMakerNew import initGrid
from BackEnd import display
from BackEnd.version1 import returnMain


def process_grid_with_direction(grid_json,grid):
    """
    Iterate through the grid JSON, update each cell with direction.
    """
    indexCells = grid.indexCells
    for i in range(len(indexCells)):
        celly = indexCells[i]
        if isinstance(celly, HybridCell):
            indexCells.append(celly.down)

    for i in range(len(indexCells)):
        for j in range(len(grid_json)):
            if indexCells[i].word ==grid_json[j]['word']:
                grid_json[j]["direction"] = indexCells[i].getDirection()


    return grid_json


#Sorts through the list of index cells and sorts them based on row then col
def sortotherIndexs(grid_json):
    sorted_grid = sorted(grid_json, key=lambda x: (x["row"], x["column"]))
    return sorted_grid


def addHints(jsonIndex, hints):
    print(hints)
    print(len(hints))
    print(len(jsonIndex))
    for i in range(len(hints)):
        jsonIndex[i]["hint"] = hints[i]
    return jsonIndex

def runBackend(size):
    grid, jsonGrid, hints = returnMain(size)

    jsonGrid = jsonGrid['grid_data']
    # Gives indexCells used in js file a direction

    jsonGrid = process_grid_with_direction(jsonGrid, grid)

    # Sorts indexCells
    jsonGrid = sortotherIndexs(jsonGrid)
    jsonGrid = addHints(jsonGrid, hints)


    print(grid)

    print(jsonGrid)
    print(grid.blockedCells)
    return grid,jsonGrid,hints

#Sets up folder for HTML tabs
app = Flask(__name__, template_folder='templates',static_folder='static')


@app.route('/menu')#END OF URL htttps/somthing/poop
def menu():
   # backend.tester.printTest()
    #create grid

    return render_template("Menu.html")


#Page to run game of grid size 9
@app.route('/grid9')
def grid9():
    size = 9
    #Runs all backend and collects needed data

    grid, jsonGrid ,hints = runBackend(size)


    #Runs hmtl file with a dictionary of indexCells
    return render_template("grid.html",size = size, jsonIndex=jsonGrid, hints=hints,blockedTiles=grid.blockedCells)

#Page to run game of grid size 11
@app.route('/grid11')
def grid11():
    size = 11
    # Runs all backend and collects needed data

    grid, jsonGrid, hints = runBackend(size)
    # Runs hmtl file with a dictionary of indexCells
    return render_template("grid.html", size = size,jsonIndex=jsonGrid, hints=hints, blockedTiles=grid.blockedCells)


    #Pass in griddddd

#Page to run game of grid size 12
@app.route('/grid13')
def grid13():
    size = 13
    # Runs all backend and collects needed data

    grid, jsonGrid, hints = runBackend(size)

    # Runs hmtl file with a dictionary of indexCells
    return render_template("grid.html", size = size,jsonIndex=jsonGrid, hints=hints, blockedTiles=grid.blockedCells)




app.run(host='127.0.0.1', port=5000, debug=True)

