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
    # Try all starting nodes, just to be safe!
    S = set(graph.keys())
    n = len(S)
    best = -inf

    for start in S:
        print(start)
        current = S - {start}

        while True:
            most = -inf
            target = None
            all_edges = 0
            for node in current:
                in_other = graph[node] - current
                found = len(in_other)
                if found > most:
                    target = node
                    most = found
                all_edges += found
            if all_edges == 3:
                best = max(best, len(current) * (n - len(current)))
                break
            if target is None:
                break
            current.remove(target)
    return best


raw_input = split_lines("inputs/day25.txt")
graph = parse(raw_input)
part1 = partition(graph)
print(part1)
