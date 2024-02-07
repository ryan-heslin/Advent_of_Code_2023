from dataclasses import dataclass

import utils.utils as ut


@dataclass
class Line:
    def __init__(self, dest, source, rnge):
        # Only need source range, going forward
        self.lower = source
        self.upper = source + rnge - 1
        self.rnge = rnge
        self.constant = dest - source

    def __repr__(self):
        return f"(Lower: {self.lower}, Upper : {self.upper}, Range: {self.rnge}, Constant : {self.constant})"

    def __lt__(self, other):
        return (self.lower < other.lower) or (
            self.lower == other.lower and self.upper < other.upper
        )


class Mappings:
    def __init__(self, data, seeds, reverse = False):
        self.intervals = []
        self.seeds = seeds
        for group in data:
            result = self.parse_interval(group, reverse = reverse)
            self.intervals.append(result)

    def __repr__(self):
        return "\n".join(map(str, self.intervals))

    @staticmethod
    def parse_interval(lines, reverse = False):
        result = []
        for data in lines[1:]:
            if reverse:
                data[0], data[1] = data[1], data[0]
            this = Line(*data)
            result.append(this)
        # Sort by interval start
        result.sort()
        return result

    @staticmethod
    def parse_lines(groups):
        for i in range(len(groups)):
            groups[i] = groups[i].splitlines()[1:]
            groups[i] = [list(ut.scan_ints(line)) for line in groups[i]]
        return groups



    def verify_seed(self, seed):
        valid = {seed}
        for stage in self.intervals:
            #breakpoint()
            if not valid:
                break
            # Map unusued numbers to themselves
            new = set()
            # Assume unique intervals
            for interval in stage:
                for  number in valid:
                    if interval.lower <= number <= interval.upper:
                        valid.remove(number)
                        new.add(
                                number + interval.constant
                                )
                        break
            valid.update(new)

        return valid

    
def solve_part2(data, seeds):
    current = 0
    mappings = Mappings(data, [], True)
    zipped = list(zip(*seeds))
    lower = min(zipped[0])
    upper = max(zipped[1])

    while True:
        result = mappings.verify_seed(current)
        for number in result:
            if not (lower <= number <= upper):
                continue
            for rnge in seeds:
                if rnge[0] <= number <= rnge[1]:
                    return current
        current += 1

def interval_finder(intervals):
    midpoint = len(intervals) // 2
    def result(x):
        i = midpoint

        while True:
            lower = x <= intervals[i][1]
            upper = x>= intervals[i][0]

            if lower and upper:
                return True
            if lower:
                pass
# def combine_intervals(intervals: list[tuple[int, int]]):
#     for left, right in combinations(intervals, r=2):
#         if left[0] > right[0]:
#             left, right = right, left
#         if left[1] == right[1]:
#             pass
#
#
raw = ut.split_groups("inputs/day5.txt")
seeds = raw.pop(0)
targets = tuple(ut.scan_ints(seeds.lstrip("seeds: ")))
processed =  Mappings.parse_lines(raw)
mappings = Mappings(processed, targets)
part1 = min(min(mappings.verify_seed(s)) for s in mappings.seeds)
print(part1)
raw.reverse()

pairs = []
for i in range(1, len(targets), 2):
    pairs.append((targets[i-1], targets[i-1] + targets[i] - 1))
pairs.sort()
part2 = solve_part2(raw, pairs)
print(part2)
