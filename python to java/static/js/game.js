console.log("yo im here")

let grid = document.querySelector('#game')

let fragment = document.createDocumentFragment();

Array.from({length: size }).forEach(()=> {
    let row = document.createElement('div');
    row.classList.add('row');

    Array.from({length: size }).forEach(()=> {
        let tile = document.createElement('div');
        tile.classList.add('tile');

        row.appendChild(tile);

    });
    fragment.appendChild(row);

    });

grid.append(fragment)