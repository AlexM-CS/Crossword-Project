let grid = document.querySelector('#game')

let fragment = document.createDocumentFragment();
let tiles = [];
let direction = true
let currentTile;
let winCon


function checkBounds(row,col){
    if (row >= 0 && row < tiles.length && col >= 0 && col < tiles[row].length) {
        return true;
    }
    return false;
}
function clearHighlights(hintDict) {
    let color = '#e0e0e0'
    for (let hint in hintDict) {
        highlightTilesHint(hintDict, hint, color); // Reset color for each hint
    }
}

function highlightTilesHint(hintDict, hint, color) {

    let hintList = hintDict[hint]

    let [row, col, word, direction] = hintList; // Destructure the hint data


    for (let j = 0; j < word.length; j++) {
        if (direction) {
            if (tiles[row][col + j] !== currentTile) {

                tiles[row][col + j].style.backgroundColor = color;


            }

        } else {
            if (tiles[row + j][col] !== currentTile) {

                tiles[row + j][col].style.backgroundColor = color;
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


function onTileClick(event, xyDict, hintDict) {


    let color = "lightblue"
    const row = event.target.getAttribute('data-row');
    const col = event.target.getAttribute('data-col');
    currentTile = tiles[row][col]
    if(currentTile.style.backgroundColor === "black"){
        return
    }
    clearCurrent()
    clearHighlights(hintDict)


    let hints = xyDict[`${row},${col}`]


    if (hints.length === 1) {
        highlightTilesHint(hintDict, hints[0], color)
        highlightHintBox(hints[0])

    } else {
        if (direction) {
            highlightTilesHint(hintDict, hints[0], color)
            highlightHintBox(hints[0])

        } else {
            highlightTilesHint(hintDict, hints[1], color)
            highlightHintBox(hints[1])

        }
    }


    highLightCurrent()


}


xyDict = makeRowColDict(data)
//Dict { hint -> [row,col,word,direction]
hintDict = makeHintDict(data, hints)


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
        tile.addEventListener("click", (event) => onTileClick(event, xyDict, hintDict));
        tile.addEventListener("keydown", (event) => handleTextInput(event)); // Bind input event for text validation

        tiles[rowIdx][colIdx] = tile; // Store the tile in the array
        row.appendChild(tile);
    });
    fragment.appendChild(row);

});

currentTile = tiles[0][0]
grid.append(fragment)

function clearCurrent() {
    //if (currentTile.style.backgroundColor !== 'black' && currentTile.getAttribute('contenteditable') !== 'false') {
    currentTile.style.backgroundColor = '#e0e0e0';
    //}

}

function highLightCurrent() {

    if (currentTile && currentTile.style.backgroundColor !== 'black' && currentTile.getAttribute('contenteditable') !== 'false') {

        currentTile.style.backgroundColor = 'yellow';

    } else {

        console.error('currentTile is blocked or undefined.');


    }
}

function moveCurrentTile(row, col) {
    row = parseInt(row);
    col = parseInt(col);
    if (direction) {
        if (col + 1 < tiles[row].length  && tiles[row][col + 1].style.backgroundColor !== "black") {

            clearCurrent()
            currentTile = tiles[row][col + 1];
            highLightCurrent();
        }
    } else {
        if (row + 1 < tiles.length  && tiles[row+1][col].style.backgroundColor !== "black") {
            clearCurrent()
            currentTile = tiles[row + 1][col];
            highLightCurrent();
        }
    }
     currentTile.focus();
}
function moveBackCurrentTile(row, col) {
    row = parseInt(row);
    col = parseInt(col);
    if (direction) {
        if (col - 1 >= 0 && tiles[row][col - 1].style.backgroundColor !== "black" ) {

            clearCurrent()
            currentTile = tiles[row][col - 1];
            highLightCurrent();
       }
    } else {
        if (row - 1 >= 0 && tiles[row-1][col].style.backgroundColor !== "black" ) {
            clearCurrent()
            currentTile = tiles[row -1][col];
            highLightCurrent();
        }
    }
     currentTile.focus();
}
function handleDirectionSwap(row,col){
    if(direction){
        if((!checkBounds(row+1,col) || tiles[row+1][col].style.backgroundColor === "black") && (!checkBounds(row-1,col) || tiles[row-1][col].style.backgroundColor === "black" )){
            console.log("invaalid place to swap across dir")
            return;
        }
        else {
            direction = !direction
            return;
        }
    }
    else{
         if(( !checkBounds(row,col+1)  || tiles[row][col+1].style.backgroundColor === "black")  && (!checkBounds(row,col-1) || tiles[row][col-1].style.backgroundColor === "black" )){
            console.log("invaalid place to swap down dir")
             return;
        }
        else {
            direction = !direction
            return;
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
    console.log("won")

}
function handleTextInput(event) {
    const row = parseInt(currentTile.getAttribute('data-row')); // Extract row index
    const col = parseInt(currentTile.getAttribute('data-col')); // Extract column index
    let color = 'lightblue'
    let hint
    if (event.key === " ") {
        event.preventDefault();
        handleDirectionSwap(row,col)
        if (direction || xyDict[`${row},${col}`].length === 1) {
            hint = xyDict[`${row},${col}`][0]
        } else {
            hint = xyDict[`${row},${col}`][1]
        }
        clearHighlights(hintDict)
        highlightTilesHint(hintDict, hint, color)
        highlightHintBox(hint)
        // Prevent space from being entered
        return;
    }

     if (direction ||  xyDict[`${row},${col}`].length === 1) {
        hint = xyDict[`${row},${col}`][0]
    } else {
        hint = xyDict[`${row},${col}`][1]
    }

    if (event.key === "Backspace") {
        event.preventDefault(); // Prevent default backspace behavior
        currentTile.textContent = ""; // Clear the current tile
        moveBackCurrentTile(row, col); // Move focus back
        highlightTilesHint(hintDict, hint, color)
        return;
    }

     if (/^[a-zA-Z0-9]$/.test(event.key)) {
        event.preventDefault(); // Prevent default `contenteditable` behavior
        currentTile.textContent = event.key.toUpperCase(); // Set tile content (convert to uppercase if needed)
    } else {
        event.preventDefault(); // Block invalid inputs
        return;
    }


    currentTile = tiles[row][col]

    clearHighlights(hintDict);

    //if (currentTile.getAttribute('contenteditable') === 'true') {
    //const text = currentTile.textContent.trim(); // Get the entered text and trim any spaces
    const text = event.key


    //console.log(text)
   // console.log(currentTile.textContent.length)
    if (currentTile.textContent.length === 1) {
        currentTile.textContent = event.key.toUpperCase();
       event.preventDefault();
    }//else{
       // currentTile.textContent = event.key;
    //}

    moveCurrentTile(row, col)

    //}
    // currentTile.textContent = text.charAt(0);
    // Process the text input here (e.g., store the value, validate it, etc.)


    //console.log(hint)
    //console.log(`Text entered at [${row}, ${col}]:`);

    highlightHintBox(hint)
   // console.log("DHDIUDDKHDUSHDJHUSHUDHJSID")
    //console.log(hint)
    highlightTilesHint(hintDict, hint, color)
    checkIfWon()


    //}
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


function onHintClick(hintText, hintDict) {
    let color = 'lightblue'
    clearHighlights(hintDict)
    highlightTilesHint(hintDict, hintText, color)
    highlightHintBox(hintText)

    // Add your logic here, e.g., highlight grid tiles or show details
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


function createBlockCells() {

    for (let i = 0; i < blockedCells.length; i++) {
        const [row, col] = blockedCells[i];

        tiles[row][col].style.backgroundColor = "black";
        tiles[row][col].setAttribute('contenteditable', 'false'); // Disable editing

    }
}

function createIndexCellNumbers(jsonData) {
    for (let j = 0; j < jsonData.length; j++) {
        const number = document.createElement('span');
        number.classList.add('tile-number');
        number.textContent = j + 1; // Set the index number

        const row = jsonData[j].row;
        const col = jsonData[j].column;

        // Only append the number if there's no existing .tile-number span
        if (!tiles[row][col].querySelector('.tile-number')) {
            tiles[row][col].appendChild(number);
        }

        // Make the tile content editable only for the appropriate tiles
        tiles[row][col].setAttribute('contenteditable', 'true');  // Make this editable tile

        // Optional: Adjust if you need to treat the tile differently based on its content
        tiles[row][col].addEventListener("click", (event) => onTileClick(event, xyDict, hintDict));
    }
}

//Builds "Hint Menu" by taking in across and down hints separately
let acrossHintsList = document.querySelector('#acrossHints');
acrossHints.forEach(hint => {
    let listItem = document.createElement('li');
    listItem.addEventListener("click", () => onHintClick(hint, hintDict));
    listItem.textContent = hint;

    acrossHintsList.appendChild(listItem);
});

let downHintsList = document.querySelector("#downHints");
downHints.forEach((hint) => {
    let listItem = document.createElement("li");
    listItem.addEventListener("click", () => onHintClick(hint, hintDict));

    listItem.textContent = hint;
    downHintsList.appendChild(listItem);
});
//console.log(xyDict)
//console.log(hints)


//createIndexCellNumbers(data)
createBlockCells()

document.getElementById('autocheckButton').addEventListener('click', onAutoCheckClick);
document.getElementById('revealButton').addEventListener('click', onRevealClick);

function onRevealClick() {
    const letterDict = createRealWordDict(data)
    //console.log(data)
   // console.log(letterDict)

    for (let i = 0; i < tiles.length; i++) { // Loop through rows
        for (let j = 0; j < tiles[i].length; j++) { // Loop through columns
            const key = `${i},${j}`; // Form the key for the current tile
            tiles[i][j].textContent = letterDict[key]; // Set the letter if it exists in the dictionary

        }
    }
}

function onAutoCheckClick() {
    console.log("Autocheck button clicked!");
    const letterDict = createRealWordDict(data)
    //console.log(data)
   // console.log(letterDict)


    for (let i = 0; i < tiles.length; i++) { // Loop through rows
        for (let j = 0; j < tiles[i].length; j++) { // Loop through columns
            const key = `${i},${j}`; // Form the key for the current tile
            if( tiles[i][j].textContent !== letterDict[key] && tiles[i][j].textContent !== "" && tiles[i][j].style.backgroundColor !=="black" ) {
                tiles[i][j].style.backgroundColor="red" // Set the letter if it exists in the dictionary
            }
        }
    }
    // Add your Autocheck logic here
    // For example:
    // - Validate the grid
    // - Check answers
}





