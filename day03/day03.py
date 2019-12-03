import sys


def make_step_in_direction(coords, dir_char):
    """
        Adds a point one step in the direction given to the coordinate list given.
    """
    last_point = coords[-1]
    last_point_x = last_point[0]
    last_point_y = last_point[1]
    if dir_char == "R":
        coords.append((last_point_x + 1, last_point_y))
    elif dir_char == "L":
        coords.append((last_point_x - 1, last_point_y))
    elif dir_char == "U":
        coords.append((last_point_x, last_point_y + 1))
    elif dir_char == "D":
        coords.append((last_point_x, last_point_y - 1))


def calc_wire_path(wire_directions):
    coords = [(0, 0)]
    wire_directions = wire_directions.split(',')
    for direction in wire_directions:
        dir_char = direction[0:1]
        steps = int(direction[1:])
        for _ in range(steps):
            make_step_in_direction(coords, dir_char)
    return coords


def main():
    with open("d:/aoc/day03/input.txt", "r") as f:
        content = f.readlines()

    content = [x.strip() for x in content]
    # index is the amount of steps needed to get to the point
    first_wire_coords = calc_wire_path(content[0])
    second_wire_coords = calc_wire_path(content[1])
    first_wire_coords_set = set(first_wire_coords)
    second_wire_coords_set = set(second_wire_coords)

    intersection_coords = first_wire_coords_set & second_wire_coords_set
    distances = list(map(lambda x: abs(x[0]) + abs(x[1]), intersection_coords))
    distances.remove(0)
    # print solution to first part
    print(min(distances))

    min_steps = sys.maxsize
    nearest_intersection = None
    for intersection in intersection_coords:
        first_steps_needed = first_wire_coords.index(intersection)
        second_steps_needed = second_wire_coords.index(intersection)
        total_steps_needed = first_steps_needed + second_steps_needed
        if total_steps_needed < min_steps and intersection != (0, 0):
            min_steps = total_steps_needed
            nearest_intersection = intersection

    print(nearest_intersection)
    print(min_steps)


if __name__ == "__main__":
    main()
