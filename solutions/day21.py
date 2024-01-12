from collections import defaultdict
from collections import deque
from itertools import chain
from itertools import zip_longest
from math import inf
import heapq

import utils.utils as ut

class ComparableComplex(complex):


    def __lt__(self, other):
        return abs(self) > abs(other)

def interior(size):
    return 2 * (size * (size - 1)) + 1


def parse(lines):
    result = defaultdict(lambda: False)
    result.update(
        {
            complex(y, x): char == "#"
            for y, line in enumerate(lines)
            for x, char in enumerate(line)
        }
    )
    return result


def add_border(graph):
    extrema = ut.extrema(graph)
    coords = chain(
        zip_longest(
            range(extrema["xmin"] - 1, extrema["xmax"] + 2),
            (),
            fillvalue=extrema["ymin"] - 1,
        ),
        zip_longest(
            range(extrema["xmin"] - 1, extrema["xmax"] + 2),
            (),
            fillvalue=extrema["ymax"] + 1,
        ),
        zip_longest(
            (),
            range(extrema["ymin"] - 1, extrema["ymax"] + 2),
            (),
            fillvalue=extrema["xmin"] - 1,
        ),
        zip_longest(
            (),
            range(extrema["ymin"] - 1, extrema["ymax"] + 2),
            (),
            fillvalue=extrema["xmax"] + 1,
        ),
    )
    return graph | {coord: False for coord in coords}


def dijkstra(start, graph, max_dist, neighbors):
    queue = [(0, ComparableComplex(start))]
    heapq.heapify(queue)
    dist = defaultdict(lambda: inf)
    visited = set((0, ComparableComplex(start)))
    paths = defaultdict(set)
    extrema = ut.extrema(graph)
    xrange = extrema["xmax"] - extrema["xmin"] + 1
    yrange = extrema["ymax"] - extrema["ymin"] + 1

    while True:
        try:
            dist, current = heapq.heappop(queue)
        except IndexError:
            return paths
        # TODO check if vertex of diamond
        if (dist - 65) % 131 == 0:
            paths[dist].add(current)
        if dist == max_dist:
            continue
        dist += 1

        for neighbor in neighbors(current):
            clamped_neighbor = neighbor.real % xrange, neighbor.imag % yrange
            new = (dist, ComparableComplex(neighbor))
            if not (graph[clamped_neighbor]):
                #visited.add(new)
                heapq.heappush(queue, new)



def find_start(lines):
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == "S":
                return complex(x, y)


raw_input = ut.split_lines("inputs/day21.txt")
graph = parse(raw_input)
start = find_start(raw_input)
neighbors = ut.neighbors(-inf, inf, -inf, inf)
extrema = ut.extrema(graph)
# Start has to be in dead center for trick to work
extent = (extrema["xmax"] - extrema["xmin"] + 1) 
assert (
    start
    and start.real == extent // 2
    and start.imag == (extrema["ymax"] - extrema["ymin"] + 1) // 2
)

max_dist = 64
part1 = len(dijkstra(start, graph, max_dist + 1, neighbors)[max_dist])
print(part1)
max_dist = 26501365
iterations = max_dist   // extent
offset = max_dist % extent
# All fully explored
inner_tiles = interior(max_dist)
# Half explored
border = max_dist
# Plus tiles at cardinal extremes

# raw_input = [" " * xmax] + raw_input + [" " * xmax]
# raw_input = [" " + line + " " for line in raw_input]
start = find_start(raw_input)
graph = parse(raw_input)
result = dijkstra(start, graph, 589 , neighbors)
current = offset + extent
print(result)
# TODO frontier expands as diamond, and number of steps is multiple of grid size
# note size when on edge of grid, find pattern, solve
