from typing import Dict
from models import MonkeySignal, MonkeyState, Monkey, Predator
from enum import Enum


# GAME CONSTANTS

nmonkeys = 10000
nturns = 10000

# MONKEY VOCABULARY AND STATES

monkeyvocab = [
    MonkeySignal('we'),
    MonkeySignal('love'),
    MonkeySignal('jeffking')
]

monkeystates = [
    MonkeyState('grass'),
    MonkeyState('burrow'),
    MonkeyState('tree')
]

# PREDATORS

nothing = Predator(
    menu={
        monkeystates[0]: 0.0,
        monkeystates[1]: 0.0,
        monkeystates[2]: 0.0 
    })

eagle = Predator(
    menu={
        monkeystates[0]: 0.7,
        monkeystates[1]: 0.9,
        monkeystates[2]: 0.1
})

snake = Predator(
    menu={
        monkeystates[0]: 0.7,
        monkeystates[1]: 0.1,
        monkeystates[2]: 0.9
})

predators = [
    nothing,
    eagle,
    snake
]

eagle_prob = 0.2
snake_prob = 0.2

#############
# GAME START
#############

# MONKEY CREATION

monkeylist = []
for i in range(10000):
    monkeylist.append(
        Monkey(
            predator_list=predators,
            signal_list=monkeyvocab,
            state_list=monkeystates))