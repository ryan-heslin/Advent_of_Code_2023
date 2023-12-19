const fs = require("fs");

function parse(lines){ 
    return [...lines.map((x) => x.split("").map((x) => parseInt(x)))];
}

function pair_equal(x, y){ 
    return (x[0] == y[0]) && (x[1] == y[1]);
}

function dijkstra(start, goal, graph){
    let max_straight = 3;
    let xmin = ymin = 0;
    let xmax = graph[0].length -1;
    let dist = {};
    let part1 = Infinity;
    let ymax = graph.length -1;
    let queue = [{"x" : start[0], "y" : start[1], "direction" : [1, 0], "remaining" : 3, "distance" : graph[start[1]][start[0]]},{"x" : start[0], "y" : start[1], "direction" : [0, 1], "remaining" : 3, "distance" : graph[start[1]][start[0]]}] 

    // Only left, right, straight
    while(queue.length){ 
         let best = -Infinity;
         let choice = NaN;
         for(let i =0; i< queue.length; i++){ 
             if (queue[i]["distance"] > best){ 
                 best = queue[i]["distance"];
                 choice = i;
             }
         }
        let current = queue.pop();
        let x = current["x"];
        let y = current["y"];
        let direction = current["direction"];
        let this_distance = current["distance"];

        let key = [x, y, direction, current["remaining"]].toString();
        if ((key in dist) && this_distance >= dist[key]){ 
             continue;
         }
        dist[key] = this_distance;
        let at_goal = pair_equal([x, y], goal);
        //console.log(current)
        if(at_goal && this_distance < part1){ 
            part1 = this_distance;
        }else if (!(at_goal) && (this_distance <= part1)){ 
            let new_remaining = current["remaining"] -1;
            //Going left/right
            if (Math.abs(direction[0]) == 1){ 
                if(y > ymin){ 
                    queue.push({"x" : x, "y" : y -1, "direction" : [0, -1], "remaining" : max_straight, "distance" : this_distance + graph[y-1][x] });
                }
                if(y < ymax){ 
                    queue.push({"x" : x, "y" : y +1, "direction" : [0, 1], "remaining" : max_straight, "distance" : this_distance + graph[y + 1][x] });
                }
                // Straight
                let new_x = x + direction[0];
                if ( (new_remaining > 0) && (new_x >= xmin) && (new_x <= xmax)){ 
                    queue.push({"x" : new_x, "y" : y, "direction" : direction, "remaining" : new_remaining, "distance" : this_distance+ graph[y][new_x] })
                }
            // Going up/down
            }else{
            if(x > xmin){ 
                queue.push({"x" : x-1, "y" : y , "direction" : [-1, 0], "remaining" : max_straight, "distance" : this_distance + graph[y][x - 1] });
            }
            if(x < xmax){ 
                queue.push({"x" : x+1, "y" : y , "direction" : [1, 0], "remaining" : max_straight, "distance" : this_distance + graph[y ][x +1] });
            }
            // Straight
            let new_y = y + direction[1];
            if ( (current["remaining"] > 0) && (new_y >= ymin) && (new_y <= ymax )) { 
                queue.push({"x" : x , "y" : new_y, "direction" : direction, "remaining" : new_remaining, "distance" : this_distance+ graph[new_y][x] });
            }
            }
        }
        }
    console.log(dist)
    return part1;
}

const raw_input = fs.readFileSync('inputs/day17.txt', 'utf-8').toString().replace(/\n+$/, "").split("\n");
const graph = parse(raw_input);
const goal = [graph[0].length -1, graph.length -1];
const start = [0, 0]
const part1 = dijkstra(start, goal, graph);
console.log(part1);
