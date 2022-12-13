with open("day5.txt") as f:
    num_stacks = 0
    for line in f:
        if len(line) > 1 and line[1].isnumeric():
            last_el = line.find("\n")
            num_stacks = int(line[last_el - 2 : last_el - 1])

    f.seek(0)

    crate_offset = 4
    stacks = {}
    for line in f:
        if line == "\n":
            break
        for i in range(num_stacks):
            crate = line[1 + i * crate_offset]
            if crate == " " or crate.isnumeric():
                continue
            if stacks.get(i + 1) is not None:
                stacks[i + 1].insert(0, crate)
            else:
                stacks[i + 1] = [crate]

    for line in f:
        moves = line.split(" ")
        num_pops = int(moves[1])
        from_stack = int(moves[3])
        to_stack = int(moves[5])

        crates = stacks[from_stack][-num_pops:]
        stacks[from_stack] = stacks[from_stack][:-num_pops]
        print(crates)
        for crate in crates:
            stacks[to_stack].append(crate)

    keys = []
    for key in stacks.keys():
        keys.append(key)

    top_crates = []
    for key in sorted(keys):
        top_crates.append(stacks[key][-1])

    print("".join(top_crates))
