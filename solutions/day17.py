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
    prev = defaultdict(lambda: None)
    queue = [
        State(start + 1, 1, max_straight -1, graph[start +1]),
        State(
            start + 1j,
            1j,
            max_straight -1,
            graph[start +1j],
        ),
    ]
    heapq.heapify(queue)
    # Tip from Discord
    answer = 9 * (xmax + ymax)

    def verify_coord(coord):
        return xmin <= coord.real <= xmax and ymin <= coord.imag <= ymax

    def add_neighbor(new_coord, direction, this_traversed, new_remaining):
        heapq.heappush(
            queue,
            State(
                new_coord,
                direction,
                new_remaining,
                this_traversed + graph[new_coord],
            ),
        )

    visited = set()
    directions = ((-1, 1), (-1j, 1j))
    while True:
        try:
            current = heapq.heappop(queue)
        except IndexError:
            break
        assert verify_coord(current.coord)
        coord = current.coord
        this_traversed = current.traversed
        current_hash = hash(current)

        if (
            this_traversed
            >= dist[(coord, current.direction, current.remaining)]
        ):
            continue
        dist[(coord, current.direction, current.remaining)] = this_traversed
        if this_traversed >= answer:
            continue
        # assert current_hash not in hashes
        # if (current.coord, current.direction, current.remaining) in visited:
        #     breakpoint()

        visited.add((coord, current.direction, current.remaining))
        direction = current.direction
        new_remaining = current.remaining - 1
        #breakpoint()

        if coord == goal and new_remaining <= move_threshold:
            answer = this_traversed
            continue
        # Going left/right
        
        #print(current)
        if new_remaining <= move_threshold:
            for dir in directions[bool(direction.real)]:
                new_coord = coord + dir
                if verify_coord(new_coord):
                    add_neighbor(new_coord, dir, this_traversed, max_straight)
                    prev[(new_coord, dir, max_straight)] = (coord, current.direction, current.remaining)
        new_coord = current.coord + current.direction
        if new_remaining > 0 and verify_coord(new_coord):
            add_neighbor(new_coord, current.direction, this_traversed, new_remaining)
            prev[(new_coord, current.direction, new_remaining)] = (coord, current.direction, new_remaining + 1)

    current = goal
    S = []
    while prev[current] or current == start:
        S.append(current)
        current = prev[current]
        print(current)
    print(list(reversed(S)))
    return answer


raw_input = split_lines("inputs/day17.txt")
graph = parse(raw_input)
part1 = A_star(graph, 0, 3, 0)
print(part1)

part2 = A_star(parse(raw_input), 0, 10, 4)
print(part2)
# 1386 too low
# 1479 too high

from heapq import heappop, heappush as push

G = {
    i + j * 1j: int(c)
    for i, r in enumerate(open("inputs/day17.txt"))
    for j, c in enumerate(r.strip())
}


def f(min, max, end=140+140j, x=0):
    todo = [(0, 0, 0, 1), (0, 0, 0, 1j)]
    seen = set()

    while todo:
        val, _, pos, dir = heappop(todo)

        if pos == end:
            return val
        if (pos, dir) in seen:
            continue
        seen.add((pos, dir))

        for d in 1j / dir, -1j / dir:
            for i in range(min, max + 1):
                if pos + d * i in G:
                    v = sum(G[pos + d * j] for j in range(1, i + 1))
                    push(todo, (val + v, (x := x + 1), pos + d * i, d))


print(f(1, 3), f(4, 10))
