import tkinter as tk

from Cell import BlockedCell, LetterCell


#Method used to close window
def closeWindow(event):
    event.widget.quit()

#Method to display grid for test uses
def displayMap(grid):
    window = tk.Tk()  # Create the main window

    #Binds left click to closeWindow method
    window.bind("<Button-1>", closeWindow)

    #Iterates through dict
    for i in range((grid.height)):
        for j in range(grid.length):
            strVal = grid.gridMap[(100*i+j)]
            print(strVal)
            #Adds blank space if value is "*"
            if strVal == "*":
                label = tk.Label(window, width=4, height=2, bg="black", borderwidth=1, relief="solid")
            #Adds white space if value is "_"
            elif strVal == "_":
                label = tk.Label(window, width=4, height=2, bg="white", borderwidth=1, relief="solid")
            # Adds letter of value
            else:
                label = tk.Label(window, text = strVal, width=4, height=2,fg="black", bg="white", borderwidth=1, relief="solid")
            # Each label is placed in its respective grid position
            label.grid(row=i, column=j)

    window.mainloop()


def displayGrid(g):
    window = tk.Tk()  # Create the main window

    #Binds left click to closeWindow method
    window.bind("<Button-1>", closeWindow)

    #Iterates through dict
    for i in range(g.length):
        for j in range(g.length):
            cell = g.grid[i][j]

            #Adds blank space if value is "*"
            if isinstance(cell, BlockedCell):
                label = tk.Label(window, width=4, height=2, bg="black", borderwidth=1, relief="solid")
            #Adds white space if value is "_"
            elif isinstance(cell, LetterCell):
                if (g.grid[i][j]).letter  == "":
                    label = tk.Label(window, width=4, height=2, bg="white", borderwidth=1, relief="solid")
            # Adds letter of value
            else:
                label = tk.Label(window, text = g.grid[i][j].letter, width=4, height=2,fg="black", bg="white", borderwidth=1, relief="solid")
            # Each label is placed in its respective grid position
            label.grid(row=i, column=j)

    window.mainloop()
