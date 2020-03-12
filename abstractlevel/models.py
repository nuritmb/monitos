from typing import List, Dict
import random

class Item:
    """An Item

    """
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return ((self.value == other.value) and (type(self) == type(other)))

    def __hash__(self):
        return hash((self.value, type(self)))

class MonkeySignal(Item):
    """An item of a monkey's vocabulary

    """
    def __init__(self, value):
        super().__init__(value)

class MonkeyState(Item):
    """A possible action of monkey upon hearing a message (e.g. hide in a bush)

    """
    def __init__(self, value):
        super().__init__(value)


class Predator:
    """A predator takes a monkey's state and output's the monkey's survival probability

    :param menu: A map from a monkey's state to a monkey's survival chance
    
    """
    def __init__(self, menu: Dict[MonkeyState, float], name="") -> None:
        self.name = name
        self.menu = menu
        self.survivalstate = self.calculatesurvivalstate()

    def calculatesurvivalstate(self) -> MonkeyState:
        beststate = None
        bestchance = 0.0
        for monkeystate, chance in self.menu.items():
            if chance > bestchance:
                beststate = monkeystate
                bestchance = chance        
        return beststate

    def surviveprobability(self, monkeystate: MonkeyState) -> float:
        return self.menu[monkeystate]

    def survived(self, monkeystate: MonkeyState) -> bool:
        return (random.random() < self.surviveprobability(monkeystate))

class Monkey:
    """Basically a monkey

    A monkey has a *wordmap* and an *actionmap*. A wordmap maps perceptions to (spoken) words
    and an actionmap maps (heard) words to actions. The first one determines what signal a
    monkey will use if it sees a predator and the second one determines what action a monkey
    will perform if it hears a signal.

    :param predator_list: list of predators (for random initialization)
    :param signal_list: list of signals (for random initialization)
    :param state_list: list of states (for random initialization)
    :param wordmap: map from perceptions to (spoken) words
    :param actionmap: map from (heard) words to actions

    """
    def __init__(self, predator_list: List[Predator] = None, signal_list: List[MonkeySignal] = None, state_list: List[MonkeyState] = None, wordmap: Dict[Predator, MonkeySignal] = None, actionmap: Dict[MonkeySignal, MonkeyState] = None) -> None:
        self.wordmap = (wordmap if wordmap else self.random_wordmap(predator_list, signal_list))
        self.actionmap = (actionmap if actionmap else self.random_actionmap(signal_list, state_list))
        self.state = None
 
    def random_wordmap(self, predator_list: List[Predator], signal_list: List[MonkeySignal]) -> None:
        wordmap = dict()
        for predator in predator_list:
            wordmap[predator] = random.choice(signal_list)
        return wordmap

    def random_actionmap(self, signal_list: List[MonkeySignal], state_list: List[MonkeyState]) -> None:
        actionmap = dict()
        for signal in signal_list:
            actionmap[signal] = random.choice(state_list)
        return actionmap

    def emmit(self, perception: Predator) -> MonkeySignal:
        return self.wordmap[perception]

    def receive(self, heardsignal: MonkeySignal) -> None:
        self.state = self.actionmap[heardsignal]