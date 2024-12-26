// Created:
// Last updated: 12-12-2024
// Alexander Myska, Oliver Strauss, and Brandon Knautz

let grid = document.querySelector('#game')//html representation of the gid
let tiles = []; // 2-D array holding html divs in grid
let direction = true// Boolean indicating direction of user input
let currentTile;//Tile user input typing occurs
let autocheck = false//Toggle of autocheck


document.getElementById("endScreen").classList.add("hidden"); // Hides end screen



let tempGrid = document.createDocumentFragment(); //Temporary grid tiles are appended too

//Nested for loop iterating over rows and cols
Array.from({length: size}).forEach((_, rowIdx) => {

    //Creates row
    let row = document.createElement('div');
    row.classList.add('row');
    tiles[rowIdx] = [];


    Array.from({length: size}).forEach((_, colIdx) => {
        //Creates tile
        let tile = document.createElement('div');
        //Adds tile to row
        tile.classList.add('tile');
        row.appendChild(tile);

        //Assigns tile a row and col
        tile.setAttribute('data-row', rowIdx);
        tile.setAttribute('data-col', colIdx);

        //Allows tile to be typed in
        tile.setAttribute('contenteditable', 'true');

        //Assigns tile click to the onTileClick function
        tile.addEventListener("click", (event) => onTileClick(event, xyDict));

        //Assigns type input to the handleTextInput function
        tile.addEventListener("keydown", (event) => handleTextInput(event)); // Bind input event for text validation

         // Store the tile in the array
        tiles[rowIdx][colIdx] = tile;


    });
    //After inner for loop, add row to the grid
    tempGrid.appendChild(row);
});

//Moves current tile to top left current
currentTile = tiles[0][0]
grid.append(tempGrid)

/**
 * Credit: Oliver Strauss
 * Checks to see if (row, col) pair is not a black tile and in bounds
 *
 * @param row the row to check
 * @param col the column to check
 * @returns {boolean} true if the tile is valid, false otherwise
 */
function isValidTile(row, col){
    //console.log("before",row,col)
     if (inBounds(row, col)) {
         //console.log("after" , row,col)
        if (tiles[row][col].style.backgroundColor !== "black"){
            return true;
        }
    }
    return false;
}

/**
 * Credit: Oliver Strauss
 * Returns true if (row, col) is in bounds, and false otherwise
 *
 * @param row the row to check
 * @param col the column to check
 * @returns {boolean} true if (row, col) is in bounds, false otherwise
 */
function inBounds(row, col){
     return row >= 0 && row < size && col >= 0 && col < size;
}

/**
 * Credit: Oliver Strauss
 * Resets current tile color to default
 */
function clearCurrent() {
    currentTile.style.backgroundColor = '#e0e0e0';
}



/**
 * Credit: Oliver Strauss
 * Creates a dictionary that assigns each hint as a key to arr[row,col,word,direction]
 *
 * @param jsonData
 * @param hints
 * @returns {{}}
 */
function makeHintDict(jsonData, hints) {
    // The dictionary to store the hint and corresponding data
    const hintDict = {};

    //Ierates through hints and finds when hint and the jsonData hints are the same
    //and creates key
    for (let i = 0; i < hints.length; i++) {
        for (let j = 0; j < jsonData.length; j++) {
            if (hints[i] === jsonData[j].hint) {
                hintDict[hints[i]] = [jsonData[j].row, jsonData[j].column, jsonData[j].word, jsonData[j].direction]; // Associating hint with corresponding data

            }
        }
    }

    return hintDict
}
//Actually creates hintDict to use later
let hintDict = makeHintDict(data, hints)

/**
 * Credit: Oliver Strauss
 * Resets all tiles back to default color
 *
 * @param ignoreReds
 */
function clearHighlights(ignoreReds) {
    let color = '#e0e0e0'
    for (let hint in hintDict) {
        highlightTilesHint( hint, color,ignoreReds); // Reset color for each hint
    }
    highLightCurrent()
}

/**
 * Credit: Oliver Strauss
 * Highlights tiles to a corresponding hint
 * @param hint //Hint of a specific word to be highlighted
 * @param color //Color tiles are being highlighted
 * @param ignoreReds //Boolean to allow highlighting to ignore Red tile
 */
function highlightTilesHint(hint, color,ignoreReds) {
    //Pulls specific data assigned to one hint
    let hintList = hintDict[hint]

    // Destructure the hint data
    let [row, col, word, dir] = hintList;


    //Iterates through the word and highlights corresponding tiles
    for (let j = 0; j < word.length; j++) {
        if (dir) {
            if (tiles[row][col + j] !== currentTile) {
                if(ignoreReds || tiles[row][col+j].style.backgroundColor !== "red") {
                    tiles[row][col + j].style.backgroundColor = color;
                }
            }
        } else {
            if (tiles[row + j][col] !== currentTile) {
                 if(ignoreReds || tiles[row+j][col].style.backgroundColor !== "red" ) {
                     tiles[row + j][col].style.backgroundColor = color;
                 }
            }
        }
    }
}

/**
 * Credit: Oliver Strauss
 * Creates dictionary to assign "(x,y)" key to a word
 * @param jsonData
 * @returns {{}}
 */
function createRealWordDict(jsonData) {
    const wordDict = {}; // Initialize an empty dictionary

    jsonData.forEach(entry => {
        const { row, column, direction, word } = entry;

        for (let i = 0; i < word.length; i++) {
            const x = direction ? column + i : column; // Increment column if direction is true
            const y = direction ? row : row + i; // Increment row if direction is false
            wordDict[`${y},${x}`] = word[i]; // Use the (x, y) pair as the key and letter as value
        }
    });

    return wordDict; // Return the populated dictionary
}

/**
 * Credit: Oliver Strauss
 * Creates a dictionary that assigns "(x,y)" pairs to a list of hints
 * @param jsonData
 * @returns {{}}
 */
function makeRowColDict(jsonData) {
    const xyDict = {};

    // Helper function to process hints
    function processHints(isAcross) {
        for (let j = 0; j < jsonData.length; j++) {
            if (jsonData[j].direction === isAcross) { // Check direction
                for (let i = 0; i < jsonData[j].word.length; i++) {
                    const key = jsonData[j].direction
                        ? `${jsonData[j].row},${jsonData[j].column + i}` // ACROSS key
                        : `${jsonData[j].row + i},${jsonData[j].column}`; // DOWN key;

                    if (xyDict[key]) {
                        if (!Array.isArray(xyDict[key])) {
                            xyDict[key] = [xyDict[key]]; // Convert to array if needed
                        }
                        xyDict[key].push(jsonData[j].hint); // Append the hint
                    } else {
                        xyDict[key] = [jsonData[j].hint]; // Initialize with the hint
                    }
                }
            }
        }
    }

    // Process ACROSS hints first
    processHints(true);

    // Process DOWN hints next
    processHints(false);

    return xyDict;
}
//Initializes this dictionary to be used later
xyDict = makeRowColDict(data)

/**
 * Credit: Oliver Strauss
 * Handles all logic when a tile is clicked
 * @param event
 * @param xyDict
 */
function onTileClick(event, xyDict) {
    //Highlighted tiles color
    let color = "lightblue"

    //Gets row and col that user clickd on
    const row = event.target.getAttribute('data-row');
    const col = event.target.getAttribute('data-col');

    //Sets current tile to that row and col
    currentTile = tiles[row][col]

    //If user clicked on black tile, return
    if (currentTile.style.backgroundColor === "black"){
        return
    }
    //Changes the direction of user typing if necessary
    handleDirectionSwap(row,col)
    //Clears current highlighted tile
    clearCurrent()
    //Clears all current highlighted tiles
    clearHighlights()

    //List of hints on specific tile
    let hints = xyDict[`${row},${col}`]

    //If only one hint on tile highlight tiles and hint box
    if (hints.length === 1) {
        highlightTilesHint(hints[0], color)
        highlightHintBox(row,col)
    } else {
    //Else highlight both
        if (direction) {
            highlightTilesHint( hints[0], color)
            highlightHintBox(row,col)
        } else {
            highlightTilesHint( hints[1], color)
            highlightHintBox(row,col)
        }
    }
    //Highlight current tile
    highLightCurrent()
}






/**
 * Credit: Oliver Strauss
 * Sets color of current tile to yellow
 */
function highLightCurrent() {
     currentTile.style.backgroundColor = 'yellow';
}

/**
 * Credit: Oliver Strauss
 * Moves the current tile depending on input
 * @param row
 * @param col
 * @param prevOrNext //Boolean to move forward or back
 * @param jump //Num of tiles the current tile will mov
 */
function moveTile(row,col,prevOrNext,jump){
    clearCurrent()
    //Gets row and col
    row = parseInt(row);
    col = parseInt(col);

    // Sets current tile to move to previous or next tile
    let move
    if (prevOrNext){
        move = jump
    } else {
        move = (jump)*-1
    }

    // Sets current tile to next tile depending on direction
    if (direction) {

        if (isValidTile(row,col+move)) {
            currentTile = tiles[row][col + move];
        }
    } else {
        if (isValidTile(row+move,col) ) {
            currentTile = tiles[row + move][col];
        }
    }

    //Highlights new current tile
    highLightCurrent();
    //Sets all inputs to happen on current tile
    currentTile.focus();
}



/**
 * Credit: Oliver Strauss
 * Handles certain direction swap logic
 * @param row
 * @param col
 */
function handleDirectionSwap(row,col){
    //Gets row and col
    row = parseInt(row)
    col = parseInt(col)

    //If current tile has black tiles above and below sets direction across
    if( !isValidTile((row+1),col)  && !isValidTile((row-1),col)) {
        direction = true
    }
    //If current tile has black tiles to the sides of it sets direction dpwn
    if ((!isValidTile(row,col+1) ) && (!isValidTile(row,col-1) )){
        direction =  false
    }
}

/** Checks to see if user has won the game
 * Credit: Oliver Strauss
 */
function checkIfWon(){
    const letterDict = createRealWordDict(data)
    for (let i = 0; i < tiles.length; i++) { // Loop through rows
        for (let j = 0; j < tiles[i].length; j++) { // Loop through columns
            const key = `${i},${j}`; // Form the key for the current tile
            //If a tile has the wrong letter, return
            if(tiles[i][j].style.backgroundColor !=="black") {
                if (tiles[i][j].textContent !== letterDict[key]) {
                    return
                }
            }
        }
    }
    //If all tiles are correct, un-hide the wine menu
    // Show the win menu
    document.getElementById("endScreen").classList.remove("hidden");


}

/**
 * Credit: Oliver Strauss
 * Handles logic for when space bar is clicked
 *
 * @param event //Space bar clicked event
 * @param row
 * @param col
 * @param color //Color to be passed in and high
 */
function handleSpace(event,row,col,color){
    //Stops input
    event.preventDefault();

    //Swaps direction
    direction = !direction
    //Handles logic if direction is not allowed to swap
    handleDirectionSwap(row,col)

    //Gets hint depending on direction
    let hint;
    if (direction || xyDict[`${row},${col}`].length === 1) {
        hint = xyDict[`${row},${col}`][0]
    } else {
        hint = xyDict[`${row},${col}`][1]
    }
    //Clears previous highlighted tiles
    clearHighlights()
    //Highlights new tiles
    highlightTilesHint( hint, color)

    //Highlights appropriate hint box
    highlightHintBox(row,col)
}

/**
 * Credit: Oliver Strauss
 * Finds how many tiles currentTile needs to skip if they are black
 * @param userChar //Inputted character
 * @param row
 * @param col
 * @returns {(*|number)[]|number[]} // [Row,Col, num of tiles needed tp be jumped]
 */
function handleBlackTileJump(userChar, row, col) {
    let jumpIndx = 0;

    //Iterates until a non blaack tile is found
    while (true) {
         jumpIndx++;
        if (userChar === "ArrowRight") {
            col++;
        } else if (userChar === "ArrowLeft") {
            col--;
        } else if (userChar === "ArrowUp") {
            row--;
        } else if (userChar === "ArrowDown") {
            row++;
        }

        // Check bounds after each move
        if (!inBounds(row, col)) {
            return [-1,-1,-1];
        }
        if (isValidTile(row, col)) {
            break; // Exit the loop if a valid tile is found
        }
    }
    return [row, col, jumpIndx ];
}

/**
 * Credit: Oliver Strauss
 * Handles logic when user hits an arrow key
 * @param userChar //Character user inputted
 * @param row
 * @param col
 */
function handleArrowKey(userChar, row, col) {
    // Clear previous highlights
    clearHighlights();

    //Sets row and col to newRow and newCol
    let newRow = row;
    let newCol = col;

    // Adjust row/col based on arrow key
    if (userChar === "ArrowLeft") {
        direction = true;
        newCol = col - 1;

    } else if (userChar === "ArrowRight") {
        direction = true;
        newCol = col + 1;

    } else if (userChar === "ArrowUp") {
        direction = false;
        newRow = row - 1;
    } else if (userChar === "ArrowDown") {
        direction = false;
        newRow = row + 1;
    }
    //Checks if position is out of bounds
    if(!inBounds(newRow,newCol)){
        //Gets hint
        const hint = xyDict[`${row},${col}`];
        //Dummy value to save hint too
        let pluginHint
        //If multiple hints, choose one based on direction
        if(hint.length > 1){
            if(direction){
                pluginHint = hint[0]

            }
            else {
                pluginHint = hint[1]
            }
        }
        //Else choose the only one in the list
        else {
            pluginHint = hint[0]
        }
        //Highlight appropriate tiles
        highlightTilesHint(pluginHint,"lightblue",false)

        return;
    }

    //If moved position in bounds

    // Check if `xyDict` has a hint for the new position
    const newKey = `${newRow},${newCol}`;


    let keyList = xyDict[newKey]

    // Check if the new position is a black tile
    if (!isValidTile(newRow, newCol)) {
        //Chooses what hint to choose
        let hintIndex = direction ? 0 : 1;
        //Finds the new row, new col and amount of tiles currentTile needs to jump
        let  [updatedRow, updatedCol, jumpIndx] = handleBlackTileJump(userChar, newRow,newCol)
        //If out of bounds return
        if (updatedRow < 0){
            return;
        }
        //If only one hint available set hintIndex to find it
        if (xyDict[`${updatedRow},${updatedCol}`].length === 1){
            hintIndex = 0
        }

        //Moves tile sets previous or next depending on arrow direction
        moveTile(newRow,newCol,userChar === "ArrowRight" || userChar === "ArrowDown",jumpIndx)
        handleDirectionSwap(newRow,newCol)

        //Highlights new tiles
        highlightTilesHint(xyDict[`${updatedRow},${updatedCol}`][hintIndex],"lightblue")

        // Returns early to prevent errors
        return;
    }

    // Update the current tile if in bounds and a white tile
    moveTile(row, col, userChar === "ArrowRight" || userChar === "ArrowDown",1);

    //Highlights new tiles
    if (keyList.length === 1){
        highlightTilesHint(keyList[0], "lightblue");
    } else if (xyDict[newKey]) {
        const hintIndex = direction ? 0 : 1;
        highlightTilesHint(keyList[hintIndex], "lightblue");
    } else {
        //If no hints found throw a warning
        console.warn("No hint found for position:", newKey);
    }
    // Highlight the new current tile
    highLightCurrent();
}

/**
 * Credit: Oliver Strauss
 * Handles text input typed by user
 * @param event
 */
function handleTextInput(event) {

    let color = "lightblue"

    // Extract row index
    const row = parseInt(currentTile.getAttribute('data-row'));
    // Extract column index
    const col = parseInt(currentTile.getAttribute('data-col'));
    // Extracts inputed character
    let userChar = event.key

     let hint

    //Gets hint based on direction
    if (direction ||  xyDict[`${row},${col}`].length === 1) {
        hint = xyDict[`${row},${col}`][0]
    } else {
        hint = xyDict[`${row},${col}`][1]
    }

    //If user types a space handle it,
    if(userChar === " ") {
        handleSpace(event, row, col, color)
        return;
    //If user types a BackSpace, handle it
    } else if (userChar === "Backspace") {
        // Prevent default backspace behavior
        event.preventDefault();

        // Clear the current tile
        currentTile.textContent = "";
        // Moves Current Tile to previous tile
        moveTile(row, col, false,1);

        clearHighlights()
        //Highlights appropriate Tile
        highlightTilesHint( hint, color)
        return;
    //If user types an ArrowKey, handle it
    } else if ( /^Arrow(Up|Down|Left|Right)$/.test(userChar)){
        handleArrowKey(userChar,row,col)
        return;
    }

    // If user types exactly one alphanumeric character.
    if (/^[a-zA-Z0-9]$/.test(event.key)) {
        event.preventDefault();
        // Set tile content (convert to uppercase if needed)
        currentTile.textContent = event.key.toUpperCase();
    } else {
        // Block invalid inputs
        event.preventDefault();
        return;
    }
    //Sets current tile
    currentTile = tiles[row][col]

    //Clear current tiles
    clearHighlights(hintDict);

    /**
    if (currentTile.textContent.length === 1) {
        currentTile.textContent = userChar.toUpperCase();
       event.preventDefault();
    }

        **/


    //If user tries to types out of bounds set direction accordingly
    if(!inBounds(row,col+1) && direction){
        direction = false
    } else if ((!inBounds(row+1,col) && !direction )){
        direction = true
    }

    //Sets char to an arrowkey to handle movement
    if (direction ){
        userChar = "ArrowRight"
    } else {
        userChar = "ArrowDown"
    }

    //Handles if their are black tiles
    let newHint
    let [newRow, newCol, jumpIdx] = handleBlackTileJump(userChar,row,col)

    //Moves tile
    moveTile(row,col,true,jumpIdx)

    //Finds new hint depending on direction
    if (direction ||  xyDict[`${row},${col}`].length === 1) {
        newHint = xyDict[`${row},${col}`][0]
    } else {
        newHint = xyDict[`${row},${col}`][1]
    }
    //Highlights appropriate hint box
    highlightHintBox(newRow,newCol)

    //Highlights appropriate Tiles
    highlightTilesHint(newHint, color)

    //Checks if user has won
    checkIfWon()

    //Handles logic if autocheck is toggled on
    if(autocheck){
       runAutoCheck()
    }
}

/**
 * Credit: Oliver Strauss
 * Creates a 2-D list containing acrossHints and DownHints to be used to build the hint menu
 * @param data
 * @returns {*[][]}
 */
function generateHints(data) {
    //Initializes arrays
    const acrossHints = []
    const downHints = []

    for (let i = 0; i < data.length; i++) {
        const item = data[i];
        //Adds hint to appropriate list depending on direction
        if (item.direction === true) {
            acrossHints.push(item.hint)
        } else {
            downHints.push(item.hint)
        }
    }
    return [acrossHints, downHints]
}

/**
 * Credit: Oliver Strauss
 * Handles logic when user clicks on a tile
 * @param hintText
 */
function onHintClick(hintText) {
    let color = 'lightblue'
    //Clears all tiles
    clearHighlights()

    //Highlights appropriate tiles
    highlightTilesHint( hintText, color)
    //Highlights appropriate hint box
    highlightHintBox(hintDict[hintText][0],hintDict[hintText][1])
    //Clears highlight current tile
    clearCurrent()
    //Sets current tile to one user clicked on
    currentTile = tiles[hintDict[hintText][0]][hintDict[hintText][1]]
    //Sets direction
    direction = hintDict[hintText][3]
    //Highlights new CurrentTile
    highLightCurrent()
    currentTile.focus();
}

/**
 * Credit: Oliver Strauss
 * Highlights hint box in the hint menu
 * @param hintText
 */
function highlightHintBox(row,col) {
    //Removes highlighted borders from all hint boxes
    clearClueBorders()
    // Remove 'highlighted' class from all list items
    const allHintItems = document.querySelectorAll('#acrossHints li, #downHints li');
    allHintItems.forEach(item => {
        item.classList.remove('highlighted');
    });

    //Finds word associated to specific row and col
    const key = `${row},${col}`;
    let words= xyDict[key]

    let hintText
    //If multiple words lie on one tile
    if(words.length > 1 ){
        //if word is across
        if(direction){
            //Adds border highlights to perpendicular hint box
            const hintItem = Array.from(allHintItems).find(item => item.textContent === words[1]);
            // Apply dynamic highlight
            hintItem.style.boxShadow = '0 0 0 4px lightblue';
            //Saves other hint to be fully highlighted
            hintText = words[0]

        }
        else{
            //Adds border highlights to perpendicular hint box
            const hintItem = Array.from(allHintItems).find(item => item.textContent === words[0]);
            //Apply dynamic highlight
            hintItem.style.boxShadow = '0 0 0 4px lightblue';
            //Saves other hint to be fully highlighted
            hintText = words[1]
        }
    }
    //Else the tile only has one word
    else{
        //Saves hint to be fully highlighted
        hintText = words[0]
    }


    // Find the clicked hint and add 'highlighted' class to it
    const hintItem = Array.from(allHintItems).find(item => item.textContent === hintText);
    if (hintItem) {
        // Fully Highlights hint box
        hintItem.classList.add('highlighted');
    }
}

/**
 * Credit: Oliver Strauss
 * Clears all highlighted hint box borders
 */
function clearClueBorders() {
    // Select all hint items in both hint banks
    const allHintItems = document.querySelectorAll('#acrossHints li, #downHints li');

    // Loop through each item and remove the box-shadow
    allHintItems.forEach(item => {
        item.style.boxShadow = ''; // Clear any existing box-shadow
    });
}

//2-D array of across and down hints
let listOfHints = generateHints(data)
//Unpacks array into 2 separate ones
let [acrossHints, downHints] = listOfHints;

/**
 * Credit: Oliver Strauss
 * Sets all tiles that do not accept text to black and untypeable
 */
function createBlockTiles() {
    //Iterates through blocked tiles 2-D array and sets them accordingly
    for (let i = 0; i < blockedTiles.length; i++) {
        const [row, col] = blockedTiles[i];
        tiles[row][col].style.backgroundColor = "black";
        tiles[row][col].setAttribute('contenteditable', 'false'); // Disable editing

    }
}

// Builds "Hint Menu" by taking in across hints
let acrossHintsList = document.querySelector('#acrossHints');
acrossHints.forEach(hint => {
    let listItem = document.createElement('li');
    listItem.addEventListener("click", () => onHintClick(hint));
    listItem.textContent = hint;

    acrossHintsList.appendChild(listItem);
});

// Builds "Hint Menu" by taking in down hints
let downHintsList = document.querySelector("#downHints");
downHints.forEach((hint) => {
    let listItem = document.createElement("li");
    listItem.addEventListener("click", () => onHintClick(hint));

    listItem.textContent = hint;
    downHintsList.appendChild(listItem);
});

/**
 * Restarts the page
 * Credit: Oliver Strauss
 */
function restartPage(){
     location.reload();
}

//Calls the method to add the block tiles to the grid
createBlockTiles()
//All the event listener handling for buttons
document.getElementById('autocheckButton').addEventListener('click', onAutoCheckClick);//AutoCheck Button
document.getElementById('revealButton').addEventListener('click', onRevealClick);//Reveal grid button
document.getElementById('revealTileButton').addEventListener('click', onTileCheckClick)//Reveal tile button
document.getElementById('restartButton').addEventListener('click', restartPage)//Restart page button

//Creates start screen
document.getElementById("startGameButton").addEventListener("click", () => {
    document.getElementById("startScreen").classList.add("hidden");
});

//Creates letterDict
const letterDict = createRealWordDict(data)

/**
 * Credit: Oliver Strauss
 * Handles when user hits reveal grid button
 */
function onRevealClick() {
    for (let i = 0; i < tiles.length; i++) { // Loop through rows
        for (let j = 0; j < tiles[i].length; j++) { // Loop through columns
            if(tiles[i][j].style.backgroundColor !== "black") {
                const key = `${i},${j}`; // Form the key for the current tile
                tiles[i][j].textContent = letterDict[key]; // Set the letter if it exists in the dictionary
                tiles[i][j].setAttribute('contenteditable', false)
                tiles[i][j].style.color = "blue"
            }


        }
    }
}

/**
 * Credit: Oliver Strauss
 * Handles when user clicks the autocheck toggle
 */
function onAutoCheckClick() {
    //Toggles autocheck on or off
    autocheck = !autocheck
    //If button is already toggled turn it back to og color
    if (document.getElementById('autocheckButton').style.backgroundColor === "lightblue") {
        document.getElementById('autocheckButton').style.backgroundColor = '#007BFF'
        //Clear all highlights except red tiles
        clearHighlights(true)

    }
    else{
        //If autocheck was just turned on run autoCheck
        document.getElementById('autocheckButton').style.backgroundColor = "lightblue"
        runAutoCheck()
    }

}


/**
 * Credit: Oliver Strauss
 * Handles highlighting any incorrect tiles on the grid when autocheck is toggled on
 */
function runAutoCheck(){
        const letterDict = createRealWordDict(data)

        for (let i = 0; i < tiles.length; i++) { // Loop through rows
            for (let j = 0; j < tiles[i].length; j++) { // Loop through columns
                const key = `${i},${j}`; // Form the key for the current tile
                if (tiles[i][j].textContent !== letterDict[key] && tiles[i][j].textContent !== "" && tiles[i][j].style.backgroundColor !== "black") {
                    tiles[i][j].style.backgroundColor = "red" // Set the letter if it exists in the dictionary
                }
                else if(tiles[i][j].textContent === letterDict[key]){
                    //Sets correct tile color as blue
                    tiles[i][j].style.color = "Blue"

                }
            }
        }
}

/**
 * Credit: Oliver Strauss
 * Handles when Tile check button is clicked
 */
function onTileCheckClick(){
    const row = parseInt(currentTile.getAttribute('data-row')); // Extract row index
    const col = parseInt(currentTile.getAttribute('data-col')); // Extract column index
    const key = `${row},${col}`;

    //Reveals current tile letter and sets text color to blue
    tiles[row][col].textContent = letterDict[key]
    tiles[row][col].style.color = "Blue"


}