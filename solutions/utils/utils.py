def split_lines(path):
    with open(path) as f:
        return [line.strip() for line in f]

def list_map(iter, func):
    return list(map(func, iter))
