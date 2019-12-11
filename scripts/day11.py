from common.interpreter import *
import queue
import threading

in_queue = queue.Queue()
out_queue = queue.Queue()
painted_positions = set()

directions = {"up" : (0, 1), "down" : (0, -1), "left" : (-1, 0), "right": (1, 0)}
white_positions = set()

def paint(color, position):
    if color == 1:
        white_positions.add(position)
    if color == 0 and position in white_positions:
        white_positions.remove(position)
    painted_positions.add(position)
    return (*position, color)

def set_direction_and_move(angle, direction, position):
    if angle == 0:
        if direction == "up":
            direction = "left"
        elif direction == "left":
            direction = "down"
        elif direction == "down":
            direction = "right"
        elif direction == "right":
            direction = "up" 
    elif angle == 1:
        if direction == "up":
            direction = "right"
        elif direction == "left":
            direction = "up"
        elif direction == "down":
            direction = "left"
        elif direction == "right":
            direction = "down" 
    position = (position[0] + directions[direction][0], position[1] + directions[direction][1])
    return direction, position

def run_intcode(input, output):
    interpreter = IntcodeInterpreter()
    interpreter.execute_file("inputs/day11.txt", in_queue, out_queue)
    print("finished.................................")

def run_robot(input: queue.Queue, output: queue.Queue, code: threading.Thread):
    position = (0, 0)
    direction = "up"
    white_positions.add((0, 0))
    while True:
        if position in white_positions:
            input.put(1)
        else:
            input.put(0)
        color = output.get(timeout=3)
        angle = output.get(timeout=3)
        paint(color, position)
        (direction, position) = set_direction_and_move(angle, direction, position)
            


code = threading.Thread(target=run_intcode, args=[in_queue, out_queue])
robot = threading.Thread(target=run_robot, args=[in_queue, out_queue, code])
code.start()
robot.start()

code.join()
robot.join()

# part 1
print(len(painted_positions))

min_y: int = min(white_positions, key=lambda p: p[1])[1]
max_y: int = max(white_positions, key=lambda p: p[1])[1]
min_x: int = min(white_positions, key=lambda p: p[0])[0]
max_x: int = max(white_positions, key=lambda p: p[0])[0]
print(white_positions)


for i in range(min_y, max_y + 1):
    for j in range(min_x, max_x + 1):
        if (j, i) in white_positions:
            print("#", end="")
        else:
            print(".", end="")
    print()

