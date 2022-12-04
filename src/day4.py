from util import *
from collections import *
import copy
from functools import reduce
from math import prod

day = 4


def task1():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")
    ans = 0
    for line in data:
        ranges = [[int(y) for y in x.split("-")] for x in line.split(",")]
        if ranges[0][0] <= ranges[1][0] and ranges[0][1] >= ranges[1][1]:
            ans += 1
        elif ranges[1][0] <= ranges[0][0] and ranges[1][1] >= ranges[0][1]:
            ans += 1
    print(ans)
    return ans


def task2():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")
    ans = 0
    for line in data:
        ranges = [[int(y) for y in x.split("-")] for x in line.split(",")]
        if ranges[0][0] <= ranges[1][0] <= ranges[0][1]:
            ans += 1
        elif ranges[0][0] <= ranges[1][1] <= ranges[0][1]:
            ans += 1
        elif ranges[1][0] <= ranges[0][0] <= ranges[1][1]:
            ans += 1
        elif ranges[1][0] <= ranges[0][1] <= ranges[1][1]:
            ans += 1
    print(ans)
    return ans


# task1()
task2()
