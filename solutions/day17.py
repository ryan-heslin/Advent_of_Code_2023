import heapq
from collections import defaultdict
from functools import cache
from math import inf
from operator import attrgetter

from utils.utils import split_lines


class State:
    def __init__(self, coord, direction, remaining, traversed):
        self.coord = coord
        self.direction = direction
        self.remaining = remaining
        self.traversed = traversed

    def __lt__(self, other):
        return self.traversed < other.traversed

    def __hash__(self):
        return hash((self.coord, self.direction, self.remaining))

    def __repr__(self) -> str:
        return (self.coord, self.direction, self.remaining, self.traversed).__repr__()


def parse(lines):
    return {
        complex(i, j): int(char)
        for j, line in enumerate(lines)
        for i, char in enumerate(line)
    }


@cache
def manhattan(x, y):
    return abs(x.real - y.real) + abs(x.imag - y.imag)


def A_star(graph, start, max_straight, min_turn_time):
    xmin = ymin = 0
    move_threshold = max_straight - min_turn_time
    xmax = int(max(graph.keys(), key=attrgetter("real")).real)
    ymax = int(max(graph.keys(), key=attrgetter("imag")).imag)
    # goal = complex(xmax, ymax)
    goal = complex(xmax, ymax)

    dist = defaultdict(lambda: inf)
    queue = [
        State(start, 1, max_straight, 0),
        State(
            start,
            1j,
            max_straight,
            0,
        ),
    ]
    heapq.heapify(queue)
    # Tip from Discord
    answer = max(graph.values()) * (xmax + ymax)

    def verify_coord(coord):
        return xmin <= coord.real <= xmax and ymin <= coord.imag <= ymax

    def add_neighbor(new_coord, direction, this_traversed, new_remaining):
        heapq.heappush(
            queue,
            State(
                new_coord,
                direction,
                new_remaining,
                this_traversed ,
            ),
        )

    directions = ((-1, 1), (-1j, 1j))
    while True:
        try:
            current = heapq.heappop(queue)
        except IndexError:
            break
        
        new_coord = current.coord + current.direction
        if not verify_coord(new_coord):
            continue
        this_traversed = current.traversed + graph[new_coord]
        new_remaining = current.remaining - 1
        #current_hash = hash(current)
        key = (new_coord, current.direction, new_remaining)

        if not (
            new_remaining > -1
            and this_traversed < dist[key]
            and this_traversed < answer
        ):
            continue
        dist[key] = this_traversed

        if new_coord == goal and new_remaining <= move_threshold:
            answer = this_traversed
            continue
        # Going left/right

        # print(current)
        if new_remaining <= move_threshold:
            for dir in directions[bool(current.direction.real)]:
                add_neighbor(new_coord, dir, this_traversed, max_straight)
        add_neighbor(new_coord, current.direction, this_traversed, new_remaining)

    return answer


raw_input = split_lines("inputs/day17.txt")
graph = parse(raw_input)
part1 = A_star(graph, 0, 3, 0)
print(part1)

part2 = A_star(parse(raw_input), 0, 10, 4)
print(part2)
