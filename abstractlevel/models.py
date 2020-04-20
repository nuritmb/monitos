import numpy as np
import random

from typing import List, Dict, Any, Union

class MonkeySignal(int):
    '''An item of a monkey's vocabulary'''

    def __repr__(self) -> str:
        return 'Signal{:d}'.format(self)

    def __str__(self) -> str:
        return self.__repr__()


class MonkeyState(int):
    '''A possible action of a monkey upon hearing a message (e.g. hide in a bush)'''

    def __repr__(self) -> str:
        return 'State{:d}'.format(self)

    def __str__(self) -> str:
        return self.__repr__()


class Predator:
    '''A predator takes a monkey's state and outputs the monkey's survival probability

    :param menu: A map from a monkey's state to a monkey's survival chance
    
    '''
    def __init__(self, menu: Dict[MonkeyState, float], id: int = 0) -> None:
        self.id = id
        self.menu = menu
        self.survivalstates = self.calculatesurvivalstates()

    def calculatesurvivalstates(self) -> MonkeyState:
        '''Returns the best states for surviving the predator's attack'''
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
        '''Returns the survival propability of a given monkey state'''
        return self.menu[monkeystate]

    def survived(self, monkeystate: MonkeyState) -> bool:
        '''Returns true if the monkey in that state survived'''
        return (random.random() < self.surviveprobability(monkeystate))

    def __eq__(self, other) -> bool:
        return self.id.__eq__(other.id)

    def __hash__(self) -> int:
        return self.id

    def display(self, indentlevel: int=0) -> None:
        '''Displays the predator's stats'''
        indent = ' '*4*indentlevel
        print(indent+('-'*30))
        print(indent+'Predator({:d})'.format(self.id))
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
        return 'Predator{id:d}(menu={menu}, ss={ss})'.format(id=self.id, menu=menurepr, ss=self.survivalstates)

    def __str__(self) -> str:
        return 'Predator{:d}'.format(self.id)


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
    def __init__(self, id: int = 0, predator_list: List[Predator] = None, signal_list: List[MonkeySignal] = None,
                 state_list: List[MonkeyState] = None, wordmap: Dict[Predator, MonkeySignal] = None,
                 actionmap: Dict[MonkeySignal, MonkeyState] = None) -> None:
        self.id = id
        self.wordmap = (wordmap if wordmap else self.random_wordmap(predator_list, signal_list))
        self.actionmap = (actionmap if actionmap else self.random_actionmap(signal_list, state_list))
        self.state = None
 
    def random_wordmap(self, predator_list: List[Predator], signal_list: List[MonkeySignal]) -> None:
        '''Returns a random wordmap given a predator_list and a signal_list
        
        :param predator_list: list of predators
        :param signal_list: list of signals
        :returns: the wordmap linking each predator to a signal
        
        '''
        wordmap = dict()
        for predator in predator_list:
            wordmap[predator] = random.choice(signal_list)
        return wordmap

    def random_actionmap(self, signal_list: List[MonkeySignal], state_list: List[MonkeyState]) -> None:
        '''Returns a random actionmap given a signal_list and a state_list
        
        :param signal_list: list of signals
        :param state_list: list of states
        :returns: the actionmap linking each signal to a state
        
        '''
        actionmap = dict()
        for signal in signal_list:
            actionmap[signal] = random.choice(state_list)
        return actionmap

    def emmit(self, perception: Predator) -> None:
        '''Emmits the signal linked with the perceived predator

        :param perception: the perceived predator
        :returns: the emmited signal

        '''
        return self.wordmap[perception]

    def interpret(self, heardsignal: MonkeySignal) -> None:
        '''Returns the state linked to a heard signal
        
        :param heardsignal: the heard signal
        :returns: the state linked to the signal in actionmap

        '''
        return self.actionmap[heardsignal]

    def receive(self, heardsignal: MonkeySignal) -> None:
        '''Changes to the state linked to a heard signal
        
        :param heardsignal: the heard signal
        :returns: the state linked to the signal in actionmap

        '''
        self.state = self.interpret(heardsignal)

    def display(self, indentlevel=0):
        '''Displays the monkeys's stats'''
        indent = ' '*4*indentlevel
        print(indent+('-'*30))
        print(indent+'Monkey({:d})'.format(self.id))
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
        return 'Monkey{id:d}(wordmap={wordmap}, actionmap={actionmap}, state={state})'.format(
            id=self.id,
            wordmap=wordmaprepr,
            actionmap=actionmaprepr,
            state=self.state.__repr__()
        )

    def __str__(self):
        return 'Monkey{:d}'.format(self.id)


class PredArray(np.ndarray):
    '''A numpy array representing an array of predators

    This is a two-dimensional array of numbers in [0,1] in which the first dimension
    is the predator and the second dimension is the state. Thus, array[p,s] should
    be the probability of surviving against predator number p in state number s. The
    array can be created either by explicitly specifying the array, or by passing a
    list of predator and (optional) list of states

    :param array: an array of ones and zeros
    :param predator_list: a list of predators
    :param state_list:
    
    '''

    def __init__(
        self,
        array: List[List[List[int]]] = None,
        predator_list: List[Predator] = None,
        state_list: List[MonkeyState] = None) -> None:
        if array:
            # First method
            super().__init__(array)
        else:
            # Second method
            if not predator_list:
                raise ValueError('no array or list of predators was given')
            if not state_list:
                state_list = set()
                for predator in predator_list:
                    for state in predator.menu:
                        state_list.add(state)
                state_list = list(state_list)
            arr = np.ones((len(predator_list), len(state_list)))
            for i, predator in enumerate(predator_list):
                for j, state in enumerate(state_list):
                    arr[i,j] = predator.get(state, 1.0)
            self = arr
        if len(self.shape) != 2:
            raise ValueError('the array does not have the correct dimensions')

class MonkeyArray:
    '''Basically two numpy array representing an array of monkeys

    This are two three-dimensional arrays of 0s and 1s: wordarray and actionarray.
    We have wordarray[m, p, s] = 1 if the monkey number m emmits the signal number
    s when the predator number p is perceived and 0 otherwise and
    actionarray[m, s, a] = 1 if the monkey number m changes to state number a when
    the signal s is heard and 0 otherwise.

    The arrays can be created by either explicitly passing the array
    values or can be randomly initialized by passing the number of monkeys,
    predators, signals and states.

    :param wordarray: array representing the monkey's word behaviour
    :param actionarray: array representing the monkey's action behaviour
    :param nmonkeys: number of monkeys (form random initialization)
    :param npredators: number of predators (for random initialization)
    :param nsignals: number of signals (for random initialization)
    :param nstates: number of states (for random initialization)

    '''
    def __init__(
        self,
        wordarray: List[List[List[int]]] = None,
        actionarray: List[List[List[int]]] = None,
        npredators: int = None,
        nsignals: int = None,
        nstates: int = None,
        nmonkeys: int = None) -> None:
        if (wordarray is not None) and (actionarray is not None):
            # First method
            self.wordarray = wordarray if isinstance(wordarray, np.ndarray) else np.ndarray(wordarray)
            self.actionarray = actionarray if isinstance(actionarray, np.ndarray) else np.ndarray(actionarray)
        else:
            # Second method
            if (not npredators) or (npredators < 0):
                raise ValueError('no array or positive number of predators was given')
            if not nsignals or (nsignals < 0):
                raise ValueError('no array or positive number of signals was given')
            if not nstates or (nstates < 0):
                raise ValueError('no array or positive number of states was given')
            if not nmonkeys or (nmonkeys < 0):
                raise ValueError('no array or positive number of monkeys was given')
            # Builds arrays
            wordarrays = []
            actionarrays= []
            for m in range(nmonkeys):
                # Builds word array (1, #p, #s)
                wordarraylist = []
                for p in range(npredators):
                    wordarraylist.append(
                        np.append(np.zeros(nsignals-1), [1]))
                    wordarraylist[-1].sort() # TODO: check why this isn't working
                wordarrays.append(np.column_stack(wordarraylist, axis=0))
                # Builds action array (1, #s, #a)
                actionarraylist = []
                for s in range(nsignals):
                    actionarraylist.append(
                            np.append(np.zeros(nstates-1), [1]))
                    actionarraylist[-1].sort() # TODO: check why this isn't working
                actionarrays.append(np.column_stack(actionarraylist, axis=0))
            # Assign arrays
            self.wordarray = np.stack(wordarrays, axis=0)
            self.actionarray = np.stack(actionarrays, axis=0)
            