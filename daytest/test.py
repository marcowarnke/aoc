from intcode import interpreter

vm = interpreter.IntcodeInterpreter()
vm.execute([1101, 1, 1, 0, 4, 0, 99])
