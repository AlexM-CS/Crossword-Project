let grid = document.querySelector('#game')

let fragment = document.createDocumentFragment();
let tiles = [];
let direction = true
let currentTile;
let winCon

document.getElementById("endScreen").classList.add("hidden");

/**Checks to see if row,col pair is in the grid or not
 *
 * @param row
 * @param col
 * @returns {boolean}
 */
function isValidTile(row,col){

     if (row >= 0 && row < tiles.length && col >= 0 && col < tiles[row].length ) {
        if(tiles[row][col].style.backgroundColor !== "black"){
            return true;
        }
    }
    return false;
}

function inBounds(row,col){
     return row >= 0 && row < tiles.length && col >= 0 && col < tiles[row].length;

}

/**
 * Resets current tile color to default
 */
function clearCurrent() {
    currentTile.style.backgroundColor = '#e0e0e0';
}

function makeHintDict(jsonData, hints) {
    const hintDict = {}; // The dictionary to store the hint and corresponding data

    for (let i = 0; i < hints.length; i++) {
        for (let j = 0; j < jsonData.length; j++) {
            if (hints[i] === jsonData[j].hint) {
                hintDict[hints[i]] = [jsonData[j].row, jsonData[j].column, jsonData[j].word, jsonData[j].direction]; // Associating hint with corresponding data

            }
        }
    }
    return hintDict
}
let hintDict = makeHintDict(data, hints)


/** Resets all tiles back to default color
 *
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


function highlightTilesHint(hint, color,ignoreReds) {

    let hintList = hintDict[hint]
    //console.log(hintDict)
    //console.log(hint)
   //console.log(hintList)

    let [row, col, word, dir] = hintList; // Destructure the hint data


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


function onTileClick(event, xyDict) {


    let color = "lightblue"
    const row = event.target.getAttribute('data-row');
    const col = event.target.getAttribute('data-col');
    currentTile = tiles[row][col]
    if(currentTile.style.backgroundColor === "black"){
        return
    }
    clearCurrent()
    clearHighlights()


    let hints = xyDict[`${row},${col}`]


    if (hints.length === 1) {
        highlightTilesHint(hints[0], color)
        highlightHintBox(hints[0])

    } else {
        if (direction) {
            highlightTilesHint( hints[0], color)
            highlightHintBox(hints[0])

        } else {
            highlightTilesHint( hints[1], color)
            highlightHintBox(hints[1])

        }
    }


    highLightCurrent()
    // console.log(xyDict)
   // console.log(hintDict)


}


xyDict = makeRowColDict(data)
//Dict { hint -> [row,col,word,direction]



Array.from({length: size}).forEach((_, rowIdx) => {
    let row = document.createElement('div');
    row.classList.add('row');
    tiles[rowIdx] = [];

    Array.from({length: size}).forEach((_, colIdx) => {
        let tile = document.createElement('div');
        tile.classList.add('tile');

        row.appendChild(tile);
        tile.setAttribute('data-row', rowIdx);
        tile.setAttribute('data-col', colIdx);
        tile.setAttribute('contenteditable', 'true');
        tile.addEventListener("click", (event) => onTileClick(event, xyDict));
        tile.addEventListener("keydown", (event) => handleTextInput(event)); // Bind input event for text validation

        tiles[rowIdx][colIdx] = tile; // Store the tile in the array
        row.appendChild(tile);
    });
    fragment.appendChild(row);

});

currentTile = tiles[0][0]
grid.append(fragment)



function highLightCurrent() {

    if (currentTile && currentTile.style.backgroundColor !== 'black' && currentTile.getAttribute('contenteditable') !== 'false') {

        currentTile.style.backgroundColor = 'yellow';

    } else {

        console.error('currentTile is blocked or undefined.');


    }
}
function moveTile(row,col,prevOrNext,jump){
    clearCurrent()

    row = parseInt(row);
    col = parseInt(col);
    //Sets current tile to move to previous or next tile
    let move
    if(prevOrNext){
        move = jump
    }else{
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

    highLightCurrent();
    currentTile.focus();
}



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


function handleDirectionSwap(row,col){
    if(direction){
        if((!isValidTile(row+1,col) || tiles[row+1][col].style.backgroundColor === "black") && (!isValidTile(row-1,col) || tiles[row-1][col].style.backgroundColor === "black" )){
            console.log("invaalid place to swap across dir")
            return true;
        }
        else {
            direction = !direction
            return false;
        }
    }
    else{
         if(( !isValidTile(row,col+1)  || tiles[row][col+1].style.backgroundColor === "black")  && (!isValidTile(row,col-1) || tiles[row][col-1].style.backgroundColor === "black" )){
            console.log("invaalid place to swap down dir")
             return true ;
        }
        else {
            direction = !direction
            return false ;
        }
    }
}
function checkIfWon(){
    const letterDict = createRealWordDict(data)
    for (let i = 0; i < tiles.length; i++) { // Loop through rows
        for (let j = 0; j < tiles[i].length; j++) { // Loop through columns
            const key = `${i},${j}`; // Form the key for the current tile
            if(tiles[i][j].style.backgroundColor !=="black") {
                if (tiles[i][j].textContent !== letterDict[key]) {
                    console.log("lost")
                    return
                }
            }
        }
    }
    document.getElementById("endScreen").classList.remove("hidden");
 // Show the win menu
    console.log("won")

}

function handleSpace(event,row,col,color){
    event.preventDefault();
    handleDirectionSwap(row,col)
    let hint;
    if (direction || xyDict[`${row},${col}`].length === 1) {
        hint = xyDict[`${row},${col}`][0]
    } else {
        hint = xyDict[`${row},${col}`][1]
    }
    clearHighlights()
    highlightTilesHint( hint, color)
    highlightHintBox(hint)
}


function handleBlackTileJump(userChar, row, col) {
    let jumpIndx = 0;
    console.log(userChar)
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

function handleArrowKey(userChar, row, col) {
    console.log(direction)
    console.log(xyDict)
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
        console.log("gothca bitch")
            return;
    }
    console.log(newRow , newCol)
    console.log(xyDict)
     // Check if `xyDict` has a hint for the new position
    const newKey = `${newRow},${newCol}`;
    console.log(newKey)
    let keyList = xyDict[newKey]

    // Check if the new position is within bounds
    if (!isValidTile(newRow, newCol)) {

        let hintIndex = direction ? 0 : 1;
        let  [updatedRow, updatedCol, jumpIndx] = handleBlackTileJump(userChar, newRow,newCol)
        if(updatedRow < 0){
            return;
        }
        if(xyDict[`${updatedRow},${updatedCol}`].length === 1){
            hintIndex = 0
        }

            moveTile(row,col,userChar === "ArrowRight" || userChar === "ArrowDown",jumpIndx)
            handleDirectionSwap(newRow,newCol)
            console.log(xyDict[`${updatedRow},${updatedCol}`][hintIndex])
            highlightTilesHint(xyDict[`${updatedRow},${updatedCol}`][hintIndex],"lightblue")
            //if(areAllAdjacentTilesInvalid(new))
            highLightCurrent();

        //}

        console.log(hintIndex)
        console.log(xyDict[`${updatedRow},${updatedCol}`])

        return; // Exit early to prevent errors
    }

    // Update the current tile
    moveTile(row, col, userChar === "ArrowRight" || userChar === "ArrowDown",1);



    if(keyList.length === 1){
        highlightTilesHint(keyList[0], "lightblue");

    }
    else if (xyDict[newKey]) {
        const hintIndex = direction ? 0 : 1;

        highlightTilesHint(keyList[hintIndex], "lightblue");
    } else {
        console.warn("No hint found for position:", newKey);
    }

    // Highlight the new current tile
    highLightCurrent();

}


function handleTextInput(event) {
    const row = parseInt(currentTile.getAttribute('data-row')); // Extract row index
    const col = parseInt(currentTile.getAttribute('data-col')); // Extract column index
    let color = 'lightblue'
    let hint
    let userChar = event.key

    if (direction ||  xyDict[`${row},${col}`].length === 1) {
        hint = xyDict[`${row},${col}`][0]
    } else {
        hint = xyDict[`${row},${col}`][1]
    }

    if(userChar === " ") {

        handleSpace(event, row, col, color)
        return;
    }
    else if(userChar === "Backspace") {
        event.preventDefault(); // Prevent default backspace behavior
        currentTile.textContent = ""; // Clear the current tile
        moveTile(row, col, false,1); // Moves Current Tile to previous tile
        clearHighlights()
        highlightTilesHint( hint, color) //Highlights appropriate Tile
        return;
    }
    else if( /^Arrow(Up|Down|Left|Right)$/.test(userChar)){
        handleArrowKey(userChar,row,col)
        return;
    }




    //Ensures that the input consists of exactly one alphanumeric character.
     if (/^[a-zA-Z0-9]$/.test(event.key)) {
        event.preventDefault();
        currentTile.textContent = event.key.toUpperCase(); // Set tile content (convert to uppercase if needed)
    } else {
        event.preventDefault(); // Block invalid inputs
        return;
    }




    currentTile = tiles[row][col]

    clearHighlights(hintDict);


    if (currentTile.textContent.length === 1) {
        currentTile.textContent = userChar.toUpperCase();
       event.preventDefault();
    }

    if(!inBounds(row,col+1) && direction  ){
        direction = false
    }
    else if((!inBounds(row+1,col) &&  !direction ) ){
        direction = true

    }

    if(direction ){
        userChar = "ArrowRight"
    }
    else {
        userChar = "ArrowDown"
    }

    let [newRow, newCol, jumpIdx] = handleBlackTileJump(userChar,row,col)

    moveTile(row,col,true,jumpIdx)




    highlightHintBox(hint)

    highlightTilesHint(hint, color)

    checkIfWon()


}


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


function onHintClick(hintText) {
    let color = 'lightblue'
    clearHighlights()
    highlightTilesHint( hintText, color)
    highlightHintBox(hintText)

    clearCurrent()
    currentTile = tiles[hintDict[hintText][0]][hintDict[hintText][1]]
    direction = hintDict[hintText][3]
    highLightCurrent()
    currentTile.focus();



}

function highlightHintBox(hintText) {
    // Remove 'highlighted' class from all list items
    const allHintItems = document.querySelectorAll('#acrossHints li, #downHints li');
    allHintItems.forEach(item => {
        item.classList.remove('highlighted');
    });

    // Find the clicked hint and add 'highlighted' class to it
    const hintItem = Array.from(allHintItems).find(item => item.textContent === hintText);
    if (hintItem) {
        hintItem.classList.add('highlighted');
    }
}


let listOfHints = generateHints(data)
let [acrossHints, downHints] = listOfHints;

/** Sets all tiles that do not accept text to black
 *
 */
function createBlockTiles() {

    for (let i = 0; i < blockedTiles.length; i++) {
        const [row, col] = blockedTiles[i];

        tiles[row][col].style.backgroundColor = "black";
        tiles[row][col].setAttribute('contenteditable', 'false'); // Disable editing

    }
}


//Builds "Hint Menu" by taking in across and down hints separately
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

function restartPage(){
     location.reload();
}


//createIndexCellNumbers(data)
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
function onRevealClick() {


    for (let i = 0; i < tiles.length; i++) { // Loop through rows
        for (let j = 0; j < tiles[i].length; j++) { // Loop through columns
            const key = `${i},${j}`; // Form the key for the current tile
            tiles[i][j].textContent = letterDict[key]; // Set the letter if it exists in the dictionary

        }
    }
}
function onAutoCheckClick() {
    if (document.getElementById('autocheckButton').style.backgroundColor === "lightblue") {
        document.getElementById('autocheckButton').style.backgroundColor = '#007BFF'
        clearHighlights(true)
    } else {
        document.getElementById('autocheckButton').style.backgroundColor = "lightblue"
        const letterDict = createRealWordDict(data)

        for (let i = 0; i < tiles.length; i++) { // Loop through rows
            for (let j = 0; j < tiles[i].length; j++) { // Loop through columns
                const key = `${i},${j}`; // Form the key for the current tile
                if (tiles[i][j].textContent !== letterDict[key] && tiles[i][j].textContent !== "" && tiles[i][j].style.backgroundColor !== "black") {
                    tiles[i][j].style.backgroundColor = "red" // Set the letter if it exists in the dictionary
                }
                else{
                    tiles[i][j].style.color = "Blue"
                }
            }
        }
    }
}

    function onTileCheckClick(){
        const row = parseInt(currentTile.getAttribute('data-row')); // Extract row index
        const col = parseInt(currentTile.getAttribute('data-col')); // Extract column index
        const key = `${row},${col}`;
        console.log(letterDict[key])
        tiles[row][col].textContent = letterDict[key]
        tiles[row][col].style.color = "Blue"

    }