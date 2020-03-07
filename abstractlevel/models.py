
from typing import List, Dict

class MonkeySays(List[str]):
    """Monkey's basic vocabulary

    :param statelist: list of words

    """
    def __init__(self, statelist: List[int]) -> None:
            self.statelist = statelist

class MonkeySees(List[int]):
    """Monkey's perceptive states with respect to predators ('seeing an eagle', 'seeing a snake', etc.)

    :param statelist: list of perceptive states
    
    """
    def __init__(self, statelist: List[int]) -> None:
            self.statelist = statelist

class MonkeyHears(List[int]):
    """Monkey's perceptive states with respect to signals from other monkeys

    :param statelist: list of perceptive states
    
    """
    def __init__(self, statelist: List[int]) -> None:
            self.statelist = statelist

class MonkeyDoes(List[int]):
    """Monkey's possible actions after hearing the message

    :param statelist: list of actions
    
    """
    def __init__(self, statelist: List[int]) -> None:
        self.statelist = statelist

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

    def emmit(self, perception: MonkeySees) -> MonkeySays:
        return self.wordmap[perception]

    def receive(self, perception: MonkeyHears) -> MonkeyDoes:
        return self.actionmap[perception]