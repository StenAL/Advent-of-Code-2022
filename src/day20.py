from util import *
from collections import *
import copy
from functools import reduce
from math import prod

day = 20

class N:
    def __init__(self, n: int):
        self.n = n
    def __repr__(self):
        return str(self.n)

def task1():
    data = get_int_input_for_day(day)
    # data = get_int_input_for_file("test")
    data = [N(n) for n in data]
    numbers = data
    d = deque(numbers)
    for n in numbers:
        while d[0] != n:
            d.rotate(-1)
        d.popleft()
        shift = -(n.n % len(d))
        d.rotate(shift)
        d.appendleft(n)

    while d[0].n != 0:
        d.rotate(-1)
    coords =[d[1000 % len(d)], d[2000 % len(d)], d[3000 % len(d)]]
    ans = sum(n.n for n in coords)
    print(ans)
    return ans

def task2():
    data = get_int_input_for_day(day)
    # data = get_int_input_for_file("test")
    key = 811589153
    data = [N(n * key) for n in data]
    numbers = data
    d = deque(numbers)
    for i in range(10):
        for n in numbers:
            while d[0] != n:
                d.rotate(-1)
            d.popleft()
            shift = -(n.n % len(d))
            d.rotate(shift)
            d.appendleft(n)

    while d[0].n != 0:
        d.rotate(-1)
    coords =[d[1000 % len(d)], d[2000 % len(d)], d[3000 % len(d)]]
    ans = sum(n.n for n in coords)
    print(ans)
    return ans


# task1()
task2()
