import heapq
from typing import Iterable

from util import *
from collections import *
import copy
from functools import reduce
from math import prod

day = 16

"""Ford-Fulkerson"""


def get_distance_map(neighbors_map: dict[str, Iterable[str]]) -> dict[(str, str), int]:
    distance_map = defaultdict(lambda: 10000)
    for s, neighbors in neighbors_map.items():
        distance_map[(s, s)] = 0
        for n in neighbors:
            distance_map[(s, n)] = 1

    for k in neighbors_map:
        for i in neighbors_map:
            for j in neighbors_map:
                distance_map[(i, j)] = min(distance_map[(i, k)] + distance_map[(k, j)], distance_map[(i, j)])
    return distance_map


def get_reachable(location, neighbors_map):
    reachable = {location}
    q = [location]
    while len(q) > 0:
        neighbors = (n for n in neighbors_map[location] if n not in reachable)
        reachable.update(neighbors)
        for n in neighbors:
            q.append(n)


def search(neighbors_map: dict[str, Iterable[str]], flow_map, location):
    q: list[(int, int, set[str], str)] = [(0, 30, set(), location)]
    distance_map = get_distance_map(neighbors_map)
    max_flow = 0
    valves = {l for l in neighbors_map.keys() if flow_map[l] > 0}

    while len(q) > 0:
        (acc, minutes_remaining, open_valves, location) = q.pop()
        # print(acc, minutes_remaining, open_valves, location)
        flow = sum(flow_map[valve] for valve in open_valves)
        closed_valves = valves - open_valves - {location}
        reachable_closed_valves = {v for v in closed_valves if distance_map[(location, v)] + 1 < minutes_remaining}
        if len(reachable_closed_valves) == 0:
            new_acc = acc + flow * minutes_remaining
            # print(f"({acc} -> {new_acc}) wait until end at {location}, minutes remaining: {minutes_remaining}")
            max_flow = max(max_flow, new_acc)
            continue

        for closed_valve in reachable_closed_valves:
            distance = distance_map[(location, closed_valve)]
            new_acc = (distance + 1) * flow + acc  # acc increases by distance * flow during movement
            new_minutes_remaining = minutes_remaining - distance - 1  # 1 min to open valve
            # print(f"({acc} -> {new_acc}) go from {location} to {closed_valve}, minutes remaining: {new_minutes_remaining}")
            q.append((new_acc, new_minutes_remaining, open_valves.union({closed_valve}), closed_valve))
            max_flow = max(max_flow, new_acc)
        # print("")
    return max_flow

"""max score that can be possibly achieved in current state"""
def h(neighbors_map: dict[str, Iterable[str]], flow_map, state):
    (acc, minutes_remaining, open_valves, agents) = state
    open_valves = open_valves.copy()
    valves = {l for l in neighbors_map.keys() if flow_map[l] > 0}
    closed_valves = list(sorted(valves - open_valves, key=lambda v: flow_map[v]))
    heuristic = acc + sum(flow_map[v] for v in open_valves) * minutes_remaining
    while minutes_remaining > 0 and len(closed_valves) > 0:
        v1 = flow_map[closed_valves.pop()]
        heuristic += minutes_remaining * v1
        if len(closed_valves) > 0:
            v2 = flow_map[closed_valves.pop()]
            heuristic += minutes_remaining * v2
        minutes_remaining -= 2
    return heuristic





def search2(neighbors_map: dict[str, Iterable[str]], flow_map, locations):
    agents = [(l, 0) for l in locations]  # 2nd element in tuple = how long is agent busy
    starting_state = (0, 26, set(), agents)
    q: list[(int, int, set[str], str)] = [(h(neighbors_map, flow_map, starting_state), starting_state)]
    distance_map = get_distance_map(neighbors_map)
    max_flow = 0
    valves = {l for l in neighbors_map.keys() if flow_map[l] > 0}
    seen_states = set()

    while len(q) > 0:
        (_, (acc, minutes_remaining, open_valves, agents)) = heapq.heappop(q)
        agent_locations = {a[0] for a in agents}
        closed_valves = valves - open_valves - agent_locations

        agent_actions = []
        for agent in agents:
            new_agent_states = []
            agent_actions.append(new_agent_states)
            location, current_action_duration = agent
            if current_action_duration > 0:
                new_agent_states.append((location, current_action_duration))
                continue

            reachable_closed_valves = {v for v in closed_valves if distance_map[(location, v)] + 1 < minutes_remaining}
            if len(reachable_closed_valves) == 0:
                new_agent_states.append((location, minutes_remaining))
                continue

            for closed_valve in reachable_closed_valves:
                distance = distance_map[(location, closed_valve)]
                new_state = (closed_valve, distance + 1)
                new_agent_states.append(new_state)

        flow = sum(flow_map[valve] for valve in open_valves)
        for (location_1, duration_1) in agent_actions[0]:
            for (location_2, duration_2) in agent_actions[1]:
                if location_1 != location_2:
                    newly_opened_valves = set()
                    if duration_1 <= duration_2:
                        newly_opened_valves.add(location_1)
                    if duration_2 <= duration_1:
                        newly_opened_valves.add(location_2)
                    action_duration = min(duration_1, duration_2)

                    new_acc = acc + flow * action_duration
                    max_flow = max(max_flow, new_acc)
                    new_agents = ((location_1, duration_1 - action_duration),
                                  (location_2, duration_2 - action_duration))
                    new_state = (new_acc, minutes_remaining - action_duration, open_valves.union(newly_opened_valves),
                                  new_agents)
                    new_state_h = (new_state[0], new_state[1], frozenset(new_state[2]), frozenset(new_state[3]))
                    # print(
                    #     f"(score {acc} -> {new_acc}), duration: {action_duration}, remaining: {minutes_remaining}, open: {new_state[2]} agents: {[a[0] for a in agents]}")
                    # print(f"   agent 0: to {location_1} in {duration_1}")
                    # print(f"   agent 1: to {location_2} in {duration_2}")
                    # print(f"   add to q: {new_state_h not in seen_states}, h: {h(neighbors_map, flow_map, new_state)}")
                    # print()
                    heuristic = h(neighbors_map, flow_map, new_state)
                    if minutes_remaining - action_duration > 0 and new_state_h not in seen_states and heuristic > max_flow:
                        seen_states.add(new_state_h)
                        heapq.heappush(q, (heuristic, new_state))
        print(len(q), max_flow)
    return max_flow


def task1():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")
    neighbors_map = defaultdict(set)
    flow_map = {}
    for line in data:
        line = line.split(" ")
        origin = line[1]
        flow = int(line[4].strip(";").split("=")[1])
        neighbors = [el.strip(",") for el in line[9:]]
        neighbors_map[origin].update(neighbors)
        flow_map[origin] = flow

    ans = search(neighbors_map, flow_map, "AA")
    print(ans)
    return ans


def task2():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")
    neighbors_map = defaultdict(set)
    flow_map = {}
    for line in data:
        line = line.split(" ")
        origin = line[1]
        flow = int(line[4].strip(";").split("=")[1])
        neighbors = [el.strip(",") for el in line[9:]]
        neighbors_map[origin].update(neighbors)
        flow_map[origin] = flow

    ans = search2(neighbors_map, flow_map, ["AA", "AA"])
    print(ans)
    return ans


# task1()
task2()
