from util import *
from collections import *
import copy
from functools import reduce
from math import prod

day = 11

def run_operation(operation, old):
    return eval(operation.replace("old", str(old)))

def run_test(test, worry):
    divisor = int(test.split()[-1])
    return worry % divisor == 0

def task1():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")
    monkeys = []
    current_monkey = {"inspected": 0}
    for line in data:
        match line.split():
            case ["Monkey", *_]:
                continue
            case ["Starting", "items:", *items]:
                current_monkey["items"] = tuple([int(x.strip(",")) for x in items])
            case ["Operation:", "new", "=", *operation]:
                current_monkey["operation"] = " ".join(operation)
            case ["Test:", *test]:
                current_monkey["test"] = " ".join(test)
            case ["If", "true:", *if_true]:
                current_monkey["if_true"] = int(if_true[-1])
            case ["If", "false:", *if_false]:
                current_monkey["if_false"] =  int(if_false[-1])
            case []:
                monkeys.append(current_monkey)
                current_monkey = {"inspected": 0}
    monkeys.append(current_monkey)

    rounds = 20
    for i in range(rounds):
        for monkey in monkeys:
            for item in monkey["items"]:
                item = run_operation(monkey["operation"], item)
                item //= 3
                dest = monkey["if_true"] if run_test(monkey["test"], item) else monkey["if_false"]

                old = monkeys[dest]["items"]
                new = (*old, item)
                monkeys[dest]["items"] = new
            monkey["inspected"] += len(monkey["items"])
            monkey["items"] = ()

    inspected = [monkey["inspected"] for monkey in monkeys]
    ans = prod(sorted(inspected, reverse=True)[:2])
    print(ans)
    return ans

def run_operation2(operation, item, divisors):
    output = []
    for i in range(len(divisors)):
        res = eval(operation.replace("old", str(item[i])))
        output.append(res % divisors[i])
    return tuple(output)

def run_test2(divisor, worry):
    return worry % divisor == 0

def task2():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")
    monkeys = []
    current_monkey = {"inspected": 0}
    for line in data:
        match line.split():
            case ["Monkey", *_]:
                continue
            case ["Starting", "items:", *items]:
                current_monkey["items"] = tuple([int(x.strip(",")) for x in items])
            case ["Operation:", "new", "=", *operation]:
                current_monkey["operation"] = " ".join(operation)
            case ["Test:", "divisible", "by", test]:
                current_monkey["test"] = int(test)
            case ["If", "true:", *if_true]:
                current_monkey["if_true"] = int(if_true[-1])
            case ["If", "false:", *if_false]:
                current_monkey["if_false"] =  int(if_false[-1])
            case []:
                monkeys.append(current_monkey)
                current_monkey = {"inspected": 0}
    monkeys.append(current_monkey)
    divisors = [monkey["test"] for monkey in monkeys]
    for monkey in monkeys:
        new_items = []
        for item in monkey["items"]:
            new_item = []
            for divisor in divisors:
                new_item.append(item % divisor)
            new_items.append(tuple(new_item))
        monkey["items"] = tuple(new_items)

    rounds = 10000
    for r in range(rounds):
        # if r % 100 == 0:
        #     print(r)
        for i in range(len(monkeys)):
            monkey = monkeys[i]
            for item in monkey["items"]:
                item = run_operation2(monkey["operation"], item, divisors)
                dest = monkey["if_true"] if run_test2(monkey["test"], item[i]) else monkey["if_false"]

                old = monkeys[dest]["items"]
                new = (*old, item)
                monkeys[dest]["items"] = new
            monkey["inspected"] += len(monkey["items"])
            monkey["items"] = ()

    inspected = [monkey["inspected"] for monkey in monkeys]
    ans = prod(sorted(inspected, reverse=True)[:2])
    print(ans)
    return ans


# task1()
task2()
