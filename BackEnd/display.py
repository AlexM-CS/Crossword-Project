# Created: 9-21-2024
# Last updated: 2-12-2025
# Alexander Myska, Oliver Strauss, and Brandon Knautz

# External imports:
import tkinter as tk

def closeWindow(event) -> None:
    """
    Credit: Oliver Strauss
    Closes the currently displayed window.
    """
    event.widget.quit()

def displayGrid(g) -> None:
    """
    Credit: Oliver Strauss
    Displays the main window.
    @param g: the Grid to display
    """

    window = tk.Tk()

    # Binds left click to closeWindow method
    window.bind("<Button-1>", closeWindow)

    # Iterates through Grid
    for i in range(g.size):
        for j in range(g.size):
            cell = g.grid[i][j]
            if (g.grid[i][j].letter  == ""): #Adds a white space if value is ""
                label = tk.Label(window, width=4, height=2, bg="white", borderwidth=1, relief="solid")

            elif (g.grid[i][j].letter == "*"): # Adds a black space if value is "*"
                label = tk.Label(window, width=4, height=2, bg="black", borderwidth=1, relief="solid")

            else: # Adds letter of value otherwise
                label = tk.Label(window, text = g.grid[i][j].letter, width=4, height=2,fg="black", bg="white", borderwidth=1, relief="solid")

            # Each label is placed in its respective grid position
            label.grid(row=i, column=j)

    window.mainloop()