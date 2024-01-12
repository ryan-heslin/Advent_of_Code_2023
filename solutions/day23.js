const fs = require("fs");

function pair_equal(x, y){
    return (x[0] == y[0]) && (x[1] == y[1]);
}

function parse(lines){
    return [...lines.map((x) => x.split(""))];
}

function get_neighbors(graph){
    let xmin = ymin =0;
    let xmax = graph[0].length - 1;
    let ymax = graph.length -1;
    //let result = [...Array( ymax).map(() => Array(xmax))]
    let result = []
    let map = {};
    // Clockwise order
    let iterations = {"." : [[0, -1], [1, 0], [0, 1], [-1, 0]], "#" : [], "<" : [[-1, 0], [0, -1], [1, 0], [0, 1]],
        "^" : [[0, -1], [1, 0], [0, 1], [-1, 0]],
        ">" : [[1, 0], [0, 1], [-1, 0], [0, -1]],
        "v" : [[0, 1], [-1, 0], [0, -1], [1, 0]]}

    for(let row = ymin; row <= ymax; row++){
        result.push([]);
        for(let col =xmin; col <= xmax; col ++){
            result[row].push([]);
            let current = [row, col];
            let char = graph[row][col];
            let shifts = iterations[char];
            if (graph[row][col] != "#"){
            //result[row][col] = [];
            for(dir of shifts){
                let current = [row + dir[0], col + dir[1]];
                if (((current[1] >= xmin) && current[1] <= xmax) && ((current[0] >= ymin) && current[0] <= ymax) && graph[current[0]][current[1]] != "#"){
                    result[row][col].push(current);
                }
            }

            }
        }
    }
    return result;
}

function find_start(lines){ 
    let endpoint = lines.length -1;
    for(let i =0; i< lines[0].length; i++){ 
        if (lines[0][i] == "."){ 
            let start = [0, i];
            for(let j =0; j< lines[endpoint].length; j++){ 
                if (lines[endpoint][j] == "."){ 
                    return [start, [endpoint, j]]
                }
        }
    }
    }
}

function dijkstra(start, goal, neighbors){ 
    let queue = [[new Set([]), JSON.stringify(start)]];
    let target = JSON.stringify(goal)
    let best = -Infinity;

    while (queue.length){ 
        let current = queue.pop();
        let previous = current[0]
        
        console.log(current[1])
        if (current[1] == target) { 
            best = Math.max(previous.size, best);
            console.log(best)
            continue
        }
        let current_coord = JSON.parse(current[1]);
        for(neighbor of neighbors[current_coord[0]][current_coord[1]]){
            let string = JSON.stringify(neighbor); 
            //console.log(string)
            if (!(previous.has(string))){ 
                let copy = new Set(previous);
                copy.add(current[1])
                queue.push([copy, string]);
            }
    }
}
    return best ; 
}



const raw_input = fs.readFileSync('inputs/day23.txt', 'utf-8').toString().replace(/\n+$/, "").split("\n");
const graph = parse(raw_input);
let iterations = {"." : [[0, -1], [1, 0], [0, 1], [-1, 0]], "#" : [], "<" : [[-1, 0], [0, -1], [1, 0], [0, 1]],
        "^" : [[0, -1], [1, 0], [0, 1], [-1, 0]],
        ">" : [[1, 0], [0, 1], [-1, 0], [0, -1]],
        "v" : [[0, 1], [-1, 0], [0, -1], [1, 0]]}
const endpoints = find_start(graph);
const neighbors = get_neighbors(graph);
const part2 = dijkstra(endpoints[0], endpoints[1], neighbors);
console.log(part2)
// Part 1 restriction
for (char of ["<", "^", ">", "v"] ){ 
    iterations[char] = [ iterations[char] ][0]
}
const new_neighbors = get_neighbors(graph);
const part1 = dijkstra(endpoints[0], endpoints[1], new_neighbors);
console.log(part1)
