import re

from util import *
from collections import *
import copy
from functools import reduce
from math import prod, ceil

day = 19


def h1(state):
    (minutes, resources, robots) = state
    acc = resources["geode"]
    will_get = resources["geode"] * minutes
    can_get = ceil((minutes / 2) * minutes)  # arithmetic progression, buy 1x geode robot each turn
    return acc + will_get + can_get


def task1():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")

    qualities = []
    for line in data:
        ore_costs = []
        numbers = list(map(int, re.findall("[0-9]+", line)))
        blueprint = numbers[0]
        costs = numbers[1:]
        ore_costs.append(costs[0])
        ore_costs.append(costs[1])
        ore_costs.append(costs[2])
        clay_cost = costs[3]
        ore_costs.append(costs[4])
        obsidian_cost = costs[5]

        robots = defaultdict(int)
        resources = defaultdict(int)
        robots["ore"] = 1
        q = [(24, resources, robots)]
        max_geodes = -1
        seen = set()
        while len(q) > 0:
            (minutes, resources, robots) = q.pop()
            hashable = (minutes, frozenset(resources.items()), frozenset(robots.items()))
            if hashable in seen:
                continue
            if h1((minutes, resources, robots)) <= max_geodes:
                continue
            if minutes == 0:
                max_geodes = max(max_geodes, resources["geode"])
                continue
            seen.add(hashable)
            actions = [(minutes - 1, resources, robots)]

            if resources["ore"] >= ore_costs[0]:
                new_robots = robots.copy()
                new_resources = resources.copy()
                new_robots["ore"] += 1
                new_resources["ore"] -= ore_costs[0]
                actions.append((minutes - 1, new_resources, new_robots))

            if resources["ore"] >= ore_costs[1]:
                new_robots = robots.copy()
                new_resources = resources.copy()
                new_robots["clay"] += 1
                new_resources["ore"] -= ore_costs[1]
                actions.append((minutes - 1, new_resources, new_robots))

            if resources["ore"] >= ore_costs[2] and resources["clay"] >= clay_cost:
                new_robots = robots.copy()
                new_resources = resources.copy()
                new_robots["obsidian"] += 1
                new_resources["ore"] -= ore_costs[2]
                new_resources["clay"] -= clay_cost
                actions.append((minutes - 1, new_resources, new_robots))

            if resources["ore"] >= ore_costs[3] and resources["obsidian"] >= obsidian_cost:
                new_robots = robots.copy()
                new_resources = resources.copy()
                new_robots["geode"] += 1
                new_resources["ore"] -= ore_costs[3]
                new_resources["obsidian"] -= obsidian_cost
                actions.append((minutes - 1, new_resources, new_robots))

            for robot in robots:
                for action in actions:
                    action[1][robot] += robots[robot]
            q.extend(actions)

        qualities.append((blueprint, max_geodes))
    ans = sum(blueprint * geodes for blueprint, geodes in qualities)
    print(ans)
    return ans


def get_new_resources(resources, robots, minutes):
    resources = resources.copy()
    for robot, n in robots.items():
        resources[robot] += n * minutes
    return resources

def h2(state, ore_costs, clay_cost, obsidian_cost):
    (minutes, resources, robots) = state
    acc = resources["geode"]

    can_get = 0
    potential_robots = robots.copy()
    potential_resources = resources.copy()
    for i in range(minutes):
        can_get += potential_robots["geode"]
        # either build geode robot or build all 3 other robots at the same time because it's hard to know which one would be most useful
        if potential_resources["ore"] >= ore_costs[3] and potential_resources["obsidian"] >= obsidian_cost:
            potential_robots["geode"] += 1
            potential_resources["ore"] -= ore_costs[2]
            potential_resources["obsidian"] -= obsidian_cost
        else:
            if potential_resources["clay"] >= clay_cost:
                potential_robots["obsidian"] += 1
                potential_resources["clay"] -= clay_cost
            potential_robots["clay"] += 1
            potential_robots["ore"] += 1
        for robot, n in potential_robots.items():
            potential_resources[robot] += n
    return can_get + acc


def task2():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")

    geodes = []
    for line in data[:3]:
        ore_costs = []
        numbers = list(map(int, re.findall("[0-9]+", line)))
        costs = numbers[1:]
        ore_costs.append(costs[0])
        ore_costs.append(costs[1])
        ore_costs.append(costs[2])
        clay_cost = costs[3]
        ore_costs.append(costs[4])
        obsidian_cost = costs[5]

        robots = defaultdict(int)
        resources = defaultdict(int)
        robots["ore"] = 1
        q = [(32, resources, robots)]
        max_geodes = -1
        seen = set()
        while len(q) > 0:
            (minutes, resources, robots) = q.pop()
            hashable = (minutes, frozenset(resources.items()), frozenset(robots.items()))
            if hashable in seen:
                continue
            if h2((minutes, resources, robots), ore_costs, clay_cost, obsidian_cost) <= max_geodes:
                continue
            seen.add(hashable)
            # print(len(q), max_geodes)
            minutes_for_ore_bot = max(ceil((ore_costs[0] - resources["ore"]) / robots["ore"]), 0) + 1
            if minutes - minutes_for_ore_bot > 0:
                new_robots = robots.copy()
                new_resources = get_new_resources(resources, robots, minutes_for_ore_bot)
                new_resources["ore"] -= ore_costs[0]
                new_robots["ore"] += 1
                q.append((minutes - minutes_for_ore_bot, new_resources, new_robots))
            else:
                max_geodes = max(max_geodes, resources["geode"] + minutes * robots["geode"])

            minutes_for_clay_bot = max(ceil((ore_costs[1] - resources["ore"]) / robots["ore"]), 0) + 1
            if minutes - minutes_for_clay_bot > 0:
                new_robots = robots.copy()
                new_resources = get_new_resources(resources, robots, minutes_for_clay_bot)
                new_resources["ore"] -= ore_costs[1]
                new_robots["clay"] += 1
                q.append((minutes - minutes_for_clay_bot, new_resources, new_robots))
            else:
                max_geodes = max(max_geodes, resources["geode"] + minutes * robots["geode"])

            if robots["clay"] > 0:
                minutes_to_collect_ore = max(ceil((ore_costs[2] - resources["ore"]) / robots["ore"]), 0)
                minutes_to_collect_clay = max(ceil((clay_cost - resources["clay"]) / robots["clay"]), 0)
                minutes_for_obsidian_bot = max(minutes_to_collect_ore, minutes_to_collect_clay) + 1

                if minutes - minutes_for_obsidian_bot > 0:
                    new_robots = robots.copy()
                    new_resources = get_new_resources(resources, robots, minutes_for_obsidian_bot)
                    new_resources["ore"] -= ore_costs[2]
                    new_resources["clay"] -= clay_cost
                    new_robots["obsidian"] += 1
                    q.append((minutes - minutes_for_obsidian_bot, new_resources, new_robots))
                else:
                    max_geodes = max(max_geodes, resources["geode"] + minutes * robots["geode"])
            if robots["obsidian"] > 0:
                minutes_to_collect_ore = max(ceil((ore_costs[3] - resources["ore"]) / robots["ore"]), 0)
                minutes_to_collect_obsidian = max(ceil((obsidian_cost - resources["obsidian"]) / robots["obsidian"]), 0)
                minutes_for_geode_bot = max(minutes_to_collect_ore, minutes_to_collect_obsidian) + 1

                if minutes - minutes_for_geode_bot > 0:
                    new_robots = robots.copy()
                    new_resources = get_new_resources(resources, robots, minutes_for_geode_bot)
                    new_resources["ore"] -= ore_costs[3]
                    new_resources["obsidian"] -= obsidian_cost
                    new_robots["geode"] += 1
                    q.append((minutes - minutes_for_geode_bot, new_resources, new_robots))
                else:
                    max_geodes = max(max_geodes, resources["geode"] + minutes * robots["geode"])

        geodes.append(max_geodes)
    ans = prod(geodes)
    print(ans)
    return ans


# task1()
task2()
