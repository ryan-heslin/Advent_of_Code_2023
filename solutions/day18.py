from collections import deque
from itertools import groupby
from math import copysign

import utils.utils as ut


def parse(lines, part1 = True):
    result = []
    directions = ("R", "D", "L", "U")
    for line in lines:
        dir, num, hex = line.split(" ")
        hex =  hex[1:-1:1]
        if part1:
            num = int(num)
        else:
            num = int(hex[1:6], 16)
            dir = directions[int(hex[-1])]
        result.append([dir, num])
    return result


def get_vertices(lines):
    vertices = [0]
    length = 1
    current = vertices[-1]
    mapping = {"U": -1j, "R": 1, "D": 1j, "L": -1}
    for line in lines[:-1]:
        new = current + mapping[line[0]] * line[1]
        vertices.append(new)
        length += ut.manhattan(current, new) 
        current = new
    return vertices, length + ut.manhattan(current, vertices[0])


def shrink(num):
    return num - copysign(1, num)


def shoelace(vertices):
    return 0.5 * sum(
        (left.real * right.imag) - (left.imag * right.real)
        for left, right in zip(vertices, vertices[1:] + [vertices[0]])
    )
    


def draw_border(lines):
    current = 0
    vertices = {current}
    mapping = {"U": -1j, "R": 1, "D": 1j, "L": -1}
    for line in lines:
        direction = mapping[line[0]]
        target = line[1]
        for _ in range(target):
            current += direction
            vertices.add(current)
    return vertices


def flood_fill(border):
    extrema = ut.extrema(border)
    directions = {-1j, 1, 1j, -1}
    # So polygon borders not on edges
    extrema["xmin"] -= 1
    extrema["xmax"] += 1
    extrema["ymin"] -= 1
    extrema["ymax"] += 1
    outside = set()

    for i in range(extrema["xmin"], extrema["xmax"] + 1):
        for j in range(extrema["ymin"], extrema["ymax"] + 1):
            current = complex(i, j)
            if current in outside or current in border:
                continue
            queue = deque([complex(i, j)])
            inside = True
            visited = {current}

            #breakpoint()
            if current == 4j:
                breakpoint()
            while queue:
                current = queue.pop()
                for direction in directions:
                    neighbor = direction + current
                    if neighbor in border or neighbor in visited :
                        continue
                    # Outside polygon
                    if not (
                        extrema["xmin"] <= neighbor.real <= extrema["xmax"]
                        and extrema["ymin"] <= neighbor.imag <= extrema["ymax"]
                    ):
                        inside = False
                    elif neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
                        
            if inside:
                return border | visited
            else:
                outside = visited
    return border

# Pick's theorem
def pick(interior, border):
    return interior + border // 2 + 1

def area(border, vertices):
    return int(pick(shoelace(vertices), border))

raw_input = ut.split_lines("inputs/day18.txt")
data = parse(raw_input)
vertices, border = get_vertices(data)
part1 = area(border, vertices)
data = parse(raw_input, False)
print(part1)

vertices, border = get_vertices(data)
part2 = area(border, vertices)
print(part2)
