import math
from collections.abc import Iterable

from util import *
from collections import *
import copy
import heapq
from functools import reduce
from math import prod

day = 24


def get_moves(point: (int, int), len_x: int, len_y: int) -> set[(int, int)]:
    (x, y) = point
    if (x, y) == (0, -1):
        return {(0, -1), (0, 0)}
    if (x, y) == (len_x - 1, len_y):
        return {(len_x - 1, len_y), (len_x - 1, len_y - 1)}
    neighbors = set()
    if x > 0:
        neighbors.add((x - 1, y))
    if y > 0:
        neighbors.add((x, y - 1))
    if x < len_x - 1:
        neighbors.add((x + 1, y))
    if y < len_y - 1:
        neighbors.add((x, y + 1))
    neighbors.add(point)
    return neighbors


def get_blizzards_on_turn(blizzards_memo: dict[int, set[(int, int)]], blizzards: Iterable[(int, int), str], turn,
                          len_x: int, len_y: int) -> set[(int, int)]:
    key = turn % (math.lcm(len_x, len_y))
    if key in blizzards_memo:
        return blizzards_memo[key]

    new_blizzards = set()
    for (x, y, d) in blizzards:
        if d == "^":
            new_blizzards.add((x, (y - turn) % len_y))
        elif d == ">":
            new_blizzards.add(((x + turn) % len_x, y))
        elif d == "v":
            new_blizzards.add((x, (y + turn) % len_y))
        elif d == "<":
            new_blizzards.add(((x - turn) % len_x, y))
    blizzards_memo[key] = new_blizzards
    return new_blizzards


def h(location, destination) -> int:
    return abs(destination[0] - location[0]) + abs(destination[1] - location[1])


def search(location, destination, len_x, len_y, blizzard_memo, blizzards, turn):
    best = 10000
    q = [(turn, location)]
    seen = set()
    while len(q) > 0:
        (elapsed, location) = q.pop()
        # print(len(q), elapsed, best)
        if (elapsed, location) in seen:
            continue
        seen.add((elapsed, location))
        if elapsed + h(location, destination) >= best:
            continue
        next_blizzards = get_blizzards_on_turn(blizzard_memo, blizzards, elapsed + 1, len_x, len_y)
        moves = [m for m in get_moves(location, len_x, len_y) if
                 m not in next_blizzards]
        # sorted == always go closer to destination if possible
        moves.sort(key=lambda p: abs(destination[0] - p[0]) + abs(destination[1] - p[1]), reverse=True)
        for move in moves:
            if move == destination:
                best = min(best, elapsed + 1)
                break  # no point in exploring other moves if can reach finish with one
            q.append((elapsed + 1, move))
    return best


def task1():
    data = get_input_for_day(day)
    data = get_input_for_file("test")
    data = data[1:-1]
    blizzards = set()
    len_y = len(data)
    len_x = len(data[1]) - 2
    for y in range(len(data)):
        line = data[y].strip("#")
        for x in range(len(line)):
            c = line[x]
            if c != ".":
                blizzards.add((x, y, line[x]))

    blizzard_memo = dict()
    # +1 because if dest was reached it is guaranteed the end can be reached in 1 move
    ans = search((0, -1), (len_x - 1, len_y - 1), len_x, len_y, blizzard_memo, blizzards, 0) + 1
    print(ans)
    return ans


def task2():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")
    data = data[1:-1]
    blizzards = set()
    len_y = len(data)
    len_x = len(data[1]) - 2
    for y in range(len(data)):
        line = data[y].strip("#")
        for x in range(len(line)):
            c = line[x]
            if c != ".":
                blizzards.add((x, y, line[x]))

    blizzard_memo = dict()
    there = search((0, -1), (len_x - 1, len_y - 1), len_x, len_y, blizzard_memo, blizzards, 0) + 1
    back = search((len_x - 1, len_y), (0, 0), len_x, len_y, blizzard_memo, blizzards, there) + 1
    there_again = search((0, -1), (len_x - 1, len_y - 1), len_x, len_y, blizzard_memo, blizzards, back) + 1
    ans = there_again
    print(ans)
    return ans


# task1()
task2()
