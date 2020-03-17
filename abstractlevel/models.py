from typing import List, Dict, Any
import random

class Item:
    '''An Item

    '''
    def __init__(self, value: Any) -> None:
        self.value = value

    def __eq__(self, other) -> bool:
        return ((self.value == other.value) and (type(self) == type(other)))

    def __hash__(self) -> int:
        return hash((self.value, type(self)))

class MonkeySignal(Item):
    '''An item of a monkey's vocabulary

    '''
    def __init__(self, value: Any) -> None:
        super().__init__(value)

    def __repr__(self) -> str:
        return 'Signal({value})'.format(value=self.value)

    def __str__(self) -> str:
        return self.__repr__()

class MonkeyState(Item):
    '''A possible action of monkey upon hearing a message (e.g. hide in a bush)

    '''
    def __init__(self, value: Any) -> None:
        super().__init__(value)

    def __repr__(self) -> str:
        return 'State({value})'.format(value=self.value)

    def __str__(self) -> str:
        return self.__repr__()

class Predator:
    '''A predator takes a monkey's state and output's the monkey's survival probability

    :param menu: A map from a monkey's state to a monkey's survival chance
    
    '''
    def __init__(self, menu: Dict[MonkeyState, float], name: str='') -> None:
        self.name = name
        self.menu = menu
        self.survivalstates = self.calculatesurvivalstates()

    def calculatesurvivalstates(self) -> MonkeyState:
        beststates = []
        bestchance = -1.0
        for monkeystate, chance in self.menu.items():
            if chance > bestchance:
                beststates = [monkeystate]
                bestchance = chance
            elif chance == bestchance:
                beststates.append(monkeystate)
                bestchance = chance 
        return beststates

    def surviveprobability(self, monkeystate: MonkeyState) -> float:
        return self.menu[monkeystate]

    def survived(self, monkeystate: MonkeyState) -> bool:
        return (random.random() < self.surviveprobability(monkeystate))

    def __eq__(self, other) -> bool:
        return (self.name == other.name) and (self.menu == other.menu)

    def __hash__(self) -> int:
        return hash((self.name, frozenset(self.menu.items())))

    def display(self, indentlevel: int=0) -> None:
        indent = ' '*4*indentlevel
        print(indent+('-'*30))
        print(indent+self.name)
        print(indent+('-'*30))
        print(indent+'Survival Chances:')
        for state, prob in self.menu.items():
            print(indent+'{0}: {1:.2f} %'.format(state, 100.0*prob))
        print(indent+('-'*30))
        print(indent+'Best States:')
        for state in self.survivalstates:
            print(indent+state.__str__())
        print(indent+('-'*30))

    def __repr__(self) -> str:
        menurepr = []
        for state, prob in self.menu.items():
            menurepr.append('{0}:{1:.4f}'.format(state.__repr__(), prob))
        menurepr = '{' + (', '.join(menurepr)) + '}'
        return 'Predator({name}, menu={menu}, ss={ss})'.format(name=self.name, menu=menurepr, ss=self.survivalstates)

    def __str__(self) -> str:
        return 'Predator({})'.format(self.name)


class Monkey:
    '''Basically a monkey

    A monkey has a *wordmap* and an *actionmap*. A wordmap maps perceptions to (spoken) words
    and an actionmap maps (heard) words to actions. The first one determines what signal a
    monkey will use if it sees a predator and the second one determines what action a monkey
    will perform if it hears a signal.

    :param predator_list: list of predators (for random initialization)
    :param signal_list: list of signals (for random initialization)
    :param state_list: list of states (for random initialization)
    :param wordmap: map from perceptions to (spoken) words
    :param actionmap: map from (heard) words to actions

    '''
    def __init__(self, name='Jeff King', predator_list: List[Predator] = None, signal_list: List[MonkeySignal] = None, state_list: List[MonkeyState] = None, wordmap: Dict[Predator, MonkeySignal] = None, actionmap: Dict[MonkeySignal, MonkeyState] = None) -> None:
        self.name = name
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

    def interpret(self, heardsignal: MonkeySignal) -> None:
        return self.actionmap[heardsignal]

    def receive(self, heardsignal: MonkeySignal) -> None:
        self.state = self.interpret(heardsignal)

    def display(self, indentlevel=0):
        indent = ' '*4*indentlevel
        print(indent+('-'*30))
        print(indent+self.name)
        print(indent+('-'*30))
        print(indent+'Monkey Wordmap:')
        for pred, sig in self.wordmap.items():
            print(indent+pred.__str__()+' -> '+sig.__str__()+' -> '+self.interpret(sig).__str__())
        print(indent+('-'*30))
        print(indent+'Monkey Actionmap:')
        for sig, act in self.actionmap.items():
            print(indent+sig.__str__()+' -> '+act.__str__())
        print(indent+('-'*30))

    def __repr__(self):
        wordmaprepr = []
        for pred, sig in self.wordmap.items():
            wordmaprepr.append('{0}:{1}'.format(pred.__repr__(), sig.__repr__()))
        wordmaprepr = '{' + (', '.join(wordmaprepr)) + '}'
        actionmaprepr = []
        for sig, act in self.actionmap.items():
            actionmaprepr.append('{0}:{1}'.format(sig.__repr__(), act.__repr__()))
        actionmaprepr = '{' + (', '.join(actionmaprepr)) + '}'
        return 'Monkey(name={name}, wordmap={wordmap}, actionmap={actionmap}, state={state})'.format(
            name=self.name,
            wordmap=wordmaprepr,
            actionmap=actionmaprepr,
            state=self.state.__repr__()
        )

    def __str__(self):
        return 'Monkey({})'.format(self.name)