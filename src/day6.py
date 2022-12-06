from util import *
from collections import *
import copy
from functools import reduce
from math import prod

day = 6


def task1():
    data = get_input_for_day(day)[0]
    # data = get_input_for_file("test")
    chars = list(data[:3])
    ans = -1
    for i in range(3, len(data)):
        el = data[i]
        chars.append(el)
        if len(set(chars)) == 4:
            ans = i + 1
            break
        chars.pop(0)
    print(ans)
    return ans



def task2():
    data = get_input_for_day(day)[0]
    # data = get_input_for_file("test")
    chars = list(data[:13])
    ans = -1
    for i in range(13, len(data)):
        el = data[i]
        chars.append(el)
        if len(set(chars)) == 14:
            ans = i + 1
            break
        chars.pop(0)
    print(ans)
    return ans


task1()
task2()
