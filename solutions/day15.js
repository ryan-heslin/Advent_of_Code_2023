const fs = require("fs");

function HASH(chars){ 
    let current = 0;
    for(char of chars){ 
        current += char.charCodeAt();
        current *= 17;
        current %= 256;
    }
    return current;
}

function focusing_power(boxes){ 
    let result =0;
    for(let i=0; i< boxes.length; i++){
        let box = boxes[i];
        let num = i + 1;
        for(let j=0; j < box.length; j++){
            result += num *(j+1) * box[j][1] 
        }
    }
    return result;
}

function arrange(lenses){ 
    let part1 = 0;
    let length = 256;
    let boxes =Array.from(Array(length), () => []); 
    let pattern = /([a-z]+)(-|=)(\d+)?/

    for(lens of lenses){ 
        part1 += HASH(lens);
        let parts = lens.match(pattern);
        let label = parts[1];
        let box = HASH(label);

        if (parts[2] == "-"){ 
            for(let i = 0; i < boxes[box].length; i++){
                //Do nothing if no lens with label in box
                if (boxes[box][i][0] == label){ 
                    boxes[box].splice(i, 1);
                }
            }
        }else{ 
            let done = false;
            let item = [label, parseInt(parts[3])];
            for(let i = 0; i < boxes[box].length; i++){
                //Do nothing if no lens with label in box
                if (boxes[box][i][0] == label){ 
                    boxes[box][i] = item;
                    done = true;
                    break
                }
            }
            if (!done){ 
                boxes[box].push(item);
            }
        }
    }

    return [part1, focusing_power(boxes)];
}

const raw_input = fs.readFileSync('inputs/day15.txt', 'utf-8').toString().replace("\n", "").split(",");
const parts = arrange(raw_input);
console.log(parts[0]);
console.log(parts[1]);
