const fs = require('fs');

function parse_lines(lines) { 
    let result = {};
    for(line of lines) { 
        let nodes = [...line.matchAll(/[A-Z]{3}/g)];
        result[nodes[0][0]] = [nodes[1][0], nodes[2][0]];
    }
    return result;
}

function find(directions, indices, start, test){ 
    let current = start;
    let goal = "ZZZ";
    let n_indices = indices.length;
    let steps = 0;
    
    while (!(test(current))){ 
        let choice = indices[steps % n_indices];
        let next = directions[current][choice];
        current = next;
        steps ++;
    }
    return steps;
}

function gcd(a, b){ 
    while (b != 0){ 
        let t = b;
        b = a % b;
        a = t;
    }
    return a;
}

function lcm(a, b){ 
    return Math.abs(a) * (Math.abs(b) / gcd(a, b));
}

// TO generically find cycle: find repeat of direction index and node
// Some Reddit conversation on this point I copied for later
//[–]evouga 5 points 5 hours ago 

// You are right that it’s not purely CRT, if a ghost encounters multiple ??Z nodes along its cycle. But for each choice of ??Z node encountered by each ghost, you can use CRT to solve for the time all ghosts hit their chosen node (and the final answer is the minimum over those choices)
//
//     permalinkembedsaveparentreportreply
//
// [–]taylorott 2 points 5 hours ago 
//
// ^ This right here. One thing to note is that any given ??Z node encountered by a ghost could potentially correspond to multiple remainders (since a true period must be divisible by the the LR string length), which is another thing to that must be iterated over when searching for the minimum.
function solve_ghost(directions, indices, targets){ 
    let periods = targets.map((x) => find(directions, indices, x, (x) => x.substr(2, 3) == "Z"))
    return periods.reduce(lcm);
}

const raw_input = fs.readFileSync('inputs/day8.txt', 'utf-8').toString().split("\n\n");
let indices = raw_input[0].split("").map((x) => x == "R" ? 1 : 0);
let directions = parse_lines(raw_input[1].replace(/\n+$/, "").split("\n"));
let start = "AAA";
const part1 = find(directions, indices, start, (x) => x == "ZZZ");
console.log(part1);


let starts = [...Object.keys(directions)].filter((x) => x.substring(2, 3) == "A");
const part2 = solve_ghost(directions, indices, starts)
console.log(part2)
