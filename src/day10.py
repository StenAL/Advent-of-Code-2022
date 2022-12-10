from util import *
from collections import *
import copy
from functools import reduce
from math import prod

day = 10


def task1():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")
    x = 1
    cycle = 1

    strengths = []
    for line in data:
        match line.split():
            case ["addx", val]:
                cycle += 1
                print(cycle, x)
                if cycle in [20, 60, 100, 140, 180, 220]:
                    strengths.append(x * cycle)
                x += int(val)
            case _:
                pass
        cycle += 1
        print(cycle, x)
        if cycle in [20, 60, 100, 140, 180, 220]:
            strengths.append(x * cycle)

    ans = sum(strengths)
    print(ans)
    return ans

def draw(output, x, cycle):
    # print(cycle, x, end="")
    if x + 1 >= (cycle - 1) % 40 >= x - 1:
        output.append("█")
        # print("█")
    else:
        output.append(" ")
        # print(" ")

def task2():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")
    x = 1
    cycle = 1
    output = []

    for line in data:
        draw(output, x, cycle)
        if line.startswith("addx"):
            [_, val] = line.split()
            cycle += 1
            draw(output, x, cycle)
            x += int(val)
        cycle += 1


    for i in range(len(output)):
        if i > 0 and i % 40 == 0:
            print()
        print(output[i], end="")

task1()
task2()
