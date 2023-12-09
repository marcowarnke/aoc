from collections import defaultdict
from math import prod

def chk(symbol: str):
    return not symbol.isdigit() and not symbol == "."


with open("input", "r") as f:
    lines = [x.strip() for x in f.readlines()]

    G = []
    for line in lines:
        indices = []
        i = 0
        while i < len(line):
            if line[i].isnumeric():
                start = i
                while i < len(line) and line[i].isnumeric():
                    i += 1
                end = i - 1
                indices.append((start, end))
            i += 1
        G.append(indices)

    my = len(lines)
    mx = len(lines[0])
    offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    p1l = []
    d = defaultdict(set)
    for y, li in enumerate(G):
        for index in li:
            start = index[0]
            end = index[1]
            is_part = False

            for x in range(start, end + 1):
                for offset in offsets:
                    yo = y + offset[1]
                    xo = x + offset[0]
                    if 0<=yo<my and 0<=xo<mx:
                        scan = lines[yo][xo]
                        if chk(scan):
                            is_part = True
                            if scan == "*":
                                d[(xo, yo)].add(lines[y][start:end+1])

            if is_part:
                p1l.append(int("".join([lines[y][x] for x in range(start, end + 1)])))
    
    p2 = []
    for gear in d.values():
        if len(gear) == 2:
            gs = prod([int(x) for x in gear])
            p2.append(gs)

    print(sum(p1l))
    print(p2)
    print(sum(p2))
