from util import *
from collections import *
import copy
from functools import reduce
from math import prod

day = 1


def task1():
    data = get_input_for_day(day)
    ans = -1
    acc = 0
    for line in data:
        if line == "":
            ans = max(ans, acc)
            acc = 0
        else:
            acc += int(line)
    print(ans)
    return ans


def task2():
    data = get_input_for_day(day)
    cals = []
    acc = 0
    for line in data:
        if line == "":
            cals.append(acc)
            acc = 0
        else:
            acc += int(line)
    ans = sum(sorted(cals, reverse=True)[:3])
    print(ans)
    return ans


task1()
task2()
