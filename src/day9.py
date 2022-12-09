from util import *
from collections import *
import copy
from functools import reduce
from math import prod, copysign

day = 9

def is_diagonal(p1, p2):
    return abs(p2[0] - p1[0]) > 0 and abs(p2[1] - p1[1]) > 0

def task1():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")
    head = [0,0]
    tail = [0,0]
    positions = set()
    for line in data:
        [direction, step] = line.split()
        step = int(step)
        for i in range(step):
            match direction:
                case "L":
                    head[0] -= 1
                case "U":
                    head[1] += 1
                case "R":
                    head[0] += 1
                case "D":
                    head[1] -= 1

            dx = head[0] - tail[0]
            dy = head[1] - tail[1]
            d = abs(dx) + abs(dy)
            if is_diagonal(head, tail) and d == 3:
                if abs(dx) > abs(dy):
                    tail[0] += dx - copysign(1, dx)
                    tail[1] += dy
                else:
                    tail[0] += dx
                    tail[1] += dy - copysign(1, dy)
            elif d == 2:
                if abs(dx) > 0:
                    tail[0] += dx - copysign(1, dx)
                else:
                    tail[1] += dy - copysign(1, dy)
            positions.add(tuple(tail))
    ans = len(positions)
    print(ans)
    return ans


def task2():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")
    positions = []
    for i in range(10):
        positions.append([0,0])
    tail_positions = {(0, 0)}
    for line in data:
        [direction, step] = line.split()
        step = int(step)
        for i in range(step):
            match direction:
                case "L":
                    positions[0][0] -= 1
                case "U":
                    positions[0][1] += 1
                case "R":
                    positions[0][0] += 1
                case "D":
                    positions[0][1] -= 1
            for j in range(1, len(positions)):
                prev = positions[j - 1]
                current = positions[j]
                dx = prev[0] - current[0]
                dy = prev[1] - current[1]
                d = abs(dx) + abs(dy)
                if is_diagonal(prev, current) and d >= 3:
                    if abs(dx) > abs(dy):
                        current[0] += dx - copysign(1, dx)
                        current[1] += dy
                    elif abs(dy) > abs(dx):
                        current[0] += dx
                        current[1] += dy - copysign(1, dy)
                    else:
                        current[0] += dx - copysign(1, dx)
                        current[1] += dy - copysign(1, dy)
                elif d == 2:
                    if abs(dx) > 0:
                        current[0] += dx - copysign(1, dx)
                    else:
                        current[1] += dy - copysign(1, dy)
            tail_positions.add(tuple(positions[-1]))

    ans = len(tail_positions)
    print(ans)
    return ans


# task1()
task2() # 7331 too high
