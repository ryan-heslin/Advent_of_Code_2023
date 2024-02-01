from collections import defaultdict
from collections import deque
from functools import cache
from math import inf

from utils.utils import split_lines


def print_path(path, graph):
    return "\n".join(
        "".join(
            graph[complex(x, y)] if complex(x, y) not in path else "O"
            for x in range(23)
        )
        for y in range(23)
    )


def get_path(graph, start):
    current = start
    queue = []
    inside = True

    while inside:
        queue.append(current)
        for dir in {-1, 1, 1j, -1j}:
            new = dir + current
            try:
                char = graph[int(new.imag)][int(new.real)]
            except:
                continue
            if char == "O" and new not in queue:
                current += dir
                break
        else:
            inside = False

    return queue


def mark_path(lines):
    return {
        complex(x, y)
        for y, line in enumerate(lines)
        for x, char in enumerate(line)
        if char in {"S", "O"}
    }


def find_start(lines, reverse=False):
    loop = reversed(list(enumerate(lines))) if reverse else enumerate(lines)
    for y, line in loop:
        for x, char in enumerate(line):
            if char == ".":
                return complex(x, y)


def parse(lines):
    return {
        complex(x, y): char
        for y, line in enumerate(lines)
        for x, char in enumerate(line)
    }


def make_neighbors(graph, directions):
    @cache
    def result(coord):
        result = set()
        offsets = directions[graph[coord]]
        for offset in offsets:
            new = coord + offset
            if new in graph and graph[new] != "#":
                result.add(new)
        return frozenset(result)

    return result


def node_paths(start, neighbors, targets):
    queue = deque([[start]])

    while queue:
        current = queue.pop()
        current_coord = current[-1]

        for neighbor in neighbors(current_coord):
            if neighbor not in current:
                # New path found to node, so end here
                if neighbor in targets and neighbor != current_coord:
                    # Longer path found
                    yield start, neighbor, len(current)
                else:
                    queue.append(current + [neighbor])


def reduce_graph(graph, start, goal, neighbors):
    targets = {c for c  in graph.keys() if len(neighbors(c)) > 2} | {start, goal}
    result = defaultdict(dict)
    for target in targets:
        gen = node_paths(target, neighbors, targets)
        # Exhaust results from generator
        while True:
            try:
                this = next(gen)
                if this is not None:
                    start, dest, length = this
                    result[start][dest] = max(result[start].get(dest, -inf), length)
                    result[dest][start] = max(result[dest].get(start, -inf), length)
            except StopIteration:
                break
    return result


def solve(graph, start, goal):
    queue = deque([(set(), start,  0)])
    result = -inf

    while queue:
        current, current_coord, current_dist = queue.pop()
        if current_coord == goal:
            result = max(result, current_dist)
        else:
            neighbors = graph[current_coord]
            for neighbor, dist in neighbors.items():
                if neighbor not in current:
                    new_dist = current_dist + dist
                    queue.append((current | {current_coord}, neighbor, new_dist))
    return result


def dijkstra(graph, start, goal, threshold, neighbors):
    queue = deque([(set(), start)])
    part1 = threshold

    while queue:
        previous, current_coord = queue.pop()
        if current_coord == goal:
            part1 = max(len(previous), part1)
            continue

        for neighbor in neighbors(current_coord):
            if neighbor not in previous:
                queue.append((previous | { current_coord }, neighbor))

    return part1 


raw_input = split_lines("inputs/day23.txt")
directions = {
    ".": frozenset({-1, 1, -1j, 1j}),
    "^": frozenset({-1j}),
    ">": frozenset({1}),
    "v": frozenset({1j}),
    "<": frozenset({-1}),
    "#": frozenset(),
}
start = find_start(raw_input)
goal = find_start(raw_input, reverse=True)
graph = parse(raw_input)
neighbors = make_neighbors(graph, directions)
part1 = dijkstra(graph, start, goal, -inf, neighbors)
print(part1)


directions[">"] = directions["v"] = directions["<"] = directions["^"] = directions["."]
neighbors = make_neighbors(graph, directions)
reduced = reduce_graph(graph, start, goal, neighbors)
part2 = solve(reduced, start, goal)
print(part2)
