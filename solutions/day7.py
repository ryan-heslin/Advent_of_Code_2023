from collections import Counter

from utils.utils import list_map
from utils.utils import split_lines


class Hand:
    joker = "J"
    ranks = {
        (5,): 7,
        (4, 1): 6,
        (3, 2): 5,
        (3, 1, 1): 4,
        (2, 2, 1): 3,
        (2, 1, 1, 1): 2,
        (1, 1, 1, 1, 1): 1,
    }
    n_cards = 5

    def __init__(self, cards, suits, joker=False):
        # if joker:
        #     breakpoint()
        self.cards = tuple(suits[c] for c in cards)
        self._count = Counter(cards)
        self.rank = self.ranks[tuple(sorted(self._count.values(), reverse=True))]
        if joker and (jokers := self._count[self.joker]) > 0:
            ranks = {
                (5,): 7,
                (4, 1): 6,
                (3, 2): 5,
                (3, 1, 1): 4,
                (2, 2, 1): 3,
                (2, 1, 1, 1): 2,
                (1, 1, 1, 1, 1): 1,
            }
            match (self.rank, jokers):
                case (1, 1):
                    self.rank = 2
                case (2, 1) | (2, 2):
                    self.rank = 4
                # two pair
                case (3, 1):
                    self.rank = 5
                case (3, 2):
                    self.rank = 6
                # should be impossible
                case (3, 3):
                    print("check")
                    self.rank = 7
                # 3 of a kind
                case (4, 1) | (4, 3):
                    self.rank = 6
                # 4 of a kind, full house
                case (5, _) | (6, _):
                    self.rank = 7
                case _:
                    pass

    def __lt__(self, other):
        attr = "rank" if self.rank != other.rank else "cards"
        return getattr(self, attr) < getattr(other, attr)

    def __repr__(self) -> str:
        return str(self.cards)

    # Jokers act as weakest for hand comparison, strongest for hand type


def solve(hands, points):
    order = sorted(range(len(hands)), key=lambda i: hands[i])
    return sum(points[index] * (i + 1) for i, index in enumerate(order))


raw = split_lines("inputs/day7.txt")
suits = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
mapping = dict(zip(suits, range(len(suits))))
lines, points = zip(*(line.split(" ") for line in raw))
hands = [Hand(line, mapping, False) for line in lines]
points = list_map(points, int)
part1 = solve(hands, points)
print(part1)

suits.remove("J")
suits.insert(0, "J")
new_mapping = dict(zip(suits, range(len(suits))))
joker_hands = [Hand(line, new_mapping, True) for line in lines]
part2 = solve(joker_hands, points)
print(part2)
