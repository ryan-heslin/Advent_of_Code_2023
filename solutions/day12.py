import re
from collections import defaultdict
from functools import cache

from utils.utils import list_map
from utils.utils import split_lines


# .
@cache
def decide_dot(group_index, group_size, _, target_length):
    # Not in group
    if group_size == 0:
        return (group_index, group_size)
    # Exiting group
    elif group_size == target_length:
        return (group_index + 1, 0)


# #
@cache
def decide_hash(group_index, group_size, n_groups, target_length):
    # Starting group
    if group_size == 0 and group_index < n_groups:
        return (group_index, 1)
    # Advance current group
    elif group_size < target_length:
        return (group_index, group_size + 1)


def parse(line):
    parts = line.split(" ")
    parts[1] = list_map(parts[1].split(","), int)
    return parts


def bfs(string, groups):
    # group_index, group_size
    start = (
        0,
        0,
    )
    n_groups = len(groups)
    reference = groups + [0]
    last = {start: 1}
    choices = {".": (decide_dot,), "#": (decide_hash,), "?": (decide_dot, decide_hash)}

    for char in string:
        next = defaultdict(lambda: 0)
        choosers = choices[char]

        for state in list(last.keys()):
            count = last.pop(state)
            group_index, group_size = state
            target_length = reference[group_index]

            for chooser in choosers:
                result = chooser(group_index, group_size, n_groups, target_length)
                if result is not None:
                    next[result] += count
        last = next
    correct = {(n_groups, 0), (n_groups - 1, reference[-2])}
    return sum(v for k, v in last.items() if k in correct)


def reparse(data, n=5):
    return [["?".join([l[0]] * n), l[1] * n] for l in data]


raw = split_lines("inputs/day12.txt")
parsed = list_map(raw, parse)
part1 = sum(bfs(line, nums) for line, nums in parsed)
print(part1)

new_parsed = reparse(parsed)
part2 = sum(bfs(line, nums) for line, nums in new_parsed)
print(part2)
