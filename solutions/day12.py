import re
from collections import defaultdict
from collections import deque
from functools import cache
from itertools import combinations
from math import inf

from utils.utils import list_map
from utils.utils import split_lines


def parse(line):
    parts = line.split(" ")
    return parts[0], list(map(int, parts[1].split(",")))


memo_combinations = cache(combinations)


def brute_force(line, nums):
    end = len(nums) - 1
    pattern = re.compile(
        r"^\.*#"
        + "#".join(
            "{" + str(num) + r"}\." + ("+" if i < end else "*")
            for i, num in enumerate(nums)
        )
        + "$"
    )
    found = int(bool(re.match(pattern, "".join(line).replace("?", "."))))
    ref = list(line)
    indices = tuple(i for i, char in enumerate(line) if char == "?")
    total = len(indices)

    for r in range(1, total + 1):
        combos = combinations(indices, r=r)
        for combo in combos:
            copy = list(ref)
            for i in indices:
                copy[i] = "#" if i in combo else "."
            # print("".join(copy))
            # print(bool(re.match(pattern, "".join(copy))))
            found += bool(re.match(pattern, "".join(copy)))
    return found


class Node:
    def __init__(self, group_index, cur_group_size):
        self.group_index = group_index
        self.cur_group_size = cur_group_size

    def __hash__(self):
        return hash((self.group_index, self.cur_group_size))

    def __lt__(self, other):
        return (self.group_index, self.cur_group_size) < (
            other.char_index,
            other.group_index,
            other.cur_group_size,
        )

    def __eq__(self, other):
        return type(other) == type(self) and hash(self) == hash(other)

    def __ne__(self, other):
        return type(other) != type(self) or hash(self) != hash(other)

    def __bool__(self):
        return True


# .
@cache
def decide_dot(group_index, group_size, n_groups, target_length):
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

    # Dict of states to add to count?
    for char in string:
        next = defaultdict(lambda: 0)
        choosers = choices[char]

        for state in list(last.keys()):
            count = last.pop(state)
            group_index, group_size = state
            target_length = reference[group_index]

            for  chooser in choosers:
                result = chooser(group_index, group_size, n_groups, target_length)
                if result is not None:
                    next[result] += count
        last = next
    correct = {(n_groups, 0), (n_groups -1, reference[-2])}
    return sum(v for k, v in last.items() if k in correct)
# Multiply by recursive call to remaining string
def reparse(data, n=5):
    return [["?".join([ l[0] ] * n), l[1] * n] for l in data]


raw = split_lines("inputs/day12.txt")
parsed = list_map(raw, parse)
part1 = sum(bfs(line, nums) for line, nums in parsed)
print(part1)

new_parsed = reparse(parsed)
part2 = sum(bfs(line, nums) for line, nums in new_parsed)
print(part2)
