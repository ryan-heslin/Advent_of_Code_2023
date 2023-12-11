# (1, 0) -> right
# (-1, 0) -> left
# (0, -1) -> up
# (0, 1) -> down
from collections import deque
from functools import cache
from itertools import chain
from itertools import product
from math import ceil

from utils.utils import split_lines

directions = {
    ("|", 0, -1): (0, -1),  # no change, going straight
    ("|", 0, 1): (0, 1),
    ("-", 1, 0): (1, 0),
    ("-", -1, 0): (-1, 0),
    ("F", 0, -1): (1, 0),
    ("F", -1, 0): (0, 1),  # left-down
    ("J", 1, 0): (0, -1),
    ("J", 0, 1): (-1, 0),
    ("L", 0, 1): (1, 0),
    ("L", -1, 0): (0, -1),
    ("7", 1, 0): (0, 1),
    ("7", 0, -1): (-1, 0),
}


def neighbors(xmin, xmax, ymin, ymax, diag=False, combos=None):
    """Cartesian neighbors"""
    if combos is None:
        combos = product(range(-1, 2), range(-1, 2))
    # Each combination of 1-step movements
    shifts = {
        (x, y) for x, y in combos if (x != 0 or y != 0) and (diag or (x == 0 or y == 0))
    }
    print(shifts)

    @cache
    def result(coord):
        result = set()
        for shift in shifts:
            new = (shift[0] + coord[0], shift[1] + coord[1])
            if xmin <= new[0] <= xmax and ymin <= new[1] <= ymax:
                result.add(new)

        return frozenset(result)

    return result


def loop_size(start, grid):
    x, y = start
    xmin = ymin = 0
    xmax = len(grid[0]) - 1
    ymax = len(grid) - 1
    dist = 0
    traversed = set()
    traversed.add(start)

    # Find first valid direction, TRBL order
    if y > ymin and grid[y - 1][x] in ("|", "F", "7"):
        xdir = 0
        ydir = -1
    elif x < xmax and grid[y][x + 1] in ("-", "J", "7"):
        xdir = 1
        ydir = 0
    elif y < ymax and grid[y + 1][x] in ("|", "J", "L"):
        xdir = 0
        ydir = 1
    elif x > xmin and grid[y][x - 1] in ("-", "F", "L"):
        xdir = -1
        ydir = 0
    else:
        raise ValueError("No valid directions")


    first = grid[y + ydir][x + xdir]
    while True:
        # All four spaces in 
        x += xdir
        y += ydir
        char = grid[y][x]
        dist += 1

        if char == "S":
            return ceil(dist / 2), traversed
        # TODO: allow movement onto pipe tiles, but not THROUGH them 
        # Move laterally in spaces between pipes
        # How to handle?
        # Infer S piece type from first, last piece directions
                additions = 
        xdir, ydir = directions[(char, xdir, ydir)]


def find_start(lines):
    for y, line in enumerate(lines):
        try:
            x = line.index("S")
            return x, y
        except:
            continue


def force_int(t):
    return tuple(map(int, t))


def flood_fill(grid, barriers, xmin, xmax, ymin, ymax):
    queue = deque()
    enclosed = set()
    # Which must be non-enclosed
    border = chain(
        product(range(xmin, xmax + 1), (ymin,)),
        product((xmax,), range(ymin, ymax + 1)),
        product(range(xmin, xmax + 1), (ymax,)),
        product((xmin,), range(ymin, ymax + 1)),
    )
    deltas = ((0.5, 0), (0, 0.5), (0.5, 0), (0, 0.5))

    for i, coord in enumerate(border):
        delta = deltas[i // 4]
        if not (coord in barriers):
            queue.append(coord)
        beside = (coord[0] + delta[0], coord[1] + delta[1])
        if not (beside in barriers):
            queue.append(beside)

        while queue:
            current = queue.pop()
            new_neighbors = neighbor_finder(current)
            for neighbor in new_neighbors:
                if not (neighbor in barriers or neighbor in enclosed):
                    queue.append(coord)

    return (len(grid) * len(grid[0])) - len(set(map(force_int, barriers)))


raw = split_lines("inputs/day10.txt")
start = find_start(raw)
part1, traversed = loop_size(start, raw)
print(part1)
xmin = ymin = 0
xmax = len(raw[0])
ymax = len(raw)
combos = product((-0.5, 0, 0.5), (-0.5, 0, 0.5))
neighbor_finder = neighbors(xmin, xmax, ymin, ymax, diag=True)
part2 = flood_fill(raw, traversed, xmin, xmax, ymin, ymax)
print(part2)

# Problems:
# 1. Paths can exist between tiles if not blocked by pipe segments.
# 2. S needs special treatment

# Only count pipe segments as spaces if not part of loop
