"""
Day 07 of Advent of Code
"""
# pylint: disable=invalid-name
from itertools import permutations
import queue
import threading
from common.interpreter import IntcodeInterpreter


def run_interpreter(in_queue: queue.Queue, out_queue: queue.Queue, phase):
    in_queue.put(phase[i])
    in_queue.put(out_queues[i - 1].get())
    interpreter = IntcodeInterpreter()
    interpreter.execute_file("inputs/day07.txt", in_queue, out_queue)


phase_values = list(range(5, 10))
phase_settings = list(permutations(phase_values))
max_thrust = 0
best_phase = None

for phase_setting in phase_settings:
    out_queues = [queue.Queue() for _ in range(5)]
    out_queues[-1].put(0)
    threads = []

   # launch the threads
    for i in range(5):
        t = threading.Thread(target=run_interpreter, args=[
            out_queues[i - 1], out_queues[i], phase_setting])
        t.start()
        threads.append(t)

    # pick the threads back up
    for t in threads:
        t.join()

    thrust = out_queues[-1].get()
    if thrust > max_thrust:
        max_thrust = thrust
        best_phase = phase_setting

print(max_thrust, best_phase)
