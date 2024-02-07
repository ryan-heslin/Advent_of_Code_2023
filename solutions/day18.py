import utils.utils as ut


def parse(lines, part1 = True):
    result = []
    directions = ("R", "D", "L", "U")
    for line in lines:
        dir, num, hex = line.split(" ")
        hex =  hex[1:-1:1]
        if part1:
            num = int(num)
        else:
            num = int(hex[1:6], 16)
            dir = directions[int(hex[-1])]
        result.append([dir, num])
    return result


def get_vertices(lines):
    vertices = [0]
    length = 1
    current = vertices[-1]
    mapping = {"U": -1j, "R": 1, "D": 1j, "L": -1}
    for line in lines[:-1]:
        new = current + mapping[line[0]] * line[1]
        vertices.append(new)
        length += ut.manhattan(current, new) 
        current = new
    return vertices, length + ut.manhattan(current, vertices[0])


def shoelace(vertices):
    return 0.5 * sum(
        (left.real * right.imag) - (left.imag * right.real)
        for left, right in zip(vertices, vertices[1:] + [vertices[0]])
    )
    

# Pick's theorem
def pick(interior, border):
    return interior + border // 2 + 1

def area(border, vertices):
    return int(pick(shoelace(vertices), border))

raw_input = ut.split_lines("inputs/day18.txt")
data = parse(raw_input)
vertices, border = get_vertices(data)
part1 = area(border, vertices)
data = parse(raw_input, False)
print(part1)

vertices, border = get_vertices(data)
part2 = area(border, vertices)
print(part2)
