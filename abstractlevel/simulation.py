import random
import pandas as pd
import time

from typing import Dict, List, Tuple, Union
from enum import Enum

# if it doesn't run, add '.' right before models
from .models import MonkeySignal, MonkeyState, Monkey, Predator
from .printer import print_sections


class Simulation:
    '''Class which contains paramaters for a simulation

    :param nmonkeys: initial and max number of monkeys
    :param rep_rate: rate of reprodiction
    :param mut_prob: chance of random mutation in a generated monkey
    :param predator_dict: dict of predators linked to their spawn probabilities
    :param signal_list: list of signals that a monkey can use
    :param state_list: list of states in which a monkey can be
    :param delete_only_elderly: if True, it will delete the oldest monkeys when adjusting for overpopulation
    :param archive_cicle: integer representing how many turns until the state of the game is archived
    :param min_monkeys: minimum number of monkeys for the game to continue
    :param archive_maps: if True, monkey maps are archived along with the gamestate

    '''

    def __init__(self,
                 nmonkeys: int,
                 rep_rate: float,
                 mut_prob: float,
                 predator_dict: Dict[Predator,
                                     float],
                 signal_list: List[MonkeySignal],
                 state_list: List[MonkeyState],
                 delete_only_elderly: bool = True,
                 archive_cicle: int = 100,
                 min_monkeys: int = 1,
                 archive_maps: bool = False) -> None:
        # Received parameters
        self.nmonkeys = nmonkeys
        self.rep_rate = rep_rate
        self.mut_prob = mut_prob
        self.predator_dict = self.normalize_pred_dict(predator_dict)
        self.signal_list = signal_list
        self.state_list = state_list
        self.delete_only_elderly = delete_only_elderly
        self.archive_cicle = archive_cicle
        self.min_monkeys = min_monkeys
        self.archive_maps = archive_maps
        # Calculated parameters
        self.predator_list = list(self.predator_dict)
        self.predator_intervals = self.define_predator_intervals()
        self.monkey_list = []
        self.actionmap_count = self.initialize_actionmap_count()
        self.wordmap_count = self.initialize_wordmap_count()
        self.archives = []
        self.turn = 0

    def normalize_pred_dict(
            self, predator_dict: Dict[Predator, float]) -> Dict[Predator, float]:
        '''Makes sure that the spawn probabilities in predator_dict sum up to 1

        :param predator_dict: dictionary with predators as keys and spawn probabilities as values
        :returns: predator dictionary with normalized probabilities

        '''
        new_predator_dict = {}
        prob_sum = sum(predator_dict.values())
        for pred, prob in predator_dict.items():
            new_predator_dict[pred] = prob / prob_sum
        return new_predator_dict

    def define_predator_intervals(self) -> Dict[Tuple[float, float], Predator]:
        '''Defines intervals related to predator_dict with a random dart throw

        :returns: partition of [0;1] into intervals, with each piece linked to a predator

        '''
        predator_intervals = {}
        left = 0.0
        for pred, prob in self.predator_dict.items():
            predator_intervals[(left, left + prob)] = pred
            left += prob
        return predator_intervals

    def initialize_wordmap_count(
            self) -> Dict[Predator, Dict[MonkeySignal, int]]:
        '''Initialized the wordmap_count to 0

        :returns: wordmap_count with all signals set to 0 for each predator

        '''
        wordmap_count = {}
        for pred in self.predator_dict:
            wordmap_count[pred] = {}
            for sig in self.signal_list:
                wordmap_count[pred][sig] = 0
        return wordmap_count

    def initialize_actionmap_count(
            self) -> Dict[MonkeySignal, Dict[MonkeyState, int]]:
        '''Initialized the actionmap_count to 0

        :returns: actionmap_count with all actions set to 0 for each signal

        '''
        actionmap_count = {}
        for sig in self.signal_list:
            actionmap_count[sig] = {}
            for act in self.state_list:
                actionmap_count[sig][act] = 0
        return actionmap_count

    def reset_game(self) -> None:
        '''Resets the game to its original state'''
        self.monkey_list = []
        self.wordmap_count = self.initialize_wordmap_count()
        self.actionmap_count = self.initialize_actionmap_count()
        self.archives = []
        self.turn = 0

    def add_monkey_wordmap(self, monkey: Monkey) -> None:
        '''Adds the wordmap of a particular monkey to the wordmap_count parameter

        :param monkey: monkey whose wordmap is to be added to the general count

        '''
        for pred, sig in monkey.wordmap.items():
            self.wordmap_count[pred][sig] += 1

    def add_monkey_actionmap(self, monkey: Monkey) -> None:
        '''Adds the actionmap of a particular monkey to the actionmap_count parameter

        :param monkey: monkey whose actionmap is to be added to the general count

        '''
        for sig, act in monkey.actionmap.items():
            self.actionmap_count[sig][act] += 1

    def add_monkey_maps(self, monkey: Monkey) -> None:
        '''Adds the wordmap and actionap of a particular monkey to the wordmap_count and actionmap_count parameters

        :param monkey: monkey whose maps are to be added to the general count

        '''
        self.add_monkey_wordmap(monkey)
        self.add_monkey_actionmap(monkey)

    def delete_monkey_wordmap(self, monkey: Monkey) -> None:
        '''Substracts the wordmap of a particular monkey to the wordmap_count parameter

        :param monkey: monkey whose wordmap is to be substracted to the general count

        '''
        for pred, sig in monkey.wordmap.items():
            self.wordmap_count[pred][sig] -= 1

    def delete_monkey_actionmap(self, monkey: Monkey) -> None:
        '''Substracts the actionmap of a particular monkey to the actionmap_count parameter

        :param monkey: monkey whose actionmap is to be substracted to the general count

        '''
        for sig, act in monkey.actionmap.items():
            self.actionmap_count[sig][act] -= 1

    def delete_monkey_maps(self, monkey: Monkey) -> None:
        '''Substracts the wordmap and actionap of a particular monkey to the wordmap_count and actionmap_count parameters

        :param monkey: monkey whose maps are to be substracted to the general count

        '''
        self.delete_monkey_wordmap(monkey)
        self.delete_monkey_actionmap(monkey)

    def get_wordmap_convention(self) -> Dict[Predator, MonkeySignal]:
        '''Gets the wordmap convention from the general count in wordmap_count

        :returns: word convention for each predator

        '''
        wordmap_convention = {}
        for pred, sigcount in self.wordmap_count.items():
            convention = []
            maxcount = 0
            for sig, count in sigcount.items():
                if count > maxcount:
                    convention = [sig]
                elif count == maxcount:
                    convention.append(sig)
            wordmap_convention[pred] = convention
        return wordmap_convention

    def get_actionmap_convention(self) -> Dict[MonkeySignal, MonkeyState]:
        '''Gets the actionmap convention from the general count in actionmap_count

        :returns: action convention for each word

        '''
        actionmap_convention = {}
        for sig, actcount in self.actionmap_count.items():
            convention = []
            maxcount = 0
            for act, count in actcount.items():
                if count > maxcount:
                    convention = [act]
                elif count == maxcount:
                    convention.append(act)
            actionmap_convention[sig] = convention
        return actionmap_convention

    def get_random_predator(self) -> Predator:
        '''Gets a random predator with the probability distribution in predator_intervals

        :returns: random predator

        '''
        p = random.random()
        for intv, pred in self.predator_intervals.items():
            uppercond = ((p < intv[1]) if intv[1] < 1.0 else (p <= intv[1]))
            if (intv[0] <= p) and uppercond:
                return pred
        raise ValueError('probability not within any interval')

    def get_random_monkey(self) -> Monkey:
        '''Gets a random monkey from monkey_list

        :returns: random monkey

        '''
        return random.choice(self.monkey_list)

    def create_monkeys(self,
                       number: Union[int,
                                     None] = None,
                       starting_number: Union[int,
                                              None] = None) -> None:
        '''Create the number of monkeys specified numbers (default is self.nmonkeys)

        :param number: number of monkeys to be created
        :param starting_number: starting number for automatic id assingment

        '''
        number = self.nmonkeys if (number is None) else number
        starting_number = starting_number if starting_number else (
            len(self.monkey_list) + 1)
        monkey_list = []
        for i in range(starting_number, starting_number + number):
            monkey = Monkey(
                id=i,
                predator_list=self.predator_list,
                signal_list=self.signal_list,
                state_list=self.state_list)
            monkey_list.append(monkey)
            if self.archive_maps:
                self.add_monkey_maps(monkey)
        self.monkey_list.extend(monkey_list)

    def replication_phase(self,
                          starting_number: Union[int,
                                                 None] = None) -> None:
        '''Simulates the replication phase in a turn

        :param starting_number: number for automatic id assignment

        '''
        t0 = time.time()
        counting_time = 0.0
        starting_number = starting_number if starting_number else (
            len(self.monkey_list) + 1)
        # Normal reproduction
        number__no_mutation = int(
            len(self.monkey_list) * (self.rep_rate - 1.0) * (1.0 - self.mut_prob))
        teachers = random.choices(self.monkey_list, k=number__no_mutation)
        monkey_list__no_mutation = []
        i = starting_number
        for teacher in teachers:
            monkey = Monkey(
                id=i,
                wordmap=teacher.wordmap,
                actionmap=teacher.actionmap)
            monkey_list__no_mutation.append(monkey)
            if self.archive_maps:
                t0c = time.time()
                self.add_monkey_maps(monkey)
                counting_time += time.time() - t0c
            i += 1
        self.monkey_list.extend(monkey_list__no_mutation)
        t1 = time.time()
        # Mutated reproduction
        number__mutation = int(len(self.monkey_list) *
                               (self.rep_rate - 1.0) * self.mut_prob)
        self.create_monkeys(number=number__mutation, starting_number=i)
        # Deleting Excess
        if len(self.monkey_list) > self.nmonkeys:
            excess = len(self.monkey_list) - self.nmonkeys
            if self.delete_only_elderly:
                n_dead = int(len(self.monkey_list) - self.nmonkeys)
                for monkey in self.monkey_list[:n_dead]:
                    if self.archive_maps:
                        t0c = time.time()
                        self.delete_monkey_maps(monkey)
                        counting_time += time.time() - t0c
                self.monkey_list = self.monkey_list[n_dead:]
            else:
                random.shuffle(self.monkey_list)
                for monkey in self.monkey_list[self.nmonkeys:]:
                    if self.archive_maps:
                        t0c = time.time()
                        self.delete_monkey_maps(monkey)
                        counting_time += time.time() - t0c
                self.monkey_list = self.monkey_list[:self.nmonkeys]
        else:
            excess = None
        t2 = time.time()
        if (self.turn % self.archive_cicle) == 0:
            self.archives[-1]['Replication Stats (No Mutation)'] = len(
                monkey_list__no_mutation)
            self.archives[-1]['Replication Stats (Mutation)'] = number__mutation
            self.archives[-1]['Replication Stats (Excess)'] = excess
            self.archives[-1]['Replication Stats (Final Population)'] = len(
                self.monkey_list)
            self.archives[-1]['Replication Phase Time (No Mutation+C)'] = t1 - t0
            self.archives[-1]['Replication Phase Time (Mutation+C)'] = t2 - t1
            self.archives[-1]['Replication Phase Time (Counting)'] = counting_time
            self.archives[-1]['Replication Phase Time (Archiving)'] = time.time(
            ) - t2

    def predator_phase(self) -> None:
        '''Simulates the predator phase in a turn'''
        t0 = time.time()
        # Witnessing Phase
        counting_time = 0.0
        initial_population = len(self.monkey_list)
        pred = self.get_random_predator()
        witness = self.get_random_monkey()
        message = witness.emmit(pred)
        t1 = time.time()
        # Hunting Phase
        monkey_state_counter = {}
        for state in self.state_list:
            monkey_state_counter[state] = 0
        new_monkey_list = []
        for monkey in self.monkey_list:
            monkey.receive(message)
            monkey_state_counter[monkey.state] += 1
            if pred.survived(monkey.state):
                new_monkey_list.append(monkey)
            else:
                if self.archive_maps:
                    t0c = time.time()
                    self.delete_monkey_maps(monkey)
                    counting_time += time.time() - t0c
        self.monkey_list = new_monkey_list
        t2 = time.time()
        # Archiving Phase
        if (self.turn % self.archive_cicle) == 0:
            self.archives[-1]['Message'] = message
            self.archives[-1]['Predator'] = pred
            self.archives[-1]['Average Survival Chance'] = 0
            self.archives[-1]['Optimal State Counter'] = 0
            for state, count in monkey_state_counter.items():
                self.archives[-1]['Monkey State Counter: %s' % state] = count
                self.archives[-1]['Average Survival Chance'] += count * \
                    pred.surviveprobability(state)
                if state in pred.survivalstates:
                    self.archives[-1]['Optimal State Counter'] += count
            self.archives[-1]['Average Survival Chance'] = self.archives[-1]['Average Survival Chance'] / initial_population
            self.archives[-1]['Optimal Survival Chance'] = pred.surviveprobability(
                pred.survivalstates[0])
            self.archives[-1]['Monkey Population (Pre Predator)'] = initial_population
            self.archives[-1]['Monkey Population (Post Predator)'] = len(
                self.monkey_list)
            if self.archive_maps:
                for pred, sigcount in self.wordmap_count.items():
                    for sig, count in sigcount.items():
                        self.archives[-1]['Wordmap {0} -> {1}'.format(
                            pred, sig)] = count
                for sig, actcount in self.actionmap_count.items():
                    for act, count in actcount.items():
                        self.archives[-1]['Actionmap {0} -> {1}'.format(
                            sig, act)] = count
            self.archives[-1]['Predator Phase Time (Witnessing)'] = t1 - t0
            self.archives[-1]['Predator Phase Time (Hunting+C)'] = t2 - t1
            self.archives[-1]['Predator Phase Time (Counting)'] = counting_time
            self.archives[-1]['Predator Phase Time (Archiving)'] = time.time() - t2

    def run_turn(self) -> None:
        '''Runs a turn which consists in the predator and the replication phase'''
        t0 = time.time()
        if (self.turn % self.archive_cicle) == 0:
            self.archives.append({})
        self.predator_phase()
        t1 = time.time()
        self.replication_phase()
        t2 = time.time()
        if (self.turn % self.archive_cicle) == 0:
            self.archives[-1]['Turn'] = self.turn
            self.archives[-1]['Predator Phase Time'] = t1 - t0
            self.archives[-1]['Replication Phase Time'] = t2 - t1
        self.turn += 1

    def run(self, nturns: int) -> None:
        '''Runs the game which forcefully ends after *nturns* turns or when less than min_monkeys remain

        :param nturns: maximum number of turns until forceful termination of the game

        '''
        print('Creating monkeys...', end=' ')
        t0 = time.time()
        self.create_monkeys()
        t1 = time.time()
        print('Game started ({time:.4f}s, {timepm:.0f}μs/monkey).'.format(
            time=(t1 - t0), timepm=1000000 * (t1 - t0) / self.nmonkeys))
        for i in range(1, nturns + 1):
            if len(self.monkey_list) < self.min_monkeys:
                t1 = time.time()
                gameduration = t1 - t0
                print(
                    'There are less than {nmonk:d} monkeys. Game ended in {nturns:d} turns. Duration: {dur:.4f} ({durpt:.0f} ms per turn)'.format(
                        nmonk=self.min_monkeys,
                        nturns=i,
                        dur=gameduration,
                        durpt=1000 *
                        gameduration /
                        i))
                return
            self.run_turn()
        t1 = time.time()
        gameduration = t1 - t0
        print(
            'All turns {nturns:d} have passed. Game ended with {nmonk:d} monkeys. Duration: {dur:.4f} ({durpt:.0f} ms per turn)'.format(
                nturns=i,
                nmonk=len(
                    self.monkey_list),
                dur=gameduration,
                durpt=1000 *
                gameduration /
                i))
