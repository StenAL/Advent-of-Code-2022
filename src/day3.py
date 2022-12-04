from util import *
from collections import *
import copy
from functools import reduce
from math import prod

day = 3


def task1():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")
    priorities = []
    for line in data:
        length = len(line)
        compartments = [line[:length//2], line[length//2:]]
        counters = [set(Counter(compartment).keys()) for compartment in compartments]
        dupe = counters[0].intersection(counters[1]).pop()
        priority = ord(dupe) - 96 if dupe.islower() else ord(dupe) - 64 + 26
        priorities.append(priority)

    ans = sum(priorities)
    print(ans)
    return ans

def task2():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")
    priorities = []
    group = []
    for line in data:
        group.append(line)
        if len(group) != 3:
            continue

        counters = [set(Counter(x).keys()) for x in group]
        dupe = counters[0].intersection(counters[1]).intersection(counters[2]).pop()
        priority = ord(dupe) - 96 if dupe.islower() else ord(dupe) - 64 + 26
        priorities.append(priority)
        group = []

    ans = sum(priorities)
    return ans


# task1()
task2()
