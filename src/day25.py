from util import *
from collections import *
import copy
from functools import reduce
import math

day = 25

def symbol_to_n(symbol: str) -> int:
    if symbol.isnumeric():
        return int(symbol)
    match symbol:
        case "-": return -1
        case "=": return -2

def n_to_symbols(decimal: int) -> str:
    acc = ""
    while decimal > 0:
        digit = decimal % 5 # rightmost
        decimal = decimal // 5
        match digit:
            case 0: acc = "0" + acc
            case 1: acc = "1" + acc
            case 2: acc = "2" + acc
            case 3:
                acc = "=" + acc
                decimal += 1
            case 4:
                acc = "-" + acc
                decimal += 1
    return acc



def task1():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")
    numbers = []
    for line in data:
        n = 0
        for i in range(len(line)):
            c = line[len(line) - 1 - i]
            n += 5 ** i * symbol_to_n(c)
        numbers.append(n)
    s = sum(numbers)
    ans = n_to_symbols(s)
    print(ans)
    return ans


task1()
# task2()
