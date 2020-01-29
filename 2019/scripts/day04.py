from collections import Counter


def has_six_digits(number):
    return len(str(number)) == 6


def has_adjacent_double(number):
    nstr = str(number)
    result = dict(
        Counter(s1 + s2 for s1, s2 in zip(nstr, nstr[1:]) if s1 == s2))
    return 1 in result.values()


def never_decreases(number):
    nstr = str(number)
    for i in range(len(nstr) - 1):
        if int(nstr[i]) > int(nstr[i + 1]):
            return False
    return True


def is_valid_pw(number):
    return has_six_digits(number) and has_adjacent_double(number) and never_decreases(number)


def main():
    min_pw = 240920
    max_pw = 789857
    possible_pws = []
    for i in range(min_pw, max_pw):
        if is_valid_pw(i):
            possible_pws.append(i)
    print(len(possible_pws))


if __name__ == "__main__":
    main()
