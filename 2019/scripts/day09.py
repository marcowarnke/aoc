import queue
from common.interpreter import *

input_queue = queue.Queue()
input_queue.put(2)
output_queue = queue.Queue()
interpreter = IntcodeInterpreter()
interpreter.execute_file("inputs/day09.txt", input_queue, output_queue)

print(output_queue.queue)
