import copy
import random
import pandas as pd
import time

from typing import Dict, List
from enum import Enum

from models import MonkeySignal, MonkeyState, Monkey, Predator # if it doesn't run, add '.' right before models
from printer import print_sections


class Simulation:

    def __init__(self, nmonkeys, rep_rate, mut_prob, predator_dict, signal_list, state_list, monkey_basename='Jeff King', delete_only_elderly=True, archive_cicle=100):
        self.nmonkeys = nmonkeys
        self.rep_rate = rep_rate
        self.mut_prob = mut_prob
        self.predator_dict = self.normalize_pred_dict(predator_dict)
        self.predator_intervals = self.define_predator_intervals()
        self.signal_list = signal_list
        self.state_list = state_list
        self.monkey_basename = monkey_basename
        self.delete_only_elderly = delete_only_elderly
        self.monkey_list = []
        self.archives = []
        self.wordmap_count = {}
        self.actionmap_count = {}
        self.archive_cicle = archive_cicle
        self.turn = 0

    def normalize_pred_dict(self, predator_dict):
        new_predator_dict = {}
        prob_sum = sum(predator_dict.values())
        for pred, prob in predator_dict.items():
            new_predator_dict[pred] = prob/prob_sum
        return new_predator_dict

    def define_predator_intervals(self):
        predator_intervals = {}
        left = 0.0
        for pred, prob in self.predator_dict.items():
            predator_intervals[(left, left+prob)] = pred
            left += prob
        return predator_intervals

    def get_random_predator(self):
        p = random.random()
        for intv, pred in self.predator_intervals.items():
            uppercond = ((p < intv[1]) if intv[1] < 1.0 else (p <= intv[1]))
            if (intv[0] <= p) and uppercond:
                return pred
        raise ValueError('probability not within any interval')

    @property
    def predators(self):
        return list(self.predator_dict)

    def get_random_monkey(self):
        return random.choice(self.monkey_list)

    def create_monkeys(self, number=None, starting_number=None):
        number = self.nmonkeys if (number is None) else number
        starting_number = starting_number if starting_number else (len(self.monkey_list)+1)
        monkey_list = []
        for i in range(starting_number, starting_number+number):
            monkey_list.append(
                Monkey(
                    name=self.monkey_basename+' '+str(i),
                    predator_list=self.predators,
                    signal_list=self.signal_list,
                    state_list=self.state_list))
        self.monkey_list.extend(monkey_list)

    def count_wordmaps(self):
        wordmap_count = {}
        for monkey in self.monkey_list:
            for pred, sig in monkey.wordmap.items():
                if (pred.name, sig) in wordmap_count:
                    wordmap_count[(pred.name, sig)] += 1
                else:
                    wordmap_count[(pred.name, sig)] = 1
        return wordmap_count

    def count_actionmaps(self):
        actionmap_count = {}
        for monkey in self.monkey_list:
            for sig, act in monkey.wordmap.items():
                if (sig, act) in actionmap_count:
                    actionmap_count[(sig, act)] += 1
                else:
                    actionmap_count[(sig, act)] = 1
        return actionmap_count

    def replication_phase(self, starting_number=None):
        t0 = time.time()
        starting_number = starting_number if starting_number else (len(self.monkey_list)+1)
        # Normal reproduction
        number__no_mutation = int(len(self.monkey_list)*(self.rep_rate-1.0)*(1.0-self.mut_prob))
        teachers  = random.choices(self.monkey_list, k=number__no_mutation)
        monkey_list__no_mutation = []
        i = starting_number
        for teacher in teachers:
            monkey_list__no_mutation.append(Monkey(
                name=self.monkey_basename+' '+str(i),
                wordmap=teacher.wordmap,
                actionmap=teacher.actionmap))
            i += 1
        self.monkey_list.extend(monkey_list__no_mutation)
        t1 = time.time()
        # Mutated reproduction
        number__mutation = int(len(self.monkey_list)*(self.rep_rate-1.0)*self.mut_prob)
        self.create_monkeys(number=number__mutation, starting_number=i)
        # Deleting Excess
        if len(self.monkey_list) > self.nmonkeys:
            excess = len(self.monkey_list) - self.nmonkeys
            if self.delete_only_elderly:
                n_dead = int(len(self.monkey_list) - self.nmonkeys)
                self.monkey_list = self.monkey_list[n_dead:] # TODO test
            else:
                random.shuffle(self.monkey_list)
                self.monkey_list = self.monkey_list[:self.nmonkeys]
        else:
            excess = None
        t2 = time.time()
        if (self.turn % self.archive_cicle) == 0:
            self.archives[-1]['Replication Stats (No Mutation)'] = len(monkey_list__no_mutation)
            self.archives[-1]['Replication Stats (Mutation)'] = number__mutation
            self.archives[-1]['Replication Stats (Excess)'] = excess
            self.archives[-1]['Replication Stats (Final Population)'] = len(self.monkey_list)
            t3 = time.time()
            self.archives[-1]['Replication Phase Time (No Mutation)'] = t1 - t0
            self.archives[-1]['Replication Phase Time (Mutation)'] = t2 - t1
            self.archives[-1]['Replication Phase Time (Archiving)'] = t3 - t2

    def predator_phase(self):
        t0 = time.time()
        initial_population = len(self.monkey_list)
        pred = self.get_random_predator()
        witness = self.get_random_monkey()
        message = witness.emmit(pred)
        t1 = time.time()
        monkey_state_counter = {}
        new_monkey_list = []
        for monkey in self.monkey_list:
            monkey.receive(message)
            if monkey.state in monkey_state_counter:
                monkey_state_counter[monkey.state] += 1
            else:
                monkey_state_counter[monkey.state] = 1
            if pred.survived(monkey.state):
                new_monkey_list.append(monkey)
        t2 = time.time()
        self.monkey_list = new_monkey_list
        if (self.turn % self.archive_cicle) == 0:
            self.archives[-1]['Message'] = message
            self.archives[-1]['Predator'] = pred
            self.archives[-1]['Average Survival Chance'] = 0
            self.archives[-1]['Optimal State Counter'] = 0
            for state, count in monkey_state_counter.items():
                self.archives[-1]['Monkey State Counter: %s' % state] = count
                self.archives[-1]['Average Survival Chance'] += count*pred.surviveprobability(state)
                if state in pred.survivalstates:
                    self.archives[-1]['Optimal State Counter'] += count
            self.archives[-1]['Average Survival Chance'] = self.archives[-1]['Average Survival Chance']/initial_population
            self.archives[-1]['Optimal Survival Chance'] = pred.surviveprobability(pred.survivalstates[0])
            self.archives[-1]['Monkey Population (Pre Predator)'] = initial_population
            self.archives[-1]['Monkey Population (Post Predator)'] = len(self.monkey_list)
            surviving_wordmaps = self.count_wordmaps()
            surviving_actionmaps = self.count_actionmaps()
            for (predname, sig), count in surviving_wordmaps.items():
                self.archives[-1]['Wordmap Predator({0}) -> {1}'.format(predname, sig)] = count
            for (sig, act), count in surviving_actionmaps.items():
                self.archives[-1]['Wordmap {0} -> {1}'.format(sig, act)] = count
            t3 = time.time()
            self.archives[-1]['Predator Phase Time (Witnessing)'] = t1 - t0
            self.archives[-1]['Predator Phase Time (Hunting)'] = t2 - t1
            self.archives[-1]['Predator Phase Time (Archiving)'] = t3 - t2

    def run_turn(self):
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

    def run(self, nturns):
        self.create_monkeys()
        for i in range(1, nturns+1):
            print('TURN %d' % i)
            if len(self.monkey_list) == 0:
                print('GAME OVER. All monkeys have been killed.')
                return
            self.run_turn()
        print('GAME OVER. %d monkeys have survived.' % len(self.monkey_list))

signal_list=[
    MonkeySignal('we'),
    MonkeySignal('love'),
    MonkeySignal('jeffking')]
state_list=[
    MonkeyState('grass'),
    MonkeyState('burrow'),
    MonkeyState('tree')]
predators = [
    Predator(
        menu={
            state_list[0]: 1.0,
            state_list[1]: 0.99,
            state_list[2]: 0.99
        },
        name='nothing'),
    Predator(
        menu={
            state_list[0]: 0.4,
            state_list[1]: 0.9,
            state_list[2]: 0.3
        },
        name='eagle'),
    Predator(
        menu={
            state_list[0]: 0.4,
            state_list[1]: 0.3,
            state_list[2]: 0.9
        },
        name='snake')]

game = Simulation(
    nmonkeys=10000,
    rep_rate=1.5,
    mut_prob=0.2,
    predator_dict={
        predators[0]:0.6,
        predators[1]:0.2,
        predators[2]:0.2},
    signal_list=signal_list,
    state_list=state_list
)

print('')
print('RUNNING GAME')
game.run(10000)

print('ARCHIVES')
df = pd.DataFrame(game.archives)
df.to_csv('archives.csv')
print(df)