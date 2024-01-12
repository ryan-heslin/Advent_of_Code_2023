# For each brick, determine if:
# 1. Any bricks above rest on it
# Those bricks rest on no other brick
import typing
from collections import namedtuple
from itertools import chain

from utils.utils import split_lines

# TODO
# Make named tuple subclass to rely on namedtuple's hash
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


class Brick:
    def __init__(self, coords):
        # Is brick horizontal or vertical?
        self.coords = coords

    def __repr__(self):
        return self.coords.__repr__()

        # def below(self):
        #     """All in all, you're just another part of the brick pile"""
        #     if self.first.z == 0:
        #         raise ValueError
        #     if self.axis == 2:
        #         yield first.lower()
        #     start = first.lower()
        #     for i in range(self.first[self.axis], self.second[self.axis] + 1):
        #         yield start.update(self.axis, i + start)

    def __in__(self, coord):
        return coord in self.coords

    # def lower(self, container):
    #     if self.first.z <= 1:
    #         raise ValueError
    #     return __class__(
    #         self.first.update(2, self.first.z - 1),
    #         self.second.update(2, self.second.z - 1),
    #         container
    #     )
    #
    # # def update(self):
    #     self.container.update(self.coords)
    #
    # def discard(self):
    #     self.container.discard(self.coords)
    #


def parse(line):
    parts = line.split("~")
    return Coord(map(int, parts[0].split(","))), Coord(map(int, parts[1].split(",")))


def fall(bricks, contained):
    undone = set(bricks.keys())
    fallen = True
    #breakpoint()
    # Just move all in ascending z order
    this_bricks = list(bricks.items())
    while fallen:
        this_bricks = sorted(this_bricks, key = lambda x: x[1][1::-1])
        fallen = False

        for i in range(len(this_bricks)):
            # Track coordinate changes and bricks done moving
            # if id not in undone:
            #     new_bricks[id] = brick
            #     continue
            index, brick = this_bricks[i]
            new_coords = set()
            for c in brick:
                new = c - 1
                # Can't fall any further
                if (new in contained and new not in brick) or new[2] < 1:
                    print(brick)
                    print(bricks, "\n\n")
                    # undone.remove(id)
                    break
                new_coords.add(new)
            else:
                fallen = True
                this_bricks[index][1] = new_coords
                contained -= brick
                contained |= new_coords

    return dict(bricks)


def count_not_supporting(bricks):
    # How many bricks don't support any others?
    # How many bricks aren't the only brick keeping at least one brick from falling
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
            new = coord.update(2, coord[2] - 1)
            supporting = mapping.get(new)
            if supporting is not None and supporting != id:
                below.add(supporting)
        if len(below) == 1:
            alone.update(below)
    return len(alone)


raw_input = split_lines("inputs/day22.txt")
parsed = list(map(parse, raw_input))
contained = set()
bricks = {i: coord_range(*line) for i, line in enumerate(parsed)}
for brick in bricks.values():
    contained |= brick
# breakpoint()
print(bricks)
bricks = fall(bricks, contained)
part1 = count_not_supporting(bricks)
print(part1)

# Expected
# A    (1, 0, 1)    (1, 2, 1)
# C    (0, 2, 2)    (2, 2, 2)
# B    (0, 0, 2)    (2, 0, 2)
# E    (2, 0, 3)    (2, 2, 3)
# D    (0, 0, 3)    (0, 2, 3)
# F    (0, 1, 4)    (2, 1, 4)
# G    (1, 1, 5)    (1, 1, 6)
