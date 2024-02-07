import re

from utils.utils import split_lines

raw = split_lines("inputs/day1.txt")
# No zeroes
naturals = r"[1-9]"
stripped = [re.sub("[a-z]+", "", line) for line in raw]
part1 = sum(int(line[0] + line[-1]) for line in stripped)
print(part1)

nums = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
n = len(nums)
nums.append(naturals)
parts = "|".join(nums)
pattern = f"(?=({parts}))"
chars = list(map(str, range(1, 1 + n)))
keys = dict(zip(nums, chars))

matches = [re.findall(pattern, line) for line in raw]
part2 = sum(
    int(keys.get(r[0], r[0]) + keys.get(r[-1], r[-1])) if r else 0 for r in matches
)
print(part2)
