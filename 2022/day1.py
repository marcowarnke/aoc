with open("day1.txt") as f:
    sums = []

    cals = 0
    for line in f:
        line = str.join("", [c for c in line if c.isalnum()])
        if line == "":
            sums.append(cals)
            cals = 0
        else:
            cals += int(line)

    top3 = sorted(sums, reverse=True)[:3]
    print(sum(top3))
