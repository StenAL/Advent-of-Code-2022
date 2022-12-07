from util import *
from collections import *
import copy
from functools import reduce
from math import prod

day = 7


def task1():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")
    sizes = defaultdict(int)
    directory_stack = []
    for line in data:
        if line.startswith("$ cd"):
            [_, _, destination] = line.split(" ")
            if destination == "..":
                directory_stack.pop()
            else:
                directory_stack.append(destination)
            sizes[" - ".join(directory_stack)] += 0  # force entries for empty directories
            continue
        if line.startswith("dir") or line.startswith("$ ls"):
            continue
        [size, filename] = line.split(" ")
        sizes[" - ".join(directory_stack)] += int(size)
    print(sizes)
    for dir in sizes.keys():
        for [dir2, dir2_size] in sizes.items():
            if dir != dir2 and dir2.startswith(dir):
                sizes[dir] += dir2_size
    print(sizes)
    ans = sum([x for x in sizes.values() if x <= 100000])
    print(ans)
    return ans


def task2():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")
    sizes = defaultdict(int)
    directory_stack = []
    for line in data:
        if line.startswith("$ cd"):
            [_, _, destination] = line.split(" ")
            if destination == "..":
                directory_stack.pop()
            else:
                directory_stack.append(destination)
            sizes[" - ".join(directory_stack)] += 0  # force entries for empty directories
            continue
        if line.startswith("dir") or line.startswith("$ ls"):
            continue
        [size, filename] = line.split(" ")
        sizes[" - ".join(directory_stack)] += int(size)
    for dir in sizes.keys():
        for [dir2, dir2_size] in sizes.items():
            if dir != dir2 and dir2.startswith(dir):
                sizes[dir] += dir2_size

    size_used = sizes.get("/")
    currently_unused = 70000000 - size_used
    size_needed = 30000000 - currently_unused
    ans = [size for size in sorted(sizes.values()) if size >= size_needed][0]
    print(ans)
    return ans

# task1()
task2()
