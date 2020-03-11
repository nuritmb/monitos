from typing import List, Dict

class MonkeySays:
    """Item of a monkey's basic vocabulary

    """
    def __init__(self, value):
        self.value = value

class MonkeySees:
    """A monkey's perceptive state with respect to predators (e.g. seeing an eagle)

    """
    def __init__(self, value):
        self.value = value

class MonkeyHears:
    """A Monkey's perceptive state with respect to signals from other monkeys (e.g. heard signal x)

    """
    def __init__(self, value):
        self.value = value

class MonkeyDoes:
    """A possible action of monkey upon hearing a message (e.g. hide in a bush)

    """
    def __init__(self, value):
        self.value = value

class Monkey:
    """Basically a monkey

    A monkey has a *wordmap* and an *actionmap*. A wordmap maps perceptions to (spoken) words
    and an actionmap maps (heard) words to actions. The first one determines what signal a
    monkey will use if it sees a predator and the second one determines what action a monkey
    will perform if it hears a signal.

    :param wordmap: map from perceptions to (spoken) words
    :param actionmap: map from (heard) words to actions

    """
    def __init__(self, wordmap: Dict[MonkeySees, MonkeySays], actionmap: Dict[MonkeyHears, MonkeyDoes]) -> None:
        self.wordmap = wordmap
        self.actionmap = actionmap
        self.state = None

    def emmit(self, perception: MonkeySees) -> MonkeySays:
        return self.wordmap[perception]

    def receive(self, heardsignal: MonkeyHears) -> None:
        self.state = self.actionmap[heardsignal]


class Predator:
    """A predator takes a monkey's state and output's the monkey's survival probability

    :param menu: A map from a monkey's state to a monkey's survival chance
    
    """
    def __init__(self, menu: Dict[MonkeyDoes, float]) -> None:
        self.menu = menu
        self.survivalstate = self.calculatesurvivalstate()

    def calculatesurvivalstate(self) -> MonkeyDoes:
        beststate = None
        bestchance = 0.0
        for monkeystate, chance in self.menu.items():
            if chance > bestchance:
                beststate = monkeystate
                bestchance = chance        
        return beststate

    def trytoeat(self, monkeystate: MonkeyDoes) -> float:
        return self.menu[monkeystate]

