from util import *
from collections import *
import copy
from functools import reduce
from math import prod

day = 2


def task1():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")
    score = 0
    scores = { "X": 1, "Y": 2, "Z": 3}
    matches = {"X": "A", "Y": "B", "Z": "C"}
    wins_against = { "X": "C", "Y": "A", "Z": "B"}
    for line in data:
        [opponent, me] = line.split()
        score += scores[me]
        if matches[me] == opponent:
            score += 3
        if wins_against[me] == opponent:
            score += 6
    print(score)
    return score


def task2():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")
    score = 0
    outcomes = {"X": "lose", "Y": "draw", "Z": "win"}
    outcome_scores = {"lose": 0, "draw": 3, "win": 6}

    scores = { "rock": 1, "paper": 2, "scissors": 3}
    matches = {"A": "rock", "B": "paper", "C": "scissors", "X": "rock", "Y": "paper", "Z": "scissors"}
    wins_against = { "rock": "scissors", "paper": "rock", "scissors": "paper"}
    loses_against = {"rock": "paper", "scissors": "rock", "paper": "scissors"}
    for line in data:
        [opponent, outcome] = line.split()
        outcome = outcomes[outcome]
        score += outcome_scores[outcome]

        me = None
        opponent = matches[opponent]
        if outcome == "draw":
            me = opponent
        elif outcome == "win":
            me = loses_against[opponent]
        elif outcome == "lose":
            me = wins_against[opponent]
        score += scores[me]
    print(score)
    return score

task1()
task2()
