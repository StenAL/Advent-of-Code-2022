from util import *
from collections import *
import copy
from functools import reduce
from math import prod

day = 15


def task1():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")
    beacons = {}
    impossible_locations = defaultdict(list)
    for line in data:
        line = (line + ".").split()
        (x1, y1, x2, y2) = line[2], line[3], line[-2], line[-1]
        (x1, y1, x2, y2) = (int(e.split("=")[1][:-1]) for e in (x1, y1, x2, y2))
        beacons[(x1, y1)] = (x2, y2)
        d = abs(x1 - x2) + abs(y1 - y2)
        for dy in range(-d, d + 1):
            x_range = d - abs(dy)
            y = y1 + dy
            impossible_locations[y].append((x1 - x_range, x1 + x_range))

    for (row, ranges) in impossible_locations.items():
        combined_ranges = []
        ranges = sorted(ranges)
        current_range = list(ranges[0])
        for i in range(len(ranges)):
            r = ranges[i]
            if current_range[1] >= r[0]:
                current_range[1] = max(r[1], current_range[1])
            else:
                combined_ranges.append(tuple(current_range))
                current_range = list(r)
        combined_ranges.append(tuple(current_range))
        impossible_locations[row] = combined_ranges

    ans_row = 2000000
    ans_row_impossible = sum(r[1] - r[0] + 1 for r in impossible_locations[ans_row])
    ans_row_beacons = {b for b in beacons.values() if b[1] == ans_row}
    ans_row_sensors = {s for s in beacons.keys() if s[1] == ans_row}
    ans = ans_row_impossible - len(ans_row_beacons) - len(ans_row_sensors)
    print(ans)
    return ans



def task2():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")
    beacons = {}
    impossible_locations = defaultdict(list)
    for line in data:
        line = (line + ".").split()
        (x1, y1, x2, y2) = line[2], line[3], line[-2], line[-1]
        (x1, y1, x2, y2) = (int(e.split("=")[1][:-1]) for e in (x1, y1, x2, y2))
        beacons[(x1, y1)] = (x2, y2)
        d = abs(x1 - x2) + abs(y1 - y2)
        for dy in range(-d, d + 1):
            x_range = d - abs(dy)
            y = y1 + dy
            impossible_locations[y].append((x1 - x_range, x1 + x_range))

    for (row, ranges) in impossible_locations.items():
        combined_ranges = []
        ranges = sorted(ranges)
        current_range = list(ranges[0])
        for i in range(len(ranges)):
            r = ranges[i]
            if current_range[1] + 1 >= r[0]:
                current_range[1] = max(r[1], current_range[1])
            else:
                combined_ranges.append(tuple(current_range))
                current_range = list(r)
        combined_ranges.append(tuple(current_range))
        impossible_locations[row] = combined_ranges

    min_y = 0
    min_x = 0
    max_y = 4000000
    max_x = 4000000
    for (row, ranges) in impossible_locations.items():
        if row < min_y or row > max_y:
            continue
        for r in ranges:
            if r[1] < max_x:
                ans_location = (r[1] + 1, row)
                break
    ans = ans_location[0] * 4000000 + ans_location[1]
    print(ans)
    return ans


# task1()
task2()
