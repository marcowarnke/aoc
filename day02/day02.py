def deref(program, index):
    return program[index]


def execute_operation(pc, program):
    opcode = program[pc]
    if opcode == 1:
        program[deref(program, pc + 3)] = program[deref(program,
                                                        pc + 1)] + program[deref(program, pc + 2)]
    if opcode == 2:
        program[deref(program, pc + 3)] = program[deref(program,
                                                        pc + 1)] * program[deref(program, pc + 2)]
    pc += 4
    return (opcode, pc)


def run(pc, program):
    opcode = 0
    while opcode != 99:
        (opcode, pc) = execute_operation(pc, program)


def find_noun_and_verb(program):
    for noun in range(100):
        for verb in range(100):
            code = program.copy()
            code[1] = noun
            code[2] = verb
            run(0, code)
            if code[0] == 19690720:
                print(f"noun: {noun}, verb: {verb}")
                print(100 * noun + verb)


def main():
    with open("d:/aoc/day02/input.txt", "r") as f:
        content = f.readlines()

    program = [int(x) for x in content[0].split(",")]
    find_noun_and_verb(program)


if __name__ == "__main__":
    main()
