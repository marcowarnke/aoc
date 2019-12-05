def get_digit(number, n):
    return number // 10**n % 10


def get_opcode_from_instruction(instruction_code):
    return instruction_code % 100


def get_immediate_mode_flags(instruction_code):
    return {"C": get_digit(instruction_code, 2), "B": get_digit(instruction_code, 3), "A": get_digit(instruction_code, 4)}


def execute_operation(pc, program):
    instruction_code = program[pc]
    opcode = get_opcode_from_instruction(instruction_code)
    immediate_mode_flags = get_immediate_mode_flags(instruction_code)
    if opcode == 1:
        program[program[pc + 3]] = (program[pc + 1] if immediate_mode_flags["C"] == 1 else program[program[pc + 1]
                                                                                                   ]) + (program[pc + 2] if immediate_mode_flags["B"] == 1 else program[program[pc + 2]])
        pc += 4
    elif opcode == 2:
        program[program[pc + 3]] = (program[pc + 1] if immediate_mode_flags["C"] == 1 else program[program[pc + 1]
                                                                                                   ]) * (program[pc + 2] if immediate_mode_flags["B"] == 1 else program[program[pc + 2]])
        pc += 4
    elif opcode == 3:
        input_number = int(input("input integer: "))
        program[program[pc + 1]] = input_number
        pc += 2
    elif opcode == 4:
        if immediate_mode_flags["C"] == 1:
            print(f"output: {program[pc + 1]}")
        else:
            print(f"output: {program[program[pc + 1]]}")
        pc += 2
    elif opcode == 5:
        if program[pc + 1] != 0 and immediate_mode_flags["C"] == 1:
            if immediate_mode_flags["B"] == 1:
                pc = program[pc + 2]
            else:
                pc = program[program[pc + 2]]
        elif program[program[pc + 1]] != 0 and immediate_mode_flags["C"] == 0:
            if immediate_mode_flags["B"] == 1:
                pc = program[pc + 2]
            else:
                pc = program[program[pc + 2]]
        else:
            pc += 3
    elif opcode == 6:
        if program[pc + 1] == 0 and immediate_mode_flags["C"] == 1:
            if immediate_mode_flags["B"] == 1:
                pc = program[pc + 2]
            else:
                pc = program[program[pc + 2]]
        elif program[program[pc + 1]] == 0 and immediate_mode_flags["C"] == 0:
            if immediate_mode_flags["B"] == 1:
                pc = program[pc + 2]
            else:
                pc = program[program[pc + 2]]
        else:
            pc += 3
    elif opcode == 7:
        if (program[pc + 1] if immediate_mode_flags["C"] == 1 else program[program[pc + 1]]) < (program[pc + 2] if immediate_mode_flags["B"] == 1 else program[program[pc + 2]]):
            program[(pc + 3 if immediate_mode_flags["A"]
                     == 1 else program[pc + 3])] = 1
        else:
            program[(pc + 3 if immediate_mode_flags["A"]
                     == 1 else program[pc + 3])] = 0
        pc += 4
    elif opcode == 8:
        if (program[pc + 1] if immediate_mode_flags["C"] == 1 else program[program[pc + 1]]) == (program[pc + 2] if immediate_mode_flags["B"] == 1 else program[program[pc + 2]]):
            program[(pc + 3 if immediate_mode_flags["A"]
                     == 1 else program[pc + 3])] = 1
        else:
            program[(pc + 3 if immediate_mode_flags["A"]
                     == 1 else program[pc + 3])] = 0
        pc += 4
    elif opcode == 99:
        print("found halt instruction...")
    else:
        print(f"unknown opcode: {opcode}")
        exit(1)
    return (opcode, pc)


def run(pc, program):
    opcode = 0
    while opcode != 99:
        (opcode, pc) = execute_operation(pc, program)


def main():
    with open("d:/aoc/day05/input.txt", "r") as f:
        content = f.readlines()

    program = [int(x) for x in content[0].split(",")]
    run(0, program)


if __name__ == "__main__":
    main()
