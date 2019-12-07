"""
Day 07 of Advent of Code
"""
# pylint: disable=invalid-name
from itertools import permutations
import queue
from common.interpreter import IntcodeInterpreter

interpreter = IntcodeInterpreter()
phase_values = list(range(5, 10))
phase_settings = list(permutations(phase_values))
max_thruster_signal = 0
best_phase = None
output = [0]  # the input for the first amplifier is always zero


for phase_setting in phase_settings:
    for i in range(5):
        input_value = output.pop(0)
        interpreter.execute_file(
            "inputs/day07.txt", input=[phase_setting[i], input_value], output=output)
    if output[0] > max_thruster_signal:
        max_thruster_signal = output[0]
        best_phase = phase_setting
    output.clear()

print(max_thruster_signal)
print(best_phase)
