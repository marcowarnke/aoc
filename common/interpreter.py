"""
Provides classes for interpreting intcode programs.
"""
from typing import List
import queue

QUEUE_TIMEOUT = 3


class Instruction:
    """
    A class for intcode instructions,
    every instruction represents an executable step in an intcode program.
    """

    def __init__(self, program, raw, start, end, opcode, params, num_of_params):
        self.opcode = opcode
        self.num_of_params = num_of_params
        self.params = params
        self.raw_intcode = raw
        # pointers into the program array
        self.start_pos = start
        self.end_pos = end
        self.program = program
        self.OPCODE_FUNCTION_MAP = {
            1: self.add,
            2: self.mul,
            3: self.read,
            4: self.write,
            5: self.jmp_nzero,
            6: self.jmp_zero,
            7: self.lt,
            8: self.eq
        }

    def __str__(self):
        return f"[opcode: {self.opcode}, num_of_params: {self.num_of_params}, params: {str(self.params)}, raw_intcode: {self.raw_intcode}]"

    def execute(self, pc, in_queue, out_queue) -> bool:
        """ Executes the instruction.
            Has following sideeffects:
                updates the pc depending on the length of the executed instruction,
                updates values in the source program.
        """

        if self.opcode in self.OPCODE_FUNCTION_MAP.keys():
            func = self.OPCODE_FUNCTION_MAP[self.opcode]
            if func == self.write:
                return func(pc, out_queue)
            elif func == self.read:
                return func(pc, in_queue)
            return func(pc)
        else:
            raise LookupError(
                f"Could not run interpreter function for instruction: {self}")

    def add(self, pc):
        # add p1, p2, s1
        self.params[2].save_value(
            self.params[0].read_value() + self.params[1].read_value())
        return pc + 4

    def mul(self, pc):
        # mul p1, p2, s1
        self.params[2].save_value(
            self.params[0].read_value() * self.params[1].read_value())
        return pc + 4

    def read(self, pc, in_queue: queue.Queue):
        # read p1
        user_input = in_queue.get(timeout=QUEUE_TIMEOUT)
        self.params[0].save_value(user_input)
        return pc + 2

    def write(self, pc, out_queue: queue.Queue):
        # write p1
        output_value = self.params[0].read_value()
        out_queue.put(output_value)
        return pc + 2

    def jmp_nzero(self, pc):
        # jmp_nzero p1, pc
        if self.params[0].read_value() != 0:
            return self.params[1].read_value()
        else:
            return pc + 3

    def jmp_zero(self, pc):
        # jmp_zero p1, pc
        if self.params[0].read_value() == 0:
            return self.params[1].read_value()
        else:
            return pc + 3

    def lt(self, pc):
        # lt p1, p2, s1
        if self.params[0].read_value() < self.params[1].read_value():
            self.params[2].save_value(1)
        else:
            self.params[2].save_value(0)
        return pc + 4

    def eq(self, pc):
        # eq p1, p2, s1
        if self.params[0].read_value() == self.params[1].read_value():
            self.params[2].save_value(1)
        else:
            self.params[2].save_value(0)
        return pc + 4


class Parameter:
    """
    A class for intcode instruction parameters, every parameter belongs to an instruction an has a specified mode.
    """

    PARAMETER_MODES = {"position": 0, "immediate": 1}

    def __init__(self, program: List[int], position: int, mode: int):
        self.mode = mode
        # position is an index into the source program
        self.position = position
        self.program = program

    def __str__(self) -> str:
        return f"[mode: {self.mode}, position: {self.position}, value: {self.read_value()}, raw_value: {self.program[self.position]}]"

    def __repr__(self) -> str:
        return self.__str__()

    def read_value(self) -> int:
        """ Returns the value of the parameter, considering the mode of the parameter """
        if self.mode in self.PARAMETER_MODES.values():
            if self.mode == 0:
                return self.program[self.program[self.position]]
            elif self.mode == 1:
                return self.program[self.position]
            else:
                raise LookupError(f"Wrong mode for parameter: {self}")

    def save_value(self, value: int):
        """ Saves a value to the parameter, considering the mode of the parameter """
        if self.mode in self.PARAMETER_MODES.values():
            if self.mode == 0:
                self.program[self.program[self.position]] = value
            elif self.mode == 1:
                self.program[self.position] = value
            else:
                raise LookupError(f"Wrong mode for parameter: {self}")


class IntcodeReader:
    """
    A class for translating Intcode source into python objects.
    """

    def read_file(self, filename: str) -> List[int]:
        """ Returns the intcode source as a list of integers """
        with open(filename, "r") as f:
            content = f.readlines()

        return [int(x) for x in content[0].split(",")]

    def next_instruction(self, source: List[int], pc: int) -> Instruction:
        """ Reads the next instruction following the pc. Does not change the pc. """
        full_instr_code = str(source[pc]).zfill(5)
        opcode = int(full_instr_code[3:])
        param3_mode = int(full_instr_code[:1])
        param2_mode = int(full_instr_code[1:2])
        param1_mode = int(full_instr_code[2:3])
        param_modes = [param1_mode, param2_mode, param3_mode]

        if opcode in [1, 2, 7, 8]:
            # three param instructions
            length = 3
        elif opcode in [5, 6]:
            # two param instructions
            length = 2
        elif opcode in [3, 4]:
            # single param instrcutions
            length = 1
        elif opcode == 99:
            return None
        else:
            raise LookupError(
                f"Could not create instruction for opcode: {opcode}")

        params = [Parameter(source, pc + i[0], i[1])
                  for i in zip(range(1, length + 1), param_modes)]
        return Instruction(
            source, source[pc:pc + length + 1], pc, pc + length + 1, opcode, params, length)


class IntcodeInterpreter:
    """
    A class which can execute Intcode from files or lists.
    """

    def __init__(self):
        self.reader = IntcodeReader()
        self.pc = 0

    def execute_file(self, filename: str, in_queue: queue.Queue, out_queue: queue.Queue):
        source = self.reader.read_file(filename)
        self.execute(source, in_queue, out_queue)
        self.pc = 0

    def execute(self, source: List[int], in_queue: queue.Queue, out_queue: queue.Queue):
        while True:
            instruction = self.reader.next_instruction(source, self.pc)
            if instruction is None:
                break
            else:
                self.pc = instruction.execute(
                    self.pc, in_queue, out_queue)
