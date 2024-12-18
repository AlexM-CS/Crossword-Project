# Created: 11-18-2024
# Last updated: 12-13-2024
# Alexander Myska, Oliver Strauss, and Brandon Knautz

# External imports:
from flask import Flask, render_template

from BackEnd.backendMain import run

debugMode = False

# Sets up folder for HTML tabs
app = Flask(__name__, template_folder='FrontEnd/templates',static_folder='FrontEnd/static')

@app.route('/menu')
def menu():
    # backend.tester.printTest()
    # create grid
    return render_template("Menu.html")


@app.route('/about')
def about():
    # backend.tester.printTest()
    # create grid
    return render_template("about.html")

@app.route('/grid9')
def grid9():
    # Run the backend, and collect necessary data
    jsonIndexCells, jsonBlockedCells, hints = run(9,debugMode)

    #Runs html file with a dictionary of Index Cells
    return render_template("grid.html", size = 9, jsonIndex = jsonIndexCells, hints = hints, blockedTiles = jsonBlockedCells)

@app.route('/grid11')
def grid11():
    # Run the backend, and collect necessary data
    jsonIndexCells, jsonBlockedCells, hints = run(11, debugMode)

    # Runs html file with a dictionary of Index Cells
    return render_template("grid.html", size = 11, jsonIndex = jsonIndexCells, hints = hints, blockedTiles = jsonBlockedCells)

@app.route('/grid13')
def grid13():
    # Run the backend, and collect necessary data
    jsonIndexCells, jsonBlockedCells, hints = run(13, debugMode)

    # Runs html file with a dictionary of Index Cells
    return render_template("grid.html", size = 13, jsonIndex = jsonIndexCells, hints = hints, blockedTiles = jsonBlockedCells)

app.run(host='127.0.0.1', port=7000, debug = debugMode)