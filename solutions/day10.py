from collections import deque
from itertools import product
from math import ceil
from operator import attrgetter
from functools import cache

from utils.utils import neighbors
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

conversions = {
    "|": {1, 1 + 1j, 1 + 2j},
    "-": {0 + 1j, 1 + 1j, 2 + 1j},
    "F": {1 + 1j, 2 + 1j, 1 + 2j},
    "J": {1, 1j, 1 + 1j},
    "L": {1, 1 + 1j, 2 + 1j},
    "7": {1j, 1 + 1j, 1 + 2j},
    ".": set(),
}


def convert_grid(grid):
    result = {}
    multiplier = 3
    # 3 by 3 outputs
    for y, line in enumerate(grid):
        for x, char in enumerate(line):
            xnew = x * multiplier
            ynew = y * multiplier
            offset = complex(xnew, ynew)
            conversion = conversions[char]
            closed = char != "."

            for coord in product(range(multiplier), range(multiplier)):
                coord = complex(*coord)
                result[offset + coord] = closed and coord in conversion

    return result


def infer_start(start_dirs, end_dirs):
    
    match (start_dirs, end_dirs):
        case ((-1, 0), (-1, 0)) | ((1, 0), (1, 0)):
            return "-"
        case ((-1, 0), (0, -1)) | ((0, 1), (1, 0)):  # left-up
            return "L"
        case ((-1, 0), (0, 1)) | ((0, -1), (1, 0)):
            return "F"
        case ((0, 1), (0, 1)) | ((0, -1), (0, -1)):
            return "|"
        case ((0, 1), (-1, 0)) | ((1, 0), (0, -1)):  # down-left
            return "J"
        case ((0, -1), (-1, 0)) | ((1, 0), (0, 1)):  # up-left
            return "7"


def loop_size(start, grid):
    x, y = start
    xmin = ymin = 0
    xmax = len(grid[0]) - 1
    ymax = len(grid) - 1
    dist = 0
    traversed = {complex(x, y)}

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
    start_dirs = (xdir, ydir)

    char = None
    while char != "S":
        # All four spaces in
        x += xdir
        y += ydir
        traversed.add(complex(x, y))
        char = grid[y][x]
        dist += 1

        if char == "S":
            end_dirs = (xdir, ydir)

            start = infer_start(end_dirs, start_dirs)
            grid[y] = grid[y].replace("S", start)
            return ceil(dist / 2), traversed
        xdir, ydir = directions[(char, xdir, ydir)]


def find_start(lines):
    for y, line in enumerate(lines):
        try:
            x = line.index("S")
            return x, y
        except ValueError:
            continue


@cache
def downscale(t, factor):
    return complex(t.real // factor, t.imag // factor)


def flood_fill(grid, xmin, xmax, ymin, ymax, get_neighbors, traversed):
    exposed = set()
    enclosed = set()

    for coord, el in grid.items():
        if (el and downscale(el, 3) not in traversed) or (coord in enclosed or coord in exposed):
            continue
        queue = deque()
        queue.append(coord)
        visited = set()
        open = False

        while queue:
            new = queue.pop()
            visited.add(new)
            open = open or (
                new in exposed
                or (
                    new.real == xmin
                    or new.real == xmax
                    or new.imag == ymin
                    or new.imag == ymax
                )
            )
            new_neighbors = get_neighbors(new)

            for neighbor in new_neighbors:
                # if neighbor in exposed:
                #     open = True
                if not ((grid[neighbor] and downscale(neighbor, 3) in traversed) or neighbor in visited):
                    queue.append(neighbor)
        if open:
            exposed.update(visited)
        else:
            enclosed.update(visited)
    return enclosed


def candidates(enclosed, traversed):
    enclosed = {downscale(c, 3) for c in enclosed}
    return enclosed - traversed


def find_in_loop(enclosed, traversed, xmin, xmax, ymin, ymax):
    result = 0

    for coord in enclosed:
        x = int(coord.real)
        y = int(coord.imag)
        found = False
        for i in range(x + 1, xmax + 1):
            if complex(i, y) in traversed:
                found = True
                break

        if not found:
            break
        found = False

        for i in range(x - 1, xmin - 1, -1):
            if complex(i, y) in traversed:
                found = True
                break
        if not found:
            break
        found = False

        for j in range(y + 1, ymax + 1):
            if complex(x, j) in traversed:
                found = True
                break
        if not found:
            break

        found = False
        for j in range(y - 1, ymin - 1, -1):
            if complex(x, j) in traversed:
                result += 1
                break
    return result


def print_map(grid, xmax, ymax, special):
    if not special:
        special = set()
    return "\n".join(
        "".join(
            "X" if complex(x, y) in special else "#" if grid[complex(x, y)] else "."
            for x in range(xmax + 1)
        )
        for y in range(ymax + 1)
    )


raw = split_lines("inputs/day10.txt")
start = find_start(raw)
part1, traversed = loop_size(start, raw)
print(part1)

xmin = ymin = 0
grid = convert_grid(raw)
xmax = int(max(map(attrgetter("real"), grid.keys())))
ymax = int(max(map(attrgetter("imag"), grid.keys())))
neighbor_finder = neighbors(xmin, xmax, ymin, ymax, diag=False)
enclosed = flood_fill(grid, xmin, xmax, ymin, ymax, neighbor_finder, traversed)
possible = candidates(enclosed, traversed)
part2 = len(possible)
print(part2)
