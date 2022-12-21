import ast

from util import *
from collections import *
import copy
from functools import reduce
from math import prod

day = 21


def task1():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")

    monkeys = {}
    for line in data:
        (monkey, yell) = line.split(": ")
        if yell.isnumeric():
            monkeys[monkey] = int(yell)
        else:
            monkeys[monkey] = yell
    while isinstance(monkeys["root"], str):
        unresolved = {(k,v) for k,v in monkeys.items() if isinstance(v, str)}
        for k,v in unresolved:
            match v.split(" "):
                case [a, "+", b]:
                    if isinstance(monkeys[a], int) and isinstance(monkeys[b], int):
                        monkeys[k] = monkeys[a] + monkeys[b]
                case [a, "-", b]:
                    if isinstance(monkeys[a], int) and isinstance(monkeys[b], int):
                        monkeys[k] = monkeys[a] - monkeys[b]
                case [a, "*", b]:
                    if isinstance(monkeys[a], int) and isinstance(monkeys[b], int):
                        monkeys[k] = monkeys[a] * monkeys[b]
                case [a, "/", b]:
                    if isinstance(monkeys[a], int) and isinstance(monkeys[b], int):
                        monkeys[k] = monkeys[a] // monkeys[b]
    ans = monkeys["root"]
    print(ans)
    return ans


def task2():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")

    monkeys = {}
    for line in data:
        (monkey, yell) = line.split(": ")
        if yell.isnumeric():
            monkeys[monkey] = int(yell)
        elif monkey == "root":
            monkeys[monkey] = yell.replace("+", "=")
        else:
            monkeys[monkey] = yell
    monkeys["humn"] = "x"

    while True:
        unresolved = {(k,v) for k,v in monkeys.items() if isinstance(v, str)}
        for k,v in unresolved:
            match v.split(" "):
                case [a, "+", b]:
                    if isinstance(monkeys[a], int) and isinstance(monkeys[b], int):
                        monkeys[k] = monkeys[a] + monkeys[b]
                case [a, "-", b]:
                    if isinstance(monkeys[a], int) and isinstance(monkeys[b], int):
                        monkeys[k] = monkeys[a] - monkeys[b]
                case [a, "*", b]:
                    if isinstance(monkeys[a], int) and isinstance(monkeys[b], int):
                        monkeys[k] = monkeys[a] * monkeys[b]
                case [a, "/", b]:
                    if isinstance(monkeys[a], int) and isinstance(monkeys[b], int):
                        monkeys[k] = monkeys[a] // monkeys[b]
        unresolved_new = {(k,v) for k,v in monkeys.items() if isinstance(v, str)}
        if len(unresolved) == len(unresolved_new):
            break

    equation = monkeys["root"]
    while True:
        length_before = len(equation)
        for t in equation.split():
            t = t.strip(")").lstrip("(")
            if t not in "*+-/=" and t.isalpha() and t != "x":
                equation = equation.replace(t, f"({str(monkeys[t])})")
        if len(equation) == length_before:
            break

    # (((((58451531945585) - (((156) + (((((((96) + ((314) + ((((417) + (((((((573) + ((((((((((((2) * (((((((2) * ((268) + (((((339) + ((7) * ((547) + (((((931) + ((((((((((((2) * ((651) + ((((2) * ((((((x) - (115)) * (33)) + (970)) / (2)) - (659))) + (472)) / (2)))) - (345)) + (704)) / (3)) + (652)) + (500)) / (3)) - (566)) * (3)) - (721)) / (5))) * (6)) - (302)) / (4))))) / (2)) - (353)) * (3)))) - (380)) / (2)) + (500)) / (5)) - (457))) - (930)) * (2)) + (360)) / (4)) - (685)) * (3)) + (962)) / (11)) - (859)) / (2))) * (35)) + (552)) / (4)) - (999)) * (4))) * (2)) - (523)))) / (7)) - (582)) + (306)) + (33)) / (2))) * (2))) * (2)) + (181)) / (3)) = (17522552903925)
    # pass above into equation simplifier (https://quickmath.com/webMathematica3/quickmath/algebra/simplify/basic.jsp) and get answer

    desired = int(equation.split(" = ")[1].strip("(").strip(")"))
    equation = equation.split(" = ")[0]


    f_zero = eval(equation, {"x": 0})
    f_one = eval(equation, {"x": 0})
    increasing = f_one - f_zero > 0

    min_x = 1
    max_x = None
    x = min_x
    ans = -1
    if not increasing:
        while True:
            if max_x is not None:
                x = min_x + (max_x - min_x) // 2
            res = eval(equation, {"x": x})
            if res > desired:
                min_x = x
                if max_x is None:
                    x *= 2
            elif res < desired:
                max_x = x
            else:
                ans = x
                break
    print(ans)
    return ans

# task1()
task2()
