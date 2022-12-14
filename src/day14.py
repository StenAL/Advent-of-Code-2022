from util import *
from collections import *
import copy
from functools import reduce
from math import prod

day = 14


def task1():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")
    occupied = set()
    for line in data:
        line = line.split(" -> ")
        for (start, end) in zip(line, line[1:]):
            (x1, y1) = (int(n) for n in start.split(","))
            (x2, y2) = (int(n) for n in end.split(","))
            x_start = min(x1, x2)
            x_end = max(x1, x2)
            y_start = min(y1, y2)
            y_end = max(y1, y2)
            for x in range(x_start, x_end + 1):
                for y in range(y_start, y_end + 1):
                    occupied.add((x, y))
    ans = 0
    more_sand = True
    while more_sand:
        (x, y) = (500, 0)
        while True:
            if y > max(y for (x, y) in occupied):
                more_sand = False
                break
            if (x, y + 1) not in occupied:
                y += 1
                continue
            if (x - 1, y + 1) not in occupied:
                x -= 1
                y += 1
                continue
            if (x + 1, y + 1) not in occupied:
                x += 1
                y += 1
                continue
            if (x, y) not in occupied: # can't move
                occupied.add((x, y))
                ans += 1
                break
    print(ans)
    return ans



def task2():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")
    occupied = set()
    for line in data:
        line = line.split(" -> ")
        for (start, end) in zip(line, line[1:]):
            (x1, y1) = (int(n) for n in start.split(","))
            (x2, y2) = (int(n) for n in end.split(","))
            x_start = min(x1, x2)
            x_end = max(x1, x2)
            y_start = min(y1, y2)
            y_end = max(y1, y2)
            for x in range(x_start, x_end + 1):
                for y in range(y_start, y_end + 1):
                    occupied.add((x, y))
    ans = 0
    more_sand = True
    highest_y =  max(y for (x, y) in occupied) + 2

    while (500, 0) not in occupied:
        (x, y) = (500, 0)
        while True:
            if (x, y + 1) not in occupied and y + 1 != highest_y:
                y += 1
                continue
            if (x - 1, y + 1) not in occupied and y + 1 != highest_y:
                x -= 1
                y += 1
                continue
            if (x + 1, y + 1) not in occupied and y + 1 != highest_y:
                x += 1
                y += 1
                continue
            if (x, y) not in occupied: # can't move
                occupied.add((x, y))
                ans += 1
                break
    print(ans)
    return ans


# task1()
task2()
