from functools import reduce
from operator import itemgetter
from itertools import chain

from utils.utils import split_lines

class Coord(tuple):
    def update(self, key, value):
        return __class__(chain(self[:key], (value,), self[key + 1 :]))

    def __sub__(self, value):
        return __class__(self[:2] + (self[2] - value,))

    def __isub__(self, value):
        return self - value


def coord_range(start, end):
    start, second = sorted([start, end])
    if start == second:
        return {start}
    for field in range(len(start)):
        if start[field] != end[field]:
            axis = field
            break
    else:
        raise ValueError
    # Singleton cube

    offset = start[axis]
    assert start[axis] <= end[axis]
    return {start.update(axis, val) for val in range(offset, end[axis] + 1)}

def get_bricks(bricks):
    return reduce( set.union, bricks)


def parse(line):
    parts = line.split("~")
    return Coord(map(int, parts[0].split(","))), Coord(map(int, parts[1].split(",")))

def lowest_z(coords):
    return min(coords, key = itemgetter(-1))[-1]


def fall(bricks, contained):
    result = {}

    bricks = list(sorted(bricks.items(), key = lambda x: lowest_z(x[1])))
    # Make each brick fall in ascending order
    fallen = 0

    for pair in bricks:
        id, brick = pair
        current= set(brick)
        contained -= current
        z_level = lowest_z(brick)
        done = started = False

        while z_level > 1 and not done:
            new = set()
            for coord in current:
                new_coord = coord - 1
                if new_coord in contained:
                    done = True
                    break
                new.add(new_coord)
            else:
                started = True
                z_level -= 1
                current = new

        fallen += started
        result[id] = current
        contained |= current
    return result, fallen

def count_not_supporting(bricks):
    mapping = {}
    alone = set()
    for id, brick in bricks.items():
        for coord in brick:
            mapping[coord] = id
    for id, brick in bricks.items():
        below = set()
        for coord in brick:
            if coord[2] == 1:
                break
            new = coord - 1
            supporting = mapping.get(new)
            if supporting is not None and supporting != id:
                below.add(supporting)
        if len(below) == 1:
            alone.update(below)
    return len(bricks) - len(alone)


raw_input = split_lines("inputs/day22.txt")
parsed = list(map(parse, raw_input))
contained = set()
bricks = {i: coord_range(*line) for i, line in enumerate(parsed)}
contained = get_bricks(bricks.values())
bricks, _ = fall(bricks, contained)
part1 = count_not_supporting(bricks)
print(part1)

part2 = 0
contained = get_bricks(bricks.values())

for id in list(bricks.keys()):
    removed = bricks[id]
    bricks.pop(id)
    part2 += fall(bricks, contained - removed)[1]
    bricks[id] = removed
print(part2)
