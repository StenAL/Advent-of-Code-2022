from util import *
from collections import *
import copy
from functools import reduce
from math import prod
import sys

day = 12
sys.setrecursionlimit(1500)

def get_neighbors(point: (int, int), x_max: int, y_max: int) -> set[(int, int)]:
    (x, y) = point
    neighbors = set()
    if x > 0:
        neighbors.add((x - 1, y))
    if y > 0:
        neighbors.add((x, y - 1))
    if x < x_max - 1:
        neighbors.add((x + 1, y))
    if y < y_max - 1:
        neighbors.add((x, y + 1))
    return neighbors

def get_height(elevations, point):
    height = elevations[point[1]][point[0]]
    if height == "S":
        height = "a"
    if height == "E":
        height = "z"
    return height

def search(elevations: list[list[str]], current: (int, int), memo: dict[(int, int), int], cost: int):
    if current in memo and memo[current] <= cost:
        return []
    memo[current] = cost
    current_height = get_height(elevations, current)
    neighbors = get_neighbors(current, len(elevations[0]), len(elevations))
    valid_neighbors = {point for point in neighbors if
                       ord(get_height(elevations, point)) <= ord(current_height) + 1}

    valid_neighbors = {point for point in valid_neighbors if
                       point not in memo or memo[point] > cost + 1}

    solutions = []
    for n in valid_neighbors:
        if elevations[n[1]][n[0]] == "E":
            return [cost + 1]
        solution = search(elevations, n, memo, cost + 1)
        solutions.extend(solution)
    return solutions


def task1():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")
    elevations = []
    for i in range(len(data)):
        line = data[i]
        elevation = []
        for j in range(len(line)):
            c = line[j]
            elevation.append(c)
            if c == "S":
                origin = (j, i)
        elevations.append(elevation)
    solutions = search(elevations, origin, {}, 0)
    ans = min(solutions)
    print(ans)
    return ans

def search2(elevations: list[list[str]], current: (int, int), memo: dict[(int, int), int], cost: int):
    if current in memo and memo[current] <= cost:
        return []
    memo[current] = cost
    current_height = get_height(elevations, current)
    neighbors = get_neighbors(current, len(elevations[0]), len(elevations))
    valid_neighbors = {point for point in neighbors if
                       ord(get_height(elevations, point)) >= ord(current_height) - 1}

    valid_neighbors = {point for point in valid_neighbors if
                       point not in memo or memo[point] > cost + 1}

    solutions = []
    for n in valid_neighbors:
        if elevations[n[1]][n[0]] == "a":
            return [cost + 1]
        solution = search2(elevations, n, memo, cost + 1)
        solutions.extend(solution)
    return solutions

def task2():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")
    elevations = []
    for i in range(len(data)):
        line = data[i]
        elevation = []
        for j in range(len(line)):
            c = line[j]
            elevation.append(c)
            if c == "E":
                origin = (j, i)
        elevations.append(elevation)
    solutions = search2(elevations, origin, {}, 0)
    ans = min(solutions)
    print(ans)
    return ans


# task1()
task2()
