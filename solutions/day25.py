from collections import defaultdict, deque
from copy import deepcopy
from itertools import combinations
from utils.utils import split_lines

def parse(lines):
    result = defaultdict(set)
    for line in lines:
        source, dests = line.split(": ")
        dests = set(dests.split(" "))
        result[source].update(dests)

        for dest in dests:
            result[dest].add(source)
    return result

def find_cc(graph):
    n_components =  0
    nodes = set(graph.keys())
    sizes = []

    while nodes:
        size = 1
        n_components += 1
        start = nodes.pop()
        queue = deque([start])

        while queue:
            current = queue.pop()
            for neighbor in graph[current]:
                # Not yet explored, so remove
                if neighbor in nodes:
                    queue.append(neighbor)
                    nodes.remove(neighbor)
                    size += 1
        sizes.append(size)
    
    if n_components == 2:
        return sizes[0] * sizes[1]

def get_edges(graph):
    return {tuple(sorted((source, dest))) for source, dests in graph.items() for dest in dests }

def remove_edges(graph, edges):
    new = deepcopy(graph)
    for source, dests in graph.items():
        for dest in dests:
            if tuple(sorted((source, dest))) in edges:
                new[source].discard(dest)
                new[dest].discard(source)
    return new

def solve(graph, edges):
    i = 0
    for group in combinations(edges, r = 3):
        i += 1
        new_graph = remove_edges(graph, group)
        result = find_cc(new_graph)
        if result is not None:
            return result
        if i == 1000:
            print(i)

raw_input = split_lines("inputs/day25.txt")
graph = parse(raw_input)
edges = get_edges(graph)
part1 = solve(graph, edges)
print(part1)
