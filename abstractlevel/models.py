import numpy as np
import random
import time

from typing import Tuple, List, Dict, Any, Union

from .utilities import shuffle_along_axis

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
 
    def random_wordmap(self, predator_list: List[Predator], signal_list: List[MonkeySignal]) -> Dict[Predator, MonkeySignal]:
        '''Returns a random wordmap given a predator_list and a signal_list
        
        :param predator_list: list of predators
        :param signal_list: list of signals
        :returns: the wordmap linking each predator to a signal
        
        '''
        wordmap = dict()
        for predator in predator_list:
            wordmap[predator] = random.choice(signal_list)
        return wordmap

    def random_actionmap(self, signal_list: List[MonkeySignal], state_list: List[MonkeyState]) -> Dict[MonkeySignal, MonkeyState]:
        '''Returns a random actionmap given a signal_list and a state_list
        
        :param signal_list: list of signals
        :param state_list: list of states
        :returns: the actionmap linking each signal to a state
        
        '''
        actionmap = dict()
        for signal in signal_list:
            actionmap[signal] = random.choice(state_list)
        return actionmap

    def emmit(self, perception: Predator) -> MonkeySignal:
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


class PredArray:
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
        array: List[List[float]] = None,
        predator_list: List[Predator] = None,
        state_list: List[MonkeyState] = None) -> None:
        if array:
            # First method
            self.array = np.array(array)
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
                    arr[i,j] = predator.menu.get(state, 1.0)
            self.array = arr
        self.validate()
    
    def validate(self) -> None:
        if len(self.array.shape) != 2:
            raise ValueError('the array does not have the correct dimensions (m, n)! current dimensions are {0}'.format(self.shape))
        if np.amax(self.array) > 1.0:
            raise ValueError('the array has values grater than 1.0')
        if np.amin(self.array) < 0.0:
            raise ValueError('the array has values lower than than 1.0')

    @property
    def numpredators(self) -> int:
        return self.array.shape[0]

    @property
    def numstates(self) -> int:
        return self.array.shape[1]

    def to_predator_list(self, state_list=None) -> List[Predator]:
        if not state_list:
            state_list = []
            for i in range(self.numstates):
                state_list.append(MonkeyState(i))
        predator_list = []
        for p in range(self.numpredators):
            menu = dict()
            for s, state in enumerate(state_list):
                menu[state] = self.array[p,s]
            predator_list.append(Predator(menu, id=p))
        return predator_list


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
            # Assign arrays
            self.wordarray = shuffle_along_axis(np.concatenate((np.zeros((nmonkeys, npredators, nsignals-1)), np.ones((nmonkeys, npredators, 1))), axis=2), axis=2)
            self.actionarray = shuffle_along_axis(np.concatenate((np.zeros((nmonkeys, nsignals, nstates-1)), np.ones((nmonkeys, nsignals, 1))), axis=2), axis=2)
        # Validate data
        self.validate(nmonkeys=nmonkeys, npredators=npredators, nsignals=nsignals, nstates=nstates)

    def validate(self, nmonkeys: int, npredators: int, nsignals: int, nstates: int) -> None:
        if len(self.wordarray.shape) != 3:
            raise ValueError('wordarray must be a 3-dimensional matrix! (it is an array of shape %s)'%self.wordarray.shape)
        if not np.array_equal(np.sum(self.wordarray, axis=2), np.ones((nmonkeys, npredators))):
            raise ValueError('wordarray does not fulfill the uniqueness condition for a wordmap')
        if len(self.actionarray.shape) != 3:
            raise ValueError('actionarray must be a 3-dimensional matrix! (it is an array of shape %s)'%self.actionarray.shape)
        if not np.array_equal(np.sum(self.actionarray, axis=2), np.ones((nmonkeys, nsignals))):
            raise ValueError('actionarray does not fulfill the uniqueness condition for an actionmap')

    @property
    def shape(self) -> Tuple[Tuple[int]]:
        return (self.wordarray.shape, self.actionarray.shape)

    @property
    def pashape(self) -> Tuple[Tuple[Tuple[int]]]:
        wshape, ashape = self.shape
        return ((wshape[1], wshape[2]), (ashape[1], ashape[2]))

    @property
    def nummonkeys(self) -> int:
        return self.wordarray.shape[0]

    @property
    def numpredators(self) -> int:
        return self.wordarray.shape[1]

    @property
    def numsignals(self) -> int:
        return self.actionarray.shape[1]

    @property
    def numstates(self) -> int:
        return self.actionarray.shape[2]

    def concatenate(self, other: 'MonkeyArray') -> None:
        if type(other) is not type(self):
            raise TypeError('concatenated entity must be a MonkeyArray')
        if self.pashape != other.pashape:
            raise ValueError('the concatendated arrays must have the same predator-state shape! actual is {0}, concatenated is {1}'.format(
                self.shape,
                other.shape))
        self.wordarray = np.concatenate((self.wordarray, other.wordarray), axis=0)
        self.actionarray = np.concatenate((self.actionarray, other.actionarray), axis=0)

    def create_monkeys(self, number: int) -> None:
        added_monkeys = type(self)(
            npredators=self.numpredators,
            nsignals=self.numsignals,
            nstates=self.numstates,
            nmonkeys=number)
        self.concatenate(added_monkeys)

    def emmit(self, predator: int):
        return self.wordarray[:, predator, :]

    def interpret(self, heardsignal: int):
        return self.actionarray[:, heardsignal, :]

    def to_monkey_list(
        self,
        predator_list: List[Predator] = None,
        signal_list: List[MonkeySignal] = None,
        state_list: List[MonkeyState] = None) -> List[Monkey]:
        0 #TODO
