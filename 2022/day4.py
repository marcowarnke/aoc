with open("day4.txt") as f:
    num_contains = 0
    for line in f:
        [elf1, elf2] = line.strip().split(",")

        (elf1_lower, elf1_upper) = elf1.split("-")
        (elf2_lower, elf2_upper) = elf2.split("-")

        elf1_lower = int(elf1_lower)
        elf1_upper = int(elf1_upper)
        elf2_lower = int(elf2_lower)
        elf2_upper = int(elf2_upper)

        # 1 contained in 2
        if elf2_lower <= elf1_lower and elf2_upper >= elf1_upper:
            num_contains += 1
            print(f"one in two: {line}")
        # 2 contained in 1
        elif elf1_lower <= elf2_lower and elf1_upper >= elf2_upper:
            num_contains += 1
            print(f"two in one: {line}")

    print(num_contains)

with open("day4.txt") as f:
    num_contains = 0
    for line in f:
        [elf1, elf2] = line.strip().split(",")

        (elf1_lower, elf1_upper) = elf1.split("-")
        (elf2_lower, elf2_upper) = elf2.split("-")

        elf1_lower = int(elf1_lower)
        elf1_upper = int(elf1_upper)
        elf2_lower = int(elf2_lower)
        elf2_upper = int(elf2_upper)

        elf1_set = set([x for x in range(elf1_lower, elf1_upper + 1)])
        elf2_set = set([x for x in range(elf2_lower, elf2_upper + 1)])

        intersection = elf1_set.intersection(elf2_set)

        if len(intersection) > 0:
            num_contains += 1

    print(num_contains)
