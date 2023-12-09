res = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
    "zero": "0"
}

with open("input1", "r") as f:
    ns = []
    for line in f:
        nl = []
        for i, char in enumerate(line):
            if char.isalpha() and line[i:i+3] in res:
                nl.append(res[line[i:i+3]])
            elif char.isalpha() and line[i:i+4] in res:
                nl.append(res[line[i:i+4]])
            elif char.isalpha() and line[i:i+5] in res:
                nl.append(res[line[i:i+5]])
            elif char.isnumeric():
                nl.append(char)
        ns.append(int(nl[0] + nl[-1]))
    print(sum(ns))
