from util import *
from collections import *
import copy
from functools import reduce
from math import prod

day = 17


def task1():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")
    pattern = data[0]
    max_height = 0
    turn = 0
    rocks = 0
    occupied = set()
    bricks = [{(0, 0), (1, 0), (2, 0), (3, 0)}, {(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)},
              {(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)}, {(0, 0), (0, 1), (0, 2), (0, 3)},
              {(0, 0), (1, 0), (0, 1), (1, 1)}]
    while rocks < 2022:
        brick = bricks[rocks % len(bricks)]
        x = 2
        y = max_height + 3

        brick_falling = True
        while brick_falling:
            direction = pattern[turn % len(pattern)]

            if direction == "<":
                leftmost = min(x + x1 for (x1, _) in brick)
                should_move = all((x1 + x - 1, y + y1) not in occupied for (x1, y1) in brick) and leftmost != 0
                if should_move:
                    x -= 1
            else:
                rightmost = max(x + x1 for (x1, _) in brick)
                should_move = all((x1 + x + 1, y + y1) not in occupied for (x1, y1) in brick) and rightmost != 6
                if should_move:
                    x += 1

            lowest = min(y + y1 for (_, y1) in brick)
            should_fall = all((x1 + x, y + y1 - 1) not in occupied for (x1, y1) in brick) and lowest != 0
            if should_fall:
                y -= 1
            else:
                occupied.update((x1 + x, y1 + y) for (x1, y1) in brick)
                rocks += 1
                brick_falling = False
                max_height = max(max_height, max(y1 + y for (_, y1) in brick) + 1)

            turn += 1
    ans = max_height
    print(ans)
    return ans

def get_neighbors(point):
    (x, y) = point
    neighbors = set()
    if x > 0:
        neighbors.add((x - 1, y))
    if y > 0:
        neighbors.add((x, y - 1))
    if x < 6:
        neighbors.add((x + 1, y))
    return neighbors

def get_exposed_surface(occupied_spaces):
    y = max(y for (x, y) in occupied_spaces) + 1
    q = [(0, y)]
    exposed_surface = set()
    seen = set()
    while len(q) > 0:
        p = q.pop()
        seen.add(p)
        neighbors = get_neighbors(p)
        for n in neighbors:
            if n in occupied_spaces:
                exposed_surface.add(n)
            elif n not in seen:
                q.append(n)
    y_min = min(y1 for (_, y1) in exposed_surface)
    exposed_surface = {(x1, y1 - y_min) for (x1, y1) in exposed_surface} # normalize for height
    return exposed_surface


def task2():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")
    pattern = data[0]
    max_height = 0
    pattern_index = 0
    brick_index = 0
    total_rocks = 0
    occupied = set()
    bricks = [{(0, 0), (1, 0), (2, 0), (3, 0)}, {(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)},
              {(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)}, {(0, 0), (0, 1), (0, 2), (0, 3)},
              {(0, 0), (1, 0), (0, 1), (1, 1)}]


    seen = set()

    period_start = None
    period = None
    max_height_growth = []

    while True:
        brick = bricks[brick_index]
        x = 2
        y = max_height + 3

        brick_falling = True
        while brick_falling:
            direction = pattern[pattern_index]

            if direction == "<":
                leftmost = min(x + x1 for (x1, _) in brick)
                should_move = all((x1 + x - 1, y + y1) not in occupied for (x1, y1) in brick) and leftmost != 0
                if should_move:
                    x -= 1
            else:
                rightmost = max(x + x1 for (x1, _) in brick)
                should_move = all((x1 + x + 1, y + y1) not in occupied for (x1, y1) in brick) and rightmost != 6
                if should_move:
                    x += 1

            lowest = min(y + y1 for (_, y1) in brick)
            should_fall = all((x1 + x, y + y1 - 1) not in occupied for (x1, y1) in brick) and lowest != 0
            if should_fall:
                y -= 1
            else:
                occupied.update((x1 + x, y1 + y) for (x1, y1) in brick)
                brick_index = (brick_index + 1) % len(bricks)
                total_rocks += 1
                brick_falling = False
                old_max_height = max_height
                max_height = max(max_height, max(y1 + y for (_, y1) in brick) + 1)
                if period_start is not None:
                    max_height_growth.append(max_height - old_max_height)

            pattern_index = (pattern_index + 1) % len(pattern)

        exposed_surface = frozenset(get_exposed_surface(occupied))
        if (exposed_surface, pattern_index, brick_index) in seen:
            if period_start is None:
                period_start = (total_rocks, max_height)
            elif period is None:
                period = (total_rocks - period_start[0], max_height - period_start[1])
                break
            seen = set()
        seen.add((exposed_surface, pattern_index, brick_index))

    target = 1000000000000

    iterations = (target - period_start[0]) // period[0]
    remainder = (target - period_start[0]) % period[0]
    ans = period_start[1] + iterations * period[1] + sum(max_height_growth[0:remainder])
    print(ans)
    return ans


# task1()
task2()
