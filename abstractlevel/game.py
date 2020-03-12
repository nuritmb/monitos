from typing import Dict
from models import MonkeySignal, MonkeyState, Monkey, Predator # if it doesn't run, add '.' right before models
from enum import Enum
import random

# GAME CONSTANTS

nmonkeys = 10000
nturns = 1000
reproduction_rate = 1.7
mutation_probability = 0.1

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
        monkeystates[0]: 1.0,
        monkeystates[1]: 0.9,
        monkeystates[2]: 0.9 
    },
    name="nothing"
)

eagle = Predator(
    menu={
        monkeystates[0]: 0.3,
        monkeystates[1]: 0.9,
        monkeystates[2]: 0.1
    },
    name="eagle"
)

snake = Predator(
    menu={
        monkeystates[0]: 0.3,
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
for i in range(nmonkeys):
    monkeylist.append(
        Monkey(
            predator_list=predators,
            signal_list=monkeyvocab,
            state_list=monkeystates))

def printmonkey(monkey, index="", indentlevel=0):
    index = str(index)
    indent = "    "*indentlevel
    print("%s--------------"%indent)
    print("%sJeff King %s" % (indent,index))
    print("%s--------------"%indent)
    print("%sMonkey Wordmap:"%indent)
    for pred, sig in monkey.wordmap.items():
        print("%s%s"%(indent, pred.name), " -> ", sig.value, " -> ", monkey.interpret(sig).value)
    print("%s--------------"%indent)
    print("%sMonkey Actionmap:"%indent)
    for sig, act in monkey.actionmap.items():
        print("%s%s"%(indent, sig.value), " -> ", act.value)
    print("%s--------------"%indent)


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
    print("witness:")
    printmonkey(witness, witness_i, indentlevel=1)
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

    print("%d monkeys killed" % (len(monkeylist)-len(newmonkeylist)))
    print("%d monkeys left" % len(newmonkeylist))
    monkeylist = newmonkeylist

    babymonkeys = []
    nbabymonkeys = int(len(newmonkeylist)*(reproduction_rate-1.0))
    for babymoney_i in range(nbabymonkeys):
        teacher = random.choice(monkeylist)
        baby = Monkey(wordmap=teacher.wordmap, actionmap=teacher.actionmap)
        if random.random() < mutation_probability:
            baby.random_wordmap(predator_list=predators, signal_list=monkeyvocab)
            baby.random_actionmap(signal_list=monkeyvocab, state_list=monkeystates)
        babymonkeys.append(baby)
    print("reproduction phase: %d monkeys created" % len(babymonkeys))
    monkeylist.extend(babymonkeys)
    print("new population: %d monkeys" % len(newmonkeylist))

    if len(monkeylist) > nmonkeys:
        exceed = len(monkeylist) - nmonkeys
        print("the monkey population has exceeded capacity")
        random.shuffle(monkeylist)
        monkeylist = monkeylist[:nmonkeys]
        print("%d monkeys have been eliminated by God."%exceed)

    print("--------------")

    if len(monkeylist) < 100:
        print("GAME OVER.")
        break

input('press ENTER')

print("")
print("################")
print("SURVIVORS")
print("################")
for i, monkey in enumerate(monkeylist[:100]):
    printmonkey(monkey, i)
    print("")