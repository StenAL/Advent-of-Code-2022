from util import *
from collections import *
import copy
from functools import reduce
from math import prod

day = 5


def task1():
    f = open("input/day" + str(day) + ".txt")
    data = [line.strip("\n") for line in f.readlines()]
    stacks = []
    instructions = []
    mode = "stacks"
    for line in data:
        if line == "" or line.startswith(" "):
            mode = "instructions"
            continue
        if mode == "stacks":
            spaces = 0
            elements = []
            for el in line:
                if el in ["[", "]"]:
                    continue
                if el != " ":
                    elements.append(el)
                    spaces = 0
                else:
                    spaces += 1
                    if spaces == 4:
                        elements.append(" ")
                        spaces = 0
            for i in range(len(elements)):
                if len(stacks) <= i:
                    stacks.append([])
                if elements[i] != " ":
                    stacks[i].append(elements[i])
        if mode == "instructions":
            [_, amount, _, origin, _, to] = line.split(" ")
            instructions.append([int(amount), int(origin), int(to)])
    for [amount, origin, to] in instructions:
        moved = stacks[origin - 1][:amount]
        for el in moved:
            stacks[to - 1].insert(0, el)
            stacks[origin - 1].remove(el)

    ans = ""
    for stack in stacks:
        if len(stack) > 0:
            ans += stack[0]
    print(ans)



def task2():
    f = open("input/day" + str(day) + ".txt")
    data = [line.strip("\n") for line in f.readlines()]
    stacks = []
    instructions = []
    mode = "stacks"
    for line in data:
        if line == "" or line.startswith(" "):
            mode = "instructions"
            continue
        if mode == "stacks":
            spaces = 0
            elements = []
            for el in line:
                if el in ["[", "]"]:
                    continue
                if el != " ":
                    elements.append(el)
                    spaces = 0
                else:
                    spaces += 1
                    if spaces == 4:
                        elements.append(" ")
                        spaces = 0
            for i in range(len(elements)):
                if len(stacks) <= i:
                    stacks.append([])
                if elements[i] != " ":
                    stacks[i].append(elements[i])
        if mode == "instructions":
            [_, amount, _, origin, _, to] = line.split(" ")
            instructions.append([int(amount), int(origin), int(to)])
    for [amount, origin, to] in instructions:
        moved = stacks[origin - 1][:amount]
        for el in moved:
            stacks[origin - 1].remove(el)
        moved.extend(stacks[to - 1])
        stacks[to - 1] = moved

    ans = ""
    for stack in stacks:
        if len(stack) > 0:
            ans += stack[0]
    print(ans)


task1()
task2()
