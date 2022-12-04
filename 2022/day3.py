# for i in range(26):
#     print(chr(i + 65))

with open("day3.txt") as f:
    sum = 0
    for line in f:
        line = line.strip()
        bag1 = line[: int(len(line) / 2)]
        bag2 = line[int(len(line) / 2) :]

        found_item = None
        for item in bag1:
            if item in bag2:
                found_item = item
                break

        def score(c: chr) -> int:
            return ord(c) - 96 if str.islower(c) else ord(c) - 64 + 26

        sum += score(found_item)

    print(sum)

with open("day3.txt") as f:
    sum = 0

    def score(c: chr) -> int:
        return ord(c) - 96 if str.islower(c) else ord(c) - 64 + 26

    group_lines = []
    for line in f:
        if len(group_lines) < 3:
            group_lines.append(line.strip())
            if len(group_lines) != 3:
                continue

            for item in group_lines[0]:
                if item in group_lines[1] and item in group_lines[2]:
                    print(item)
                    sum += score(item)
                    break

            group_lines.clear()

    print(sum)
