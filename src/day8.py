from util import *
from collections import *
import copy
from functools import reduce
from math import prod

day = 8


def task1():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")
    trees = []
    for line in data:
        trees.append([])
        for i in range(len(line)):
            height = int(line[i])
            trees[-1].append(height)
    ans = 0
    for y in range(len(trees)):
        for x in range(len(trees[y])):
            height = trees[y][x]
            left = trees[y][:x]
            if len(left) == 0 or len(left) == len([tree for tree in left if tree < height]):
                ans += 1
                continue
            right = trees[y][x+1:]
            if len(right) == 0 or len(right) == len([tree for tree in right if tree < height]):
                ans += 1
                continue
            up = [trees[row][x] for row in range(0, y)]
            if len(up) == 0 or len(up) == len([tree for tree in up if tree < height]):
                ans += 1
                continue
            down = [trees[row][x] for row in range(y+1, len(trees))]
            if len(down) == 0 or len(down) == len([tree for tree in down if tree < height]):
                ans += 1
                continue
    print(ans)
    return ans


def task2():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")
    trees = []
    for line in data:
        trees.append([])
        for i in range(len(line)):
            height = int(line[i])
            trees[-1].append(height)
    ans = 0
    for y in range(len(trees)):
        for x in range(len(trees[y])):
            height = trees[y][x]
            left = trees[y][:x]
            left_higher = [i for i in range(len(left)) if left[i] >= height]
            if len(left_higher) == 0:
                left_score = len(left)
            else:
                left_score = x - left_higher[-1]

            right = trees[y][x + 1:]
            right_higher = [i + x + 1 for i in range(len(right)) if right[i] >= height]
            if len(right_higher) == 0:
                right_score = len(right)
            else:
                right_score = right_higher[0] - x

            up = [trees[row][x] for row in range(0, y)]
            up_higher = [i for i in range(len(up)) if up[i] >= height]
            if len(up_higher) == 0:
                up_score = len(up)
            else:
                up_score = y - up_higher[-1]

            down = [trees[row][x] for row in range(y + 1, len(trees))]
            down_higher = [i + y + 1 for i in range(len(down)) if down[i] >= height]
            if len(down_higher) == 0:
                down_score = len(down)
            else:
                down_score = down_higher[0] - y
            scenic_score = prod([left_score, right_score, up_score, down_score])
            ans = max(scenic_score, ans)
    print(ans)
    return ans


#task1()
task2()
