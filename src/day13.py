import functools

from util import *
from collections import *
import copy
from functools import reduce
from math import prod
import itertools

day = 13

def parse_number(line, i):
    n = ""
    while line[i].isnumeric():
        n += line[i]
        i += 1
    return int(n), i

def parse_arr(line, i):
    acc = []
    # print(f"parse_arr, {i}")
    while i < len(line):
        c = line[i]
        if c.isnumeric():
            (n, i) = parse_number(line, i)
            acc.append(n)
        elif c == "[":
            (arr, i) = parse_arr(line, i + 1)
            acc.append(arr)
        elif c == "]":
            return acc, i + 1
        elif c == ",":
            i += 1


def is_smaller(a, b):
    for (l, r) in itertools.zip_longest(a, b):
        if l is None:
            return True
        if r is None:
            return False # ran out of items
        if isinstance(l, int) and isinstance(r, int):
            if l == r:
                continue
            else:
                return r > l
        elif isinstance(l, list) and isinstance(r, list):
            smaller = is_smaller(l, r)
            if smaller is None:
                continue
            else:
                return smaller
        else:
            if isinstance(l, list):
                smaller = is_smaller(l, [r])
            else:
                smaller = is_smaller([l], r)
            if smaller is None:
                continue
            else:
                return smaller
    return None

def task1():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")
    data.append("")

    left = None
    right = None
    incorrect_lines = []
    i = 1
    for line in data:
        if left is None:
            left = parse_arr(line, 1)[0]
            continue
        if right is None:
            right = parse_arr(line, 1)[0]
            continue
        if is_smaller(left, right):
            incorrect_lines.append(i)
        left = None
        right = None
        i += 1
    ans = sum(incorrect_lines)
    print(ans)
    return ans

def is_smaller2(a, b):
    for (l, r) in itertools.zip_longest(a, b):
        if l is None:
            return 1
        if r is None:
            return -1 # ran out of items
        if isinstance(l, int) and isinstance(r, int):
            if l == r:
                continue
            else:
                return 1 if r > l else -1
        elif isinstance(l, list) and isinstance(r, list):
            smaller = is_smaller(l, r)
            if smaller is None:
                continue
            else:
                return 1 if smaller else -1
        else:
            if isinstance(l, list):
                smaller = is_smaller(l, [r])
            else:
                smaller = is_smaller([l], r)
            if smaller is None:
                continue
            else:
                return 1 if smaller else -1
    return 0

def task2():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")
    data = [l for l in data if l != ""]
    data.extend(["[[2]]", "[[6]]"])

    data = [parse_arr(line, 1)[0] for line in data]
    data.sort(key=functools.cmp_to_key(is_smaller2), reverse=True)
    ans = (data.index([[2]]) + 1) * (data.index([[6]]) + 1)
    print(ans)
    return ans


task1()
task2()
