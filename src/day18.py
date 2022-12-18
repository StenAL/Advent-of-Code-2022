from util import *
from collections import *
import copy
from functools import reduce
from math import prod

day = 18


def get_neighbors(p):
    (x, y, z) = p
    neighbors = set()
    for i in range(-1, 2):
        for j in range(-1, 2):
            for k in range(-1, 2):
                if abs(i) + abs(j) + abs(k) == 1:
                    neighbors.add((x + i, y + j, z + k))
    return neighbors


def task1():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")
    cubes = set()
    faces = 0
    for line in data:
        (x, y, z) = [int(el) for el in line.split(",")]
        faces += 6
        neighbors = get_neighbors((x, y, z))
        faces -= 2 * len(neighbors.intersection(cubes))
        cubes.add((x, y, z))
    ans = faces
    print(ans)
    return ans


def task2():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")
    cubes = set()
    for line in data:
        (x, y, z) = [int(el) for el in line.split(",")]
        cubes.add((x, y, z))

    x_min = min(x for (x, y, z) in cubes) - 2
    x_max = max(x for (x, y, z) in cubes) + 2
    y_min = min(y for (x, y, z) in cubes) - 2
    y_max = max(y for (x, y, z) in cubes) + 2
    z_min = min(z for (x, y, z) in cubes) - 2
    z_max = max(z for (x, y, z) in cubes) + 2

    shell = set() # shell of air surrounding the droplet
    q = [(x_min, y_min, z_min)]
    while len(q) > 0:
        p = q.pop()
        shell.add(p)
        neighbors = {n for n in get_neighbors(p) if
                     n[0] in range(x_min, x_max) and n[1] in range(y_min, y_max) and n[2] in range(z_min,
                                                                                                   z_max)}

        for n in neighbors - shell - cubes:
            q.append(n)
    ans = 0
    for p in shell:
        neighbors = get_neighbors(p)
        ans += len(neighbors.intersection(cubes))
    print(ans)
    return ans


task1()
task2()
