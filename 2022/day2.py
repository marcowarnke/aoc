# Your total score is the sum of your scores for each round.
# The score for a single round is the score for the shape you selected
# (1 for Rock, 2 for Paper, and 3 for Scissors) plus the score for the outcome of the round
# (0 if you lost, 3 if the round was a draw, and 6 if you won).

scores = {
    "A X": 1 + 3,
    "A Y": 2 + 6,
    "A Z": 3 + 0,
    "B X": 1 + 0,
    "B Y": 2 + 3,
    "B Z": 3 + 6,
    "C X": 1 + 6,
    "C Y": 2 + 0,
    "C Z": 3 + 3,
}

with open("day2.txt") as f:
    total = 0
    for line in f:
        line = line.rstrip()
        total += scores[line]

    print(total)

# X means you need to lose, Y means you need to end the round in a draw, and Z means you need to win. Good luck!
with open("day2.txt") as f:
    total = 0
    for line in f:
        [c1, c2] = line.split()

        mv = ""
        if c2 == "X":
            if c1 == "A":
                mv = "Z"
            elif c1 == "B":
                mv = "X"
            elif c1 == "C":
                mv = "Y"
        elif c2 == "Y":
            if c1 == "A":
                mv = "X"
            elif c1 == "B":
                mv = "Y"
            elif c1 == "C":
                mv = "Z"
        elif c2 == "Z":
            if c1 == "A":
                mv = "Y"
            elif c1 == "B":
                mv = "Z"
            elif c1 == "C":
                mv = "X"

        move = c1 + " " + mv
        print(move)

        total += scores[move]

    print(total)
