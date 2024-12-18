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

    let hints = xyDict[`${row},${col}`]

    if (hints.length === 1) {
        highlightTilesHint(hints[0], color)
        highlightHintBox(row,col)
    } else {
        if (direction) {
            highlightTilesHint( hints[0], color)
            highlightHintBox(row,col)
        } else {
            highlightTilesHint( hints[1], color)
            highlightHintBox(row,col)
        }
    }
    highLightCurrent()
}

xyDict = makeRowColDict(data)




/**
 * Credit: Oliver Strauss
 */
function highLightCurrent() {

   // if (currentTile && currentTile.style.backgroundColor !== 'black' && currentTile.getAttribute('contenteditable') !== 'false') {
        currentTile.style.backgroundColor = 'yellow';

   // } else {
     //   console.error('currentTile is blocked or undefined.');
    //}
}

/**
 * Credit: Oliver Strauss
 *
 * @param row
 * @param col
 * @param prevOrNext
 * @param jump
 */
function moveTile(row,col,prevOrNext,jump){
    clearCurrent()

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
           // console.log("yo righ there")
           // console.log(row, col+move)
        }

    } else {
        if (isValidTile(row+move,col) ) {
            currentTile = tiles[row + move][col];
        }
    }
   // console.log("yo righ there")
   // console.log(row+move, col)
   //  console.log(row, col+move)
    highLightCurrent();
    currentTile.focus();
}

/**
 * Credit: Oliver Strauss
 *
 * @param row
 * @param col
 * @returns {boolean}
 */
function areAllAdjacentTilesInvalid(row, col) {
    const directions = [
        [-1, 0], // Up
        [1, 0],  // Down
        [0, -1], // Left
        [0, 1],  // Right
    ];

    for (let [rowOffset, colOffset] of directions) {
        const newRow = row + rowOffset;
        const newCol = col + colOffset;

        if (inBounds(newRow, newCol) && tiles[newRow][newCol].style.backgroundColor !== "black") {
            return false; // Found a valid adjacent tile
        }
    }
    return true; // All adjacent tiles are invalid
}

/**
 * Credit: Oliver Strauss
 *
 * @param row
 * @param col
 * @returns {boolean}
 */
function handleDirectionSwap(row,col){
     row = parseInt(row)
     col = parseInt(col)
   // if(direction){
        if( !isValidTile((row+1),col)  && !isValidTile((row-1),col)) {

           direction = true
        }

  //  } else {
         if ((!isValidTile(row,col+1) ) && (!isValidTile(row,col-1) )){
             //console.log("invaalid place to swap down dir")
             direction =  false
        } //else {
            //direction = !direction
           // return false;
       // }
   // }
}

/**
 * Credit: Oliver Strauss
 */
function checkIfWon(){
    const letterDict = createRealWordDict(data)
    for (let i = 0; i < tiles.length; i++) { // Loop through rows
        for (let j = 0; j < tiles[i].length; j++) { // Loop through columns
            const key = `${i},${j}`; // Form the key for the current tile
            if(tiles[i][j].style.backgroundColor !=="black") {
                if (tiles[i][j].textContent !== letterDict[key]) {
                    return
                }
            }
        }
    }
    // Show the win menu
    document.getElementById("endScreen").classList.remove("hidden");


}

/**
 * Credit: Oliver Strauss
 *
 * @param event
 * @param row
 * @param col
 * @param color
 */
function handleSpace(event,row,col,color){
    event.preventDefault();
    direction = !direction
    handleDirectionSwap(row,col)
    let hint;
    if (direction || xyDict[`${row},${col}`].length === 1) {
        hint = xyDict[`${row},${col}`][0]
    } else {
        hint = xyDict[`${row},${col}`][1]
    }
    clearHighlights()
    highlightTilesHint( hint, color)
    highlightHintBox(row,col)
}

/**
 * Credit: Oliver Strauss
 *
 * @param userChar
 * @param row
 * @param col
 * @returns {(*|number)[]|number[]}
 */
function handleBlackTileJump(userChar, row, col) {
    let jumpIndx = 0;
    //console.log(userChar)
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
 *
 * @param userChar
 * @param row
 * @param col
 */
function handleArrowKey(userChar, row, col) {
   // console.log(direction)
    //console.log(xyDict)
    clearHighlights(); // Clear previous highlights

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
    if(!inBounds(newRow,newCol)){
       // console.log(row,col)
        const hint = xyDict[`${row},${col}`];
        let pluginHint
        if(hint.length > 1){
            if(direction){
                pluginHint = hint[0]

            }
            else {
                pluginHint = hint[1]
            }
        }
        else {
            pluginHint = hint[0]
        }

        highlightTilesHint(pluginHint,"lightblue",false)

        return;
    }

     // Check if `xyDict` has a hint for the new position
    const newKey = `${newRow},${newCol}`;

    let keyList = xyDict[newKey]

    // Check if the new position is within bounds
    if (!isValidTile(newRow, newCol)) {
        let hintIndex = direction ? 0 : 1;
        let  [updatedRow, updatedCol, jumpIndx] = handleBlackTileJump(userChar, newRow,newCol)
        if (updatedRow < 0){
            return;
        }
        if (xyDict[`${updatedRow},${updatedCol}`].length === 1){
            hintIndex = 0
        }
            moveTile(newRow,newCol,userChar === "ArrowRight" || userChar === "ArrowDown",jumpIndx)
            handleDirectionSwap(newRow,newCol)

            highlightTilesHint(xyDict[`${updatedRow},${updatedCol}`][hintIndex],"lightblue")
           // highLightCurrent();

        //console.log(hintIndex)
        //console.log(xyDict[`${updatedRow},${updatedCol}`])

        return; // Exit early to prevent errors
    }

    // Update the current tile
    moveTile(row, col, userChar === "ArrowRight" || userChar === "ArrowDown",1);

    if (keyList.length === 1){
        highlightTilesHint(keyList[0], "lightblue");
    } else if (xyDict[newKey]) {
        const hintIndex = direction ? 0 : 1;
        highlightTilesHint(keyList[hintIndex], "lightblue");
    } else {
        console.warn("No hint found for position:", newKey);
    }
    // Highlight the new current tile
    highLightCurrent();
}

/**
 * Credit: Oliver Strauss
 *
 * @param event
 */
function handleTextInput(event) {
    const row = parseInt(currentTile.getAttribute('data-row')); // Extract row index
    const col = parseInt(currentTile.getAttribute('data-col')); // Extract column index
    let color = 'lightblue'
    let hint
    let userChar = event.key

    const key = `${row},${col}`



    console.log(autocheck)




    if (direction ||  xyDict[`${row},${col}`].length === 1) {
        hint = xyDict[`${row},${col}`][0]
    } else {
        hint = xyDict[`${row},${col}`][1]
    }
    //console.log(hint)
    //console.log(hintDict)

    if(userChar === " ") {
        handleSpace(event, row, col, color)
        return;
    } else if (userChar === "Backspace") {
        event.preventDefault(); // Prevent default backspace behavior
        currentTile.textContent = ""; // Clear the current tile
        moveTile(row, col, false,1); // Moves Current Tile to previous tile
        clearHighlights()
        highlightTilesHint( hint, color) // Highlights appropriate Tile
        return;
    } else if ( /^Arrow(Up|Down|Left|Right)$/.test(userChar)){
        handleArrowKey(userChar,row,col)
        return;
    }

    // Ensures that the input consists of exactly one alphanumeric character.
    if (/^[a-zA-Z0-9]$/.test(event.key)) {

        event.preventDefault();
        currentTile.textContent = event.key.toUpperCase(); // Set tile content (convert to uppercase if needed)
    } else {
        event.preventDefault(); // Block invalid inputs
        return;
    }

    currentTile = tiles[row][col]

   ; // Form the key for the current tile


    clearHighlights(hintDict);

    if (currentTile.textContent.length === 1) {
        currentTile.textContent = userChar.toUpperCase();
       event.preventDefault();
    }



    if(!inBounds(row,col+1) && direction){
        direction = false
    } else if ((!inBounds(row+1,col) && !direction )){
        direction = true
    }

    if (direction ){
        userChar = "ArrowRight"
    } else {
        userChar = "ArrowDown"
    }
    let newHint
    let [newRow, newCol, jumpIdx] = handleBlackTileJump(userChar,row,col)
    moveTile(row,col,true,jumpIdx)
    if (direction ||  xyDict[`${row},${col}`].length === 1) {
        newHint = xyDict[`${row},${col}`][0]
    } else {
        newHint = xyDict[`${row},${col}`][1]
    }
    highlightHintBox(newRow,newCol)
    highlightTilesHint(newHint, color)
    checkIfWon()
    if(autocheck){
       runAutoCheck()
    }
}

/**
 * Credit: Oliver Strauss
 *
 * @param data
 * @returns {*[][]}
 */
function generateHints(data) {
    const acrossHints = []
    const downHints = []
    for (let i = 0; i < data.length; i++) {
        const item = data[i];
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
 *
 * @param hintText
 */
function onHintClick(hintText) {
    let color = 'lightblue'
    clearHighlights()
    highlightTilesHint( hintText, color)
    highlightHintBox(hintDict[hintText][0],hintDict[hintText][1])

    clearCurrent()
    currentTile = tiles[hintDict[hintText][0]][hintDict[hintText][1]]
    direction = hintDict[hintText][3]
    highLightCurrent()
    currentTile.focus();
}

/**
 * Credit: Oliver Strauss
 *
 * @param hintText
 */
function highlightHintBox(row,col) {
    clearClueBorders()
    // Remove 'highlighted' class from all list items
    const allHintItems = document.querySelectorAll('#acrossHints li, #downHints li');
    allHintItems.forEach(item => {
        item.classList.remove('highlighted');
    });
     const key = `${row},${col}`;
     let words= xyDict[key]
    let hintText
    if(words.length > 1 ){
        if(direction){
            const hintItem = Array.from(allHintItems).find(item => item.textContent === words[1]);
            hintItem.style.boxShadow = '0 0 0 4px lightblue'; // Apply dynamic highlight
            hintText = words[0]

        }
        else{
            const hintItem = Array.from(allHintItems).find(item => item.textContent === words[0]);
            hintItem.style.boxShadow = '0 0 0 4px lightblue'; // Apply dynamic highlight
            hintText = words[1]
        }
    }
    else{
        hintText = words[0]
    }


    // Find the clicked hint and add 'highlighted' class to it
    const hintItem = Array.from(allHintItems).find(item => item.textContent === hintText);
    if (hintItem) {
        hintItem.classList.add('highlighted');
    }
}

function clearClueBorders() {
    // Select all hint items in both hint banks
    const allHintItems = document.querySelectorAll('#acrossHints li, #downHints li');

    // Loop through each item and remove the box-shadow
    allHintItems.forEach(item => {
        item.style.boxShadow = ''; // Clear any existing box-shadow
    });
}

let listOfHints = generateHints(data)
let [acrossHints, downHints] = listOfHints;

/**
 * Credit: Oliver Strauss
 * Sets all tiles that do not accept text to black
 */
function createBlockTiles() {

    for (let i = 0; i < blockedTiles.length; i++) {
        const [row, col] = blockedTiles[i];

        tiles[row][col].style.backgroundColor = "black";
        tiles[row][col].setAttribute('contenteditable', 'false'); // Disable editing

    }
}

// Builds "Hint Menu" by taking in across and down hints separately
let acrossHintsList = document.querySelector('#acrossHints');
acrossHints.forEach(hint => {
    let listItem = document.createElement('li');
    listItem.addEventListener("click", () => onHintClick(hint));
    listItem.textContent = hint;

    acrossHintsList.appendChild(listItem);
});

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


// createIndexCellNumbers(data)
createBlockTiles()

document.getElementById('autocheckButton').addEventListener('click', onAutoCheckClick);
document.getElementById('revealButton').addEventListener('click', onRevealClick);
document.getElementById('restartButton').addEventListener('click', restartPage)
document.getElementById('revealTileButton').addEventListener('click', onTileCheckClick)

document.getElementById("startGameButton").addEventListener("click", () => {
    document.getElementById("startScreen").classList.add("hidden");
});
// Reload the page
const letterDict = createRealWordDict(data)

/**
 * Credit: Oliver Strauss
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
 */
function onAutoCheckClick() {
    autocheck = !autocheck
    if (document.getElementById('autocheckButton').style.backgroundColor === "lightblue") {
        document.getElementById('autocheckButton').style.backgroundColor = '#007BFF'
        clearHighlights(true)

    }
    else{
        document.getElementById('autocheckButton').style.backgroundColor = "lightblue"
        runAutoCheck()
    }

}

function runAutoCheck(){
        const letterDict = createRealWordDict(data)

        for (let i = 0; i < tiles.length; i++) { // Loop through rows
            for (let j = 0; j < tiles[i].length; j++) { // Loop through columns
                const key = `${i},${j}`; // Form the key for the current tile
                if (tiles[i][j].textContent !== letterDict[key] && tiles[i][j].textContent !== "" && tiles[i][j].style.backgroundColor !== "black") {
                    tiles[i][j].style.backgroundColor = "red" // Set the letter if it exists in the dictionary
                }
                else if(tiles[i][j].textContent === letterDict[key]){
                    tiles[i][j].style.color = "Blue"
                    // Disable editing for corecct tiles
                    //tiles[i][j].setAttribute('contenteditable', 'false');
                }
            }
        }
}

/**
 * Credit: Oliver Strauss
 */
function onTileCheckClick(){
    const row = parseInt(currentTile.getAttribute('data-row')); // Extract row index
    const col = parseInt(currentTile.getAttribute('data-col')); // Extract column index
    const key = `${row},${col}`;
    //console.log(letterDict[key])

    tiles[row][col].textContent = letterDict[key]
    tiles[row][col].style.color = "Blue"
    tiles[row][col].setAttribute('contenteditable',false)


}