from typing import Dict
from abstractlevel.models import MonkeySays, MonkeySees, MonkeyHears, MonkeyDoes, Monkey, Predator
from enum import Enum

nmonkeys = 10000
nturns = 10000
eagleprob = 0.2
snakeprob = 0.2

monkeysays = MonkeySays([
    0,
    1,
    2
])

monkeysees = MonkeySees([
    0,
    1,
    2
])

monkeyhears = MonkeyHears(

)

class MonkeyStates(Enum):
    grass = 0
    burrow = 1
    tree = 2

class MonkeySignals(Enum):
    we = 0
    love = 1
    jeffking = 2

eagle = Predator(
    menu={
        MonkeyStates.grass: 0.7,
        MonkeyStates.burrow: 0.9,
        MonkeyStates.tree: 0.1
})

snake = Predator(
    menu={
        MonkeyStates.grass: 0.7,
        MonkeyStates.burrow: 0.1,
        MonkeyStates.tree: 0.9
})

class Simulation:
    
    def __init__(self, nmonkeys: int, nturns: int, predatorprobabilities: Dict[Predator, float], monkeystates: Enum, monkeysignals: Enum):
        self.nmonkeys = nmonkeys
        self.nturns = nturns
        self.predatorprobabilities = predatorprobabilities # TODO check probabilities
        self.monkeystates = monkeystates
        self.monkeysignals = monkeysignals

    def start_game(self):
