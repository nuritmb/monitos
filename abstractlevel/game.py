from typing import Dict
from models import MonkeySignal, MonkeyState, Monkey, Predator # if it doesn't run, add '.' right before models
from enum import Enum
import random

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
    },
    name="nothing"
)

eagle = Predator(
    menu={
        monkeystates[0]: 0.7,
        monkeystates[1]: 0.9,
        monkeystates[2]: 0.1
    },
    name="eagle"
)

snake = Predator(
    menu={
        monkeystates[0]: 0.7,
        monkeystates[1]: 0.1,
        monkeystates[2]: 0.9
    },
    name="snake"
)

predators = [
    nothing,
    eagle,
    snake
]

eagle_prob = 0.2
snake_prob = 0.2

# MONKEY CREATION

monkeylist = []
for i in range(100):
    monkeylist.append(
        Monkey(
            predator_list=predators,
            signal_list=monkeyvocab,
            state_list=monkeystates))

for i, monkey in enumerate(monkeylist):
    print("Jeff King %d" % i)
    print("--------------")
    print("Monkey Wordmap:")
    for pred, sig in monkey.wordmap.items():
        print(pred.name, " -> ", sig.value)
    print("")
    print("Monkey Actionmap:")
    for sig, act in monkey.actionmap.items():
        print(sig.value, " -> ", act.value)
    print("--------------")
    print("")


#############
# GAME START
#############

for turn in range(nturns):
    print("TURN %d" % turn)
    print("--------------")
    p = random.random()

    pred = nothing
    if p > 1.0 - eagle_prob:
        pred = eagle
    elif p < snake_prob:
        pred = snake
    print("predator:", pred.name)

    witness_i = random.choice(range(len(monkeylist)))
    witness = monkeylist[witness_i]
    msg = witness.emmit(pred)
    print("witness: monkey", witness_i)
    print("message:", msg.value)

    monkeystatecounter = {}
    newmonkeylist = []
    for monkey in monkeylist:
        # TODO: witness state change
        monkey.receive(msg)

        if monkey.state in monkeystatecounter:
            monkeystatecounter[monkey.state] += 1
        else:
            monkeystatecounter[monkey.state] = 0

        if pred.survived(monkey.state):
            newmonkeylist.append(monkey)

    print("state count:")
    for state, count in monkeystatecounter.items():
        print("    %d %s monkeys"%(count, state.value))
    print("")

    print("%d monkeys killed" % (len(monkeylist)-len(newmonkeylist)))
    print("%d monkeys left" % len(newmonkeylist))
    monkeylist = newmonkeylist
    print("--------------")

    if len(monkeylist) == 0:
        print("GAME OVER.")
        break