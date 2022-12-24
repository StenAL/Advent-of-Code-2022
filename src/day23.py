from typing import Iterable

from util import *
from collections import *
import copy
from functools import reduce
from math import prod

day = 23


def get_neighbors(p: (int, int)) -> set[(int, int)]:
    (x, y) = p
    neighbors = set()
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            neighbors.add((x + dx, y + dy))
    neighbors.remove(p)
    return neighbors


def task1():
    data = get_input_for_day(day)
    # data = get_input_for_file("test2")
    elves = set()
    for y in range(len(data)):
        line = data[y]
        for x in range(len(line)):
            c = line[x]
            if c == "#":
                elves.add((x, y))
    turns = 10
    for turn in range(turns):
        proposed_moves = defaultdict(list)  # destination -> everyone who wants to go there
        for elf in elves:
            (x, y) = elf
            neighbors = get_neighbors(elf)
            occupied_neighbors = neighbors.intersection(elves)
            if len(occupied_neighbors) == 0:
                continue

            for j in range(4):
                rotation = (turn + j) % 4
                if rotation == 0 and occupied_neighbors.isdisjoint({(x - 1, y - 1), (x, y - 1), (x + 1, y - 1)}):
                    proposed_moves[(x, y - 1)].append(elf)
                    break
                elif rotation == 1 and occupied_neighbors.isdisjoint({(x - 1, y + 1), (x, y + 1), (x + 1, y + 1)}):
                    proposed_moves[(x, y + 1)].append(elf)
                    break
                elif rotation == 2 and occupied_neighbors.isdisjoint({(x - 1, y - 1), (x - 1, y), (x - 1, y + 1)}):
                    proposed_moves[(x - 1, y)].append(elf)
                    break
                elif rotation == 3 and occupied_neighbors.isdisjoint({(x + 1, y - 1), (x + 1, y), (x + 1, y + 1)}):
                    proposed_moves[(x + 1, y)].append(elf)
                    break

        for dest, candidates in proposed_moves.items():
            if len(candidates) > 1:
                continue
            elf = candidates.pop()
            elves.remove(elf)
            elves.add(dest)
    min_x = min(x for (x, y) in elves)
    max_x = max(x for (x, y) in elves)
    min_y = min(y for (x, y) in elves)
    max_y = max(y for (x, y) in elves)
    ans = (max_x - min_x + 1) * (max_y - min_y + 1) - len(elves)
    print(ans)
    return ans


def task2():
    data = get_input_for_day(day)
    # data = get_input_for_file("test2")
    elves = set()
    for y in range(len(data)):
        line = data[y]
        for x in range(len(line)):
            c = line[x]
            if c == "#":
                elves.add((x, y))

    turn = 0
    while True:
        proposed_moves = defaultdict(list)  # destination -> everyone who wants to go there
        for elf in elves:
            (x, y) = elf
            neighbors = get_neighbors(elf)
            occupied_neighbors = neighbors.intersection(elves)
            if len(occupied_neighbors) == 0:
                continue

            for j in range(4):
                rotation = (turn + j) % 4
                if rotation == 0 and occupied_neighbors.isdisjoint({(x - 1, y - 1), (x, y - 1), (x + 1, y - 1)}):
                    proposed_moves[(x, y - 1)].append(elf)
                    break
                elif rotation == 1 and occupied_neighbors.isdisjoint({(x - 1, y + 1), (x, y + 1), (x + 1, y + 1)}):
                    proposed_moves[(x, y + 1)].append(elf)
                    break
                elif rotation == 2 and occupied_neighbors.isdisjoint({(x - 1, y - 1), (x - 1, y), (x - 1, y + 1)}):
                    proposed_moves[(x - 1, y)].append(elf)
                    break
                elif rotation == 3 and occupied_neighbors.isdisjoint({(x + 1, y - 1), (x + 1, y), (x + 1, y + 1)}):
                    proposed_moves[(x + 1, y)].append(elf)
                    break

        if len(proposed_moves) == 0:
            ans = turn + 1
            break
        for dest, candidates in proposed_moves.items():
            if len(candidates) > 1:
                continue
            elf = candidates.pop()
            elves.remove(elf)
            elves.add(dest)
        turn += 1

    print(ans)
    return ans


# task1()
task2()
