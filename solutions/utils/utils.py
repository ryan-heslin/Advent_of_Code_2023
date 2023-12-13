from functools import cache
from itertools import product
import re

def split_lines(path):
    with open(path) as f:
        return [line.strip() for line in f]

def split_groups(path):
    with open(path) as f:
        return f.read().split("\n\n") 

def list_map(iter, func):
    return list(map(func, iter))


def neighbors(xmin, xmax, ymin, ymax, diag =  False, combos = None):
    """Cartesian neighbors"""
    if combos is None:
        combos = product(range(-1, 2), range(-1, 2))
    # Each combination of 1-step movements
    shifts = {complex(x, y) for x, y in combos if (x != 0 or y != 0) and (diag or (x== 0 or y == 0))}
    print(shifts)

    @cache
    def result(coord):
        out = set()
        for shift in shifts:
            new = shift + coord
            if (xmin <= new.real <= xmax) and (ymin <= new.imag <= ymax):
                out.add(new)

        return frozenset(out)
    
    return result

def scan_ints(line):
    return map(int, re.split(r"\s+", line))

def sort_complex(z):
    return (z.real, z.imag)
