from collections import OrderedDict
from copy import deepcopy
from enum import Enum
from itertools import cycle
from operator import attrgetter

from utils.utils import split_lines

mapping = {".": "OPEN", "#": "CUBE", "O": "ROUND"}
Coordinate = Enum("Coordinate", tuple(mapping.values()))


def parse(lines):
    return {
        complex(i, j): Coordinate[mapping[char]]
        for j, line in enumerate(reversed(lines))
        for i, char in enumerate(line)
    }


def total_load(grid, offset):
    grid = dict(grid)
    rounded = Coordinate.ROUND
    closed = {rounded, Coordinate.CUBE}
    load = 0
    keys = {
        1j: lambda x: (-x.imag, x.real),
        -1: lambda x: (x.real, x.imag),
        -1j: lambda x: (x.imag, x.real),
        1: lambda x: (-x.real, x.imag),
    }

    for coord in sorted(grid.keys(), key=keys[offset]):
        el = grid[coord]

        if el == rounded:
            current = coord
            grid[current] = Coordinate.OPEN
            while True:
                new = current + offset
                if new not in grid or grid[new] in closed:
                    grid[current] = rounded
                    load += current.imag + 1
                    break
                current = new

    return grid, int(load)


def predict(grid):
    results = OrderedDict()
    offsets = (1j, -1, -1j, 1)
    load = 0

    while True:
        for offset in offsets:
            grid, load = total_load(grid, offset)
        hash = frozenset(zip(grid.keys(), grid.values()))
        if hash in results:
            print(load)
            return results, tuple(i for i, k in enumerate(results.keys()) if k == hash)
        results[hash] = load


raw = split_lines("inputs/day14.txt")
grid = parse(raw)
_, part1 = total_load(deepcopy(grid), 1j)
print(part1)

result, i = predict(grid)
for  j, k  in enumerate(tuple(result.keys())):
    if j < i[0]:
        result.pop(k)
cycle_length = len(result) 
n = 1000000000
iteration = ((n - i[0]  ) % cycle_length) -1
part2 = result[tuple(result.keys())[iteration  % cycle_length]]
print(part2)
