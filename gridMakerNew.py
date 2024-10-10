# 10-10-2024
# Alexander Myska, Oliver Strauss, Brandon Knautz

# This class will be used to make grids, this time by looking for words first

def createEdges(size: int):
    while True: # This will repeat until a valid grid is created
        pass
        # Iterate for i < size
            # Iterate for j < size
                # Create cells with coordinates i,j

        # Set int partitions = 0
        # While partitions < 2
            # Try to create a partition on each edge

        # Generate a bridge between the disconnected parts

        # Loop over the edges and the bridge, and try to give them words
        # Check if all the edges have words now
            # If they do, break

    # Return a list of words that we will build off from
    pass

def fill(grid, size: int):
    # Set int wordSize = size - 2

    while True: # Loop until about 70% of the grid has letters
        pass
        # Run diagonal check
            # Try to create a word of length wordSize, perpendicular to the bridge
        # Run diagonal check
            # Try to create a word of length wordSize, parallel to the bridge
        # If wordSize is > 3, wordSize -= 2
        # Minimum wordSize is 3

    # After all letters are in place, any Cell without a letter becomes a BlockedCell
    # Return the completed grid

    pass

def main():
    g = createEdges(11)
    g = fill(g, 11)

if __name__ == "__main__":
    main()