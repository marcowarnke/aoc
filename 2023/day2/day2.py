from typing import List

with open("input", "r") as f:
    sg = []
    powers = []
    for line in f:
        gameinfo, sets = line.split(":")
        _, gn = gameinfo.split(" ")
        gn = int(gn)
        sets: List[str] = sets.split(";")
        sets[:] = map(lambda g: g.strip(), sets)

        lr = 12
        lg = 13
        lb = 14
        fg = False
        mr = 0
        mg = 0
        mb = 0
        for set in sets:
            nc = set.split(",")
            nc = [x.strip() for x in nc]
            for ncc in nc:
                num, color = ncc.split(" ")
                num = int(num)
                if color == "red":
                    mr = num if num > mr else mr
                elif color == "green":
                    mg = num if num > mg else mg
                elif color == "blue":
                    mb = num if num > mb else mb
                if color == "red" and num > lr:
                    mr = num if num > mr else mr
                    fg = True
                elif color == "green" and num > lg:
                    mg = num if num > mg else mg
                    fg = True
                elif color == "blue" and num > lb:
                    mb = num if num > mb else mb
                    fg = True
        
        if not fg:
            sg.append(gn)
        power = mr * mg * mb
        print(f"{mr} * {mg} * {mb} = {power}")
        powers.append(power)
        
    print(sum(sg))
    print(sum(powers))
