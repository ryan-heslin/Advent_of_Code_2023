from collections import defaultdict
import heapq
from math import inf

import utils.utils as ut


class ComparableComplex(complex):

    def __lt__(self, other):
        return abs(self) > abs(other)

# Standard quadratic approximation
def lagrange(X, Y):
    degree = 3
    denoms = ((X[0] - X[1]) *(X[0] - X[2]), 
              (X[1] - X[0]) * (X[1] - X[2]), 
              (X[2] - X[0]) * (X[2] - X[1])
              )
    quadratic = sum(Y[i] / denoms[i] for i in range(degree))
    linear = (-X[1] - X[2],  -X[0] - X[2] , -X[0] - X[1])
    linear = sum((Y[i] * linear[i]) /denoms[i] for i in range(degree))
    constant =(X[1] * X[2] , X[0] * X[2] , X[0] * X[1])
    constant = sum((Y[i] * constant[i]) /denoms[i] for i in range(degree))
    return quadratic, linear, constant


def parse(lines):
    result = {}
    result.update(
        {
            complex(y, x): char == "#"
            for y, line in enumerate(lines)
            for x, char in enumerate(line)
        }
    )
    return result

def dijkstra(start, graph, max_dists, neighbors):
    queue = [(0, ComparableComplex(start))]
    heapq.heapify(queue)
    visited = {(0, ComparableComplex(start))}
    greatest = max(max_dists)
    result = defaultdict(set)
    extrema = ut.extrema(graph)
    xrange = extrema["xmax"] - extrema["xmin"] + 1
    yrange = extrema["ymax"] - extrema["ymin"] + 1

    while True:
        try:
            dist, current = heapq.heappop(queue)
        except IndexError:
            return result
        if dist in max_dists:
            result[dist].add(current)
            if dist == greatest:
                continue
        dist += 1

        for neighbor in neighbors(current):
            clamped_neighbor = complex(neighbor.real % xrange, neighbor.imag % yrange)
            new = (dist, ComparableComplex(neighbor))
            if not (graph[clamped_neighbor] or new in visited):
                visited.add(new)
                heapq.heappush(queue, new)

def find_start(lines):
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == "S":
                return complex(x, y)


raw_input = ut.split_lines("inputs/day21.txt")
graph = parse(raw_input)
start = find_start(raw_input)
extrema = ut.extrema(graph)
neighbors = ut.neighbors(-inf, inf, -inf, inf,  diag=False, combos=None)
# Start has to be in dead center for trick to work
extent = extrema["xmax"] - extrema["xmin"] + 1
assert (
    start
    and start.real == extent // 2
    and start.imag == (extrema["ymax"] - extrema["ymin"] + 1) // 2
)

half = extent // 2
data = dijkstra(start, graph, (half,            half + extent, half + extent * 2), neighbors)
coefs = lagrange(range(3), list(map(len, data.values())))
final_dist = 26501365
repeats = final_dist // extent
part2 = int((coefs[0] * (repeats ** 2)) + (coefs[1] * repeats) + coefs[2])
print(part2)
