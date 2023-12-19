from collections import defaultdict
from dataclasses import dataclass
from functools import cache
from itertools import chain
from math import inf
from operator import attrgetter

from utils.utils import split_lines

mapping = {
    ".": {-1: (-1,), -1j: (-1j,), 1: (1,), 1j: (1j,)},
    "/": {1j: (-1,), -1: (1j,), -1j: (1,), 1: (-1j,)},
    "\\": {1j: (1,), -1: (-1j,), -1j: (-1,), 1: (1j,)},
    "|": {-1j: (-1j,), 1j: (1j,), -1: (-1j, 1j), 1: (-1j, 1j)},
    "-": {-1: (-1,), 1: (1,), -1j: (-1, 1), 1j: (-1, 1)},
}


def parse(lines):
    return {
        complex(i, j): mapping[char]
        for j, line in enumerate(lines)
        for i, char in enumerate(line)
    }


def beam_dict():
    return defaultdict(set)


def simulate_beam(grid, start, initial):
    # coord, direction
    current = beam_dict()
    current[start].add(initial)
    traversed = set()
    seen = set()

    while current:
        new = beam_dict()
        for coord, directions in current.items():
            for direction in directions:
                new_coord = coord + direction
                # Moving off grid
                if new_coord not in grid:
                    continue
                traversed.add(new_coord)
                new_directions = grid[new_coord][direction]

                # Add to count of beam in relevant direction on tile if it exists, otherwise create new beam
                new[new_coord].update(new_directions)
        hashed = frozenset(
            (coord, frozenset(d)) 
            for coord, d in new.items()
        )
        # print(hashed)
        if hashed in seen:
            break
        seen.add(hashed)
        current = new

    return len(traversed)


def maximize_energy(grid):
    xmin = ymin = 0
    # TRBL order
    ranges = chain(
        ((complex(x, ymin - 1), 1j) for x in range(xmax + 1)),
        ((complex(xmax + 1, y), -1) for y in range(ymax + 1)),
        ((complex(x, ymax + 1), -1j) for x in range(xmax + 1)),
        ((complex(xmin - 1, y), 1) for y in range(ymax + 1)),
    )

    return max(simulate_beam(grid, start[0], start[1]) for start in ranges)

# Non-naive way:
    # For each mirror, get next mirror (or none, if pointing away) in each direction of reflection
    # Greedily track each beam's course, stopping once in a loop or leaving grid. Memoize this


raw = split_lines("inputs/day16.txt")
grid = parse(raw)
xmax = int(max(grid.keys(), key=attrgetter("real")).real)
ymax = int(max(grid.keys(), key=attrgetter("imag")).imag)
part1 = simulate_beam(grid, -1, 1)
print(part1)

part2 = maximize_energy(grid)
print(part2)
