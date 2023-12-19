import re
from functools import cache
from itertools import combinations

from utils.utils import list_map
from utils.utils import split_lines


def parse(line):
    parts = line.split(" ")
    return parts[0], list(map(int, parts[1].split(",")))


memo_combinations = cache(combinations)


def brute_force(line, nums):
    #total = sum(nums)
    end = len(nums) - 1
    pattern = re.compile(
        r"^\.*#"
        + "#".join(
            "{" + str(num) + r"}\." + ("+" if i < end else "*")
            for i, num in enumerate(nums)
        ) + "$"
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
                copy[i] = ("#" if i in combo else ".")
            # print("".join(copy))
            # print(bool(re.match(pattern, "".join(copy))))
            found += bool(re.match(pattern, "".join(copy)))
    return found

class Node():

    def __init__(self, char_index, group_index, cur_group_size):
        self.char_index = char_index
        self.group_index = group_index
        self.cur_group_size = cur_group_size

    def __hash__(self):
        return hash((self.char_index, self.group_index, self.cur_group_size))

    def __lt__(self, other):
        return (self.char_index, self.group_index, self.cur_group_size) < (other.char_index, other.group_index, other.cur_group_size)
def bfs(string, groups):
    #char_index,  group_index, cur_group_size, count
    stop = len(string) - 1
    queue = deque([])
    total = 0
    # Dict of states to add to count?
    while queue:
        current = queue.pop()
        if char_index == stop:
            total += current.count
        if char == "#":
            # If characters left in current group, add to it
            if cur_group_size is not None:
                cur_group_size += 1
        elif char == "."
            # If current group not finished , bail
            group_index += 1
        # ?
        else:
            # If not in group, try starting
            # If in group, determined by whether group finished
            group_size = group

            

# Match char by char, consuming group lengths
# If multiple matches for certain number of groups by certain character, record number
# Multiply by recursive call to remaining string

raw = split_lines("inputs/day12.txt")
parsed = list_map(raw, parse)
part1 = sum(brute_force(line, nums) for line, nums in parsed)
print(part1)
