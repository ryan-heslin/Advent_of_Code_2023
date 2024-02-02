from collections import defaultdict
from math import inf

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


# Algorithm "borrowed" from https://www.reddit.com/r/adventofcode/comments/18qbsxs/2023_day_25_solutions/
def partition(graph):
    S = set(graph.keys())
    n = len(S)

    while True:
        most = -inf
        target = None
        all_edges = set()
        for node in S:
            in_other = {n for n in graph[node] if n not in S}
            found = len(in_other)
            if found > most:
                target = node
                most = found
            all_edges |= {tuple(sorted((node, dest))) for dest in in_other}
        if len(all_edges) == 3:
            return len(S) * (n - len(S))
        S.remove(target)


raw_input = split_lines("inputs/day25.txt")
graph = parse(raw_input)
part1 = partition(graph)
print(part1)
