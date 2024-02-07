from utils.utils import neighbors
from utils.utils import split_lines
from math import prod


class Number:
    def __init__(self, coord, val):
        self.coords = set([coord])
        self.val = val

    def __add__(self, other):
        self.coords.update(other.coords)
        self.val *= 10
        self.val += other.val
        return self

    def __repr__(self) -> str:
        return str(self.val)


def parse(lines):
    numbers = {}
    symbols = {}

    for y, line in enumerate(lines):
        num_start = None
        for x, char in enumerate(line):
            current_coord = complex(x, y)
            if char.isdigit():
                new_num = Number(current_coord, int(char))
                if num_start is not None:
                    numbers[num_start] += new_num
                else:
                    num_start = current_coord
                    numbers[num_start] = new_num
            else:
                # Exiting number
                if num_start is not None:
                    this = numbers[num_start]
                    num_start = None
                    for coord in this.coords:
                        numbers[coord] = this 
                # Found symbol
                if char != ".":
                    symbols[current_coord] = char

    return numbers, symbols

def solve(numbers, symbols, neighbors):
    gear = "*"
    counted = set()
    part1 = part2 = 0

    for coord, symbol in symbols.items():
        gear_neighbors = set()
        for neighbor in neighbors(coord):
            if neighbor in numbers:
                number = numbers[neighbor]
                if neighbor not in counted:
                    part1 += number.val
                    counted.update(number.coords)
                if symbol == gear:
                    gear_neighbors.add(frozenset(number.coords))
        if len(gear_neighbors) == 2:
            part2 += prod(numbers[next(iter(c))].val for c in gear_neighbors)

    return part1, part2



raw = split_lines("inputs/day3.txt")
xmin = ymin = 0
xmax = len(raw[0]) - 1
ymax = len(raw) - 1
find_neighbors = neighbors(xmin, xmax, ymin, ymax, diag = True)
numbers, symbols = parse(raw)
part1, part2 = solve(numbers, symbols, find_neighbors)
print(part1)
print(part2)
