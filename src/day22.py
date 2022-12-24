from util import *
from collections import *
import copy
from functools import reduce
from math import prod

day = 22


def task1():
    data = get_raw_input_for_day(day)
    # data = get_raw_input_for_file("test")
    open_tiles = set()
    walls = set()
    mode = "tiles"
    instructions = []
    for y in range(len(data)):
        line = data[y]
        if line == "":
            mode = "instructions"
            continue
        if mode == "tiles":
            for x in range(len(line)):
                c = line[x]
                if c == ".":
                    open_tiles.add((x, y))
                if c == "#":
                    walls.add((x, y))
        if mode == "instructions":
            acc = ""
            for c in line:
                if c.isnumeric():
                    acc += c
                else:
                    instructions.append(int(str(acc)))
                    acc = ""
                    instructions += c
            if len(acc) > 0:
                instructions.append(int(str(acc)))

    location = min(open_tiles, key=lambda t: t[1] * 1000 + t[0])
    direction = "R"
    directions = ["U", "R", "D", "L"]
    direction_to_coords = {"U": (0, -1), "R": (1, 0), "D": (0, 1), "L": (-1, 0)}
    for instruction in instructions:
        if isinstance(instruction, int):
            for i in range(instruction):
                d = direction_to_coords[direction]
                dest = (location[0] + d[0], location[1] + d[1])
                if dest not in open_tiles and dest not in walls:
                    if direction == "R":
                        dest = min(t for t in open_tiles.union(walls) if t[1] == dest[1])
                    elif direction == "L":
                        dest = max(t for t in open_tiles.union(walls) if t[1] == dest[1])
                    elif direction == "U":
                        dest = max(t for t in open_tiles.union(walls) if t[0] == dest[0])
                    elif direction == "D":
                        dest = min(t for t in open_tiles.union(walls) if t[0] == dest[0])
                if dest in open_tiles:
                    location = dest
                elif dest in walls:
                    break


        else:
            if instruction == "L":
                direction = directions[(directions.index(direction) - 1) % len(directions)]
            else:
                direction = directions[(directions.index(direction) + 1) % len(directions)]
    print(location)
    facing_value = {"U": 3, "R": 0, "D": 1, "L": 2}
    ans = (location[1] + 1) * 1000 + (location[0] + 1) * 4 + facing_value[direction]
    print(ans)
    return ans


CUBE_SIZE = 50


def get_offset_in_face(p: (int, int)) -> (int, int):
    (x, y) = p

    return (x % CUBE_SIZE, y % CUBE_SIZE)


def get_face_example(p: (int, int)) -> int:
    (x, y) = p
    if CUBE_SIZE <= x < 2 * CUBE_SIZE:
        if 0 <= y < CUBE_SIZE:
            return 1
        elif CUBE_SIZE <= y < 2 * CUBE_SIZE:
            return 4
        else:
            return 5
    elif CUBE_SIZE <= y < 2 * CUBE_SIZE:
        if 0 <= x < CUBE_SIZE:
            return 2
        elif CUBE_SIZE <= x < 2 * CUBE_SIZE:
            return 3
    return 6


## only for example layout
def get_wrapping_example(p, direction: str) -> ((int, int), str):
    current_face = get_face(p)
    (offset_x, offset_y) = get_offset_in_face(p)
    if current_face == 1:
        if direction == "U":  # to 2, facing down, X axis flipped
            return (CUBE_SIZE - 1 - offset_x, CUBE_SIZE), "D"
        if direction == "L":  # to 3, facing down
            return (CUBE_SIZE + offset_y, CUBE_SIZE), "D"
        if direction == "R":  # to 6, facing left
            return (4 * CUBE_SIZE - 1, 3 * CUBE_SIZE - 1 - offset_y), "L"
    if current_face == 2:
        if direction == "U":  # to 1, facing down
            return (3 * CUBE_SIZE - 1 - offset_x, 0), "D"
        if direction == "L":  # to 6, facing up
            return (4 * CUBE_SIZE - 1 - offset_y, 3 * CUBE_SIZE - 1), "U"
        if direction == "D":  # to 5, facing up
            return (2 * CUBE_SIZE + offset_x, 3 * CUBE_SIZE - 1), "U"
    if current_face == 3:
        if direction == "U":  # to 1, facing right
            return (2 * CUBE_SIZE, offset_x), "R"
        if direction == "D":  # to 5, facing right
            return (2 * CUBE_SIZE, 3 * CUBE_SIZE - 1 - offset_x), "R"
            pass
    if current_face == 4:
        if direction == "R": # to 6, facing down
            return (4 * CUBE_SIZE - 1 - offset_y, 2 * CUBE_SIZE), "D"
    if current_face == 5:
        if direction == "L":  # to 3, facing up
            return (2 * CUBE_SIZE - 1 - offset_y, 2 * CUBE_SIZE - 1), "U" #MAYBE?
        if direction == "D":  # to 2, facing up
            return (CUBE_SIZE - 1 - offset_x, 2 * CUBE_SIZE - 1), "U"
    if current_face == 6:
        if direction == "U": # to 4, facing left
            return (3 * CUBE_SIZE - 1, 2 * CUBE_SIZE - 1 - offset_x), "L"
        if direction == "R": # to 1, facing left
            return (3 * CUBE_SIZE - 1, CUBE_SIZE - 1 - offset_y), "L"
        if direction == "D": # to 2, facing right
            return (0, 2 * CUBE_SIZE - 1 - offset_x), "R"

def get_face(p: (int, int)) -> int:
    (x, y) = p
    if x < CUBE_SIZE:
        if 2 * CUBE_SIZE <= y < 3 * CUBE_SIZE:
            return 4
        elif 3 * CUBE_SIZE <= y < 4 * CUBE_SIZE:
            return 6
    elif CUBE_SIZE <= x and x < 2 * CUBE_SIZE:
        if y < CUBE_SIZE:
            return 1
        elif y < 2 * CUBE_SIZE:
            return 3
        elif y < 3 * CUBE_SIZE:
            return 5
    return 2

def get_wrapping(p, direction: str) -> ((int, int), str):
    current_face = get_face(p)
    (offset_x, offset_y) = get_offset_in_face(p)
    if current_face == 1:
        if direction == "U": # to 6
            return (0, CUBE_SIZE * 3 + offset_x), "R"
        if direction == "L": # to 4
            return (0, CUBE_SIZE * 3 - 1 - offset_y), "R"
    if current_face == 2:
        if direction == "U": # to 6
            return (offset_x, CUBE_SIZE * 4 - 1), "U"
        if direction == "R": # to 5
            return (2 * CUBE_SIZE - 1, 3 * CUBE_SIZE - 1 - offset_y), "L"
        if direction == "D": # to 3
            return (2 * CUBE_SIZE - 1, CUBE_SIZE + offset_x), "L"
    if current_face == 3:
        if direction == "L": # to 4
            return (offset_y, 2 * CUBE_SIZE), "D"
        if direction == "R": # to 2
            return (2 * CUBE_SIZE + offset_y, CUBE_SIZE - 1), "U"
    if current_face == 4:
        if direction == "U": # to 3
            return (CUBE_SIZE, CUBE_SIZE + offset_x), "R"
        if direction == "L": # to 1
            return (CUBE_SIZE, CUBE_SIZE - 1 - offset_y), "R"
    if current_face == 5:
        if direction == "R": # to 2
            return (3 * CUBE_SIZE - 1, CUBE_SIZE - 1 - offset_y), "L"
        if direction == "D": # to 6
            return (CUBE_SIZE - 1, 3 * CUBE_SIZE + offset_x), "L"
    if current_face == 6:
        if direction == "L": # to 1
            return (CUBE_SIZE + offset_y, 0), "D"
        if direction == "D": # to 2
            return (2 * CUBE_SIZE + offset_x, 0), "D"
        if direction == "R":
            return (CUBE_SIZE + offset_y, CUBE_SIZE * 3 - 1), "U"


def task2():
    data = get_raw_input_for_day(day)
    # data = get_raw_input_for_file("test")
    open_tiles = set()
    walls = set()
    mode = "tiles"
    instructions = []
    for y in range(len(data)):
        line = data[y]
        if line == "":
            mode = "instructions"
            continue
        if mode == "tiles":
            for x in range(len(line)):
                c = line[x]
                if c == ".":
                    open_tiles.add((x, y))
                if c == "#":
                    walls.add((x, y))
        if mode == "instructions":
            acc = ""
            for c in line:
                if c.isnumeric():
                    acc += c
                else:
                    instructions.append(int(str(acc)))
                    acc = ""
                    instructions += c
            if len(acc) > 0:
                instructions.append(int(str(acc)))

    location = min(open_tiles, key=lambda t: t[1] * 1000 + t[0])
    direction = "R"
    directions = ["U", "R", "D", "L"]
    direction_to_coords = {"U": (0, -1), "R": (1, 0), "D": (0, 1), "L": (-1, 0)}
    for instruction in instructions:
        if isinstance(instruction, int):
            for i in range(instruction):
                d = direction_to_coords[direction]
                new_direction = direction
                dest = (location[0] + d[0], location[1] + d[1])
                if dest not in open_tiles and dest not in walls:
                    (dest, new_direction) = get_wrapping(location, direction)
                if dest in open_tiles:
                    location = dest
                    direction = new_direction
                elif dest in walls:
                    break
        else:
            if instruction == "L":
                direction = directions[(directions.index(direction) - 1) % len(directions)]
            else:
                direction = directions[(directions.index(direction) + 1) % len(directions)]
    facing_value = {"U": 3, "R": 0, "D": 1, "L": 2}
    ans = (location[1] + 1) * 1000 + (location[0] + 1) * 4 + facing_value[direction]
    print(ans)
    return ans


# task1()
task2()
