"""
Provides classes for interpreting intcode programs.
"""
from typing import List
import queue

QUEUE_TIMEOUT = 3


class InterpreterContext:
    """
    A class for capturing the state for the interpreter. Allows the manipulation of interpreter state from instructions.
    """

    def __init__(self, source, in_queue, out_queue):
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.relative_base = 0
        self.pc = 0
        self.source = source


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
            8: self.eq,
            9: self.adj_relbase
        }

    def __str__(self):
        return f"[opcode: {self.opcode}, num_of_params: {self.num_of_params}, params: {str(self.params)}, raw_intcode: {self.raw_intcode}]"

    def execute(self, context: InterpreterContext) -> bool:
        """ Executes the instruction.
            Has following sideeffects:
                updates the pc depending on the length of the executed instruction,
                updates values in the source program.
        """

        if self.opcode in self.OPCODE_FUNCTION_MAP.keys():
            func = self.OPCODE_FUNCTION_MAP[self.opcode]
            return func(context)
        else:
            raise LookupError(
                f"Could not run interpreter function for instruction: {self}")

    def add(self, context: InterpreterContext):
        # add p1, p2, s1
        self.params[2].save_value(
            self.params[0].read_value(context) + self.params[1].read_value(context), context)
        return context.pc + 4

    def mul(self, context: InterpreterContext):
        # mul p1, p2, s1
        self.params[2].save_value(
            self.params[0].read_value(context) * self.params[1].read_value(context), context)
        return context.pc + 4

    def read(self, context: InterpreterContext):
        # read p1
        user_input = context.in_queue.get(timeout=QUEUE_TIMEOUT)
        self.params[0].save_value(user_input, context)
        return context.pc + 2

    def write(self, context: InterpreterContext):
        # write p1
        output_value = self.params[0].read_value(context)
        context.out_queue.put(output_value)
        return context.pc + 2

    def jmp_nzero(self, context: InterpreterContext):
        # jmp_nzero p1, pc
        if self.params[0].read_value(context) != 0:
            return self.params[1].read_value(context)
        else:
            return context.pc + 3

    def jmp_zero(self, context: InterpreterContext):
        # jmp_zero p1, pc
        if self.params[0].read_value(context) == 0:
            return self.params[1].read_value(context)
        else:
            return context.pc + 3

    def lt(self, context: InterpreterContext):
        # lt p1, p2, s1
        if self.params[0].read_value(context) < self.params[1].read_value(context):
            self.params[2].save_value(1, context)
        else:
            self.params[2].save_value(0, context)
        return context.pc + 4

    def eq(self, context: InterpreterContext):
        # eq p1, p2, s1
        if self.params[0].read_value(context) == self.params[1].read_value(context):
            self.params[2].save_value(1, context)
        else:
            self.params[2].save_value(0, context)
        return context.pc + 4

    def adj_relbase(self, context: InterpreterContext):
        # adj_relbase p1
        context.relative_base += self.params[0].read_value(context)
        return context.pc + 2


class Parameter:
    """
    A class for intcode instruction parameters, every parameter belongs to an instruction an has a specified mode.
    """

    PARAMETER_MODES = {"position": 0, "immediate": 1, "relative": 2}

    def __init__(self, program: List[int], position: int, mode: int):
        self.mode = mode
        # position is an index into the source program
        self.position = position
        self.program = program

    def __str__(self) -> str:
        return f"[mode: {self.mode}, position: {self.position}, value: {self.read_value()}, raw_value: {self.program[self.position]}]"

    def __repr__(self) -> str:
        return self.__str__()

    def read_value(self, context: InterpreterContext) -> int:
        """ Returns the value of the parameter, considering the mode of the parameter """
        if self.mode in self.PARAMETER_MODES.values():
            if self.mode == 0:
                return self.program[self.program[self.position]]
            elif self.mode == 1:
                return self.program[self.position]
            elif self.mode == 2:
                return self.program[context.relative_base + self.program[self.position]]
            else:
                raise LookupError(f"Wrong mode for parameter: {self}")

    def save_value(self, value: int, context: InterpreterContext):
        """ Saves a value to the parameter, considering the mode of the parameter """
        if self.mode in self.PARAMETER_MODES.values():
            if self.mode == 0:
                self.program[self.program[self.position]] = value
            elif self.mode == 1:
                self.program[self.position] = value
            elif self.mode == 2:
                self.program[context.relative_base +
                             self.program[self.position]] = value
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
        elif opcode in [3, 4, 9]:
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

    def execute_file(self, filename: str, in_queue: queue.Queue, out_queue: queue.Queue):
        source = self.reader.read_file(filename)
        self.execute(source, in_queue, out_queue)

    def execute(self, source: List[int], in_queue: queue.Queue, out_queue: queue.Queue):
        source.extend([0 for _ in range(2 ** 16 - len(source))])
        context = InterpreterContext(source, in_queue, out_queue)
        while True:
            instruction = self.reader.next_instruction(source, context.pc)
            if instruction is None:
                break
            else:
                context.pc = instruction.execute(context)
