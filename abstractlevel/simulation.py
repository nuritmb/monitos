import copy
import random
import pandas as pd
import time

from typing import Dict, List, Tuple, Union
from enum import Enum

from models import MonkeySignal, MonkeyState, Monkey, Predator # if it doesn't run, add '.' right before models
from printer import print_sections


class Simulation:

    def __init__(
            self, nmonkeys: int, rep_rate: float, mut_prob: float, predator_dict: Dict[Predator, float],
            signal_list: List[MonkeySignal], state_list: List[MonkeyState], monkey_basename: str='Jeff King',
            delete_only_elderly: bool=True, archive_cicle: int=100, min_monkeys: int=1, archive_maps: bool=False) -> None:
        self.nmonkeys = nmonkeys
        self.rep_rate = rep_rate
        self.mut_prob = mut_prob
        self.predator_dict = self.normalize_pred_dict(predator_dict)
        self.predator_list = list(self.predator_dict)
        self.signal_list = signal_list
        self.state_list = state_list
        self.monkey_basename = monkey_basename
        self.delete_only_elderly = delete_only_elderly
        self.archive_cicle = archive_cicle
        self.min_monkeys = min_monkeys
        self.archive_maps = archive_maps
        self.predator_intervals = self.define_predator_intervals()
        self.monkey_list = []
        self.actionmap_count = {}
        self.wordmap_count = {}
        self.archives = []
        self.wordmap_count = self.initialize_wordmap_count()
        self.actionmap_count = self.initialize_actionmap_count()
        self.turn = 0

    def normalize_pred_dict(self, predator_dict: Dict[Predator, float]) -> Dict[Predator, float]:
        new_predator_dict = {}
        prob_sum = sum(predator_dict.values())
        for pred, prob in predator_dict.items():
            new_predator_dict[pred] = prob/prob_sum
        return new_predator_dict

    def define_predator_intervals(self) -> Dict[Tuple[float, float], Predator]:
        predator_intervals = {}
        left = 0.0
        for pred, prob in self.predator_dict.items():
            predator_intervals[(left, left+prob)] = pred
            left += prob
        return predator_intervals

    def initialize_wordmap_count(self) -> Dict[Predator, Dict[MonkeySignal, int]]:
        wordmap_count = {}
        for pred in self.predator_dict:
            wordmap_count[pred] = {}
            for sig in self.signal_list:
                wordmap_count[pred][sig] = 0
        return wordmap_count

    def initialize_actionmap_count(self) -> Dict[MonkeySignal, Dict[MonkeyState, int]]:
        actionmap_count = {}
        for sig in self.signal_list:
            actionmap_count[sig] = {}
            for act in self.state_list:
                actionmap_count[sig][act] = 0
        return actionmap_count

    def reset_game(self) -> None:
        self.monkey_list = []
        self.wordmap_count = self.initialize_wordmap_count()
        self.actionmap_count = self.initialize_actionmap_count()
        self.archives = []
        self.turn = 0

    def add_monkey_wordmap(self, monkey: Monkey) -> None:
        for pred, sig in monkey.wordmap.items():
            self.wordmap_count[pred][sig] += 1
    
    def add_monkey_actionmap(self, monkey: Monkey) -> None:
        for sig, act in monkey.actionmap.items():
            self.actionmap_count[sig][act] += 1

    def add_monkey_maps(self, monkey: Monkey) -> None:
        self.add_monkey_wordmap(monkey)
        self.add_monkey_actionmap(monkey)

    def delete_monkey_wordmap(self, monkey: Monkey) -> None:
        for pred, sig in monkey.wordmap.items():
                self.wordmap_count[pred][sig] -= 1

    def delete_monkey_actionmap(self, monkey: Monkey) -> None:
        for sig, act in monkey.actionmap.items():
                self.actionmap_count[sig][act] -= 1

    def delete_monkey_maps(self, monkey: Monkey) -> None:
        self.delete_monkey_wordmap(monkey)
        self.delete_monkey_actionmap(monkey)

    def get_wordmap_convention(self):
        wordmap_convention = {}
        for pred, sigcount in self.wordmap_count.items():
            convention = []
            maxcount = 0
            for sig, count in sigcount.items():
                if count > maxcount:
                    convention = [sig]
                elif count == maxcount:
                    convention.extend(sig)
            wordmap_convention[pred] = convention
        return wordmap_convention    

    def get_actionmap_convention(self):
        actionmap_convention = {}
        for sig, actcount in self.actionmap_count.items():
            convention = []
            maxcount = 0
            for act, count in actcount.items():
                if count > maxcount:
                    convention = [act]
                elif count == maxcount:
                    convention.extend(act)
            actionmap_convention[sig] = convention
        return actionmap_convention    


    def get_random_predator(self) -> Predator:
        p = random.random()
        for intv, pred in self.predator_intervals.items():
            uppercond = ((p < intv[1]) if intv[1] < 1.0 else (p <= intv[1]))
            if (intv[0] <= p) and uppercond:
                return pred
        raise ValueError('probability not within any interval')

    def get_random_monkey(self) -> Monkey:
        return random.choice(self.monkey_list)

    def create_monkeys(self, number: Union[int,None]=None, starting_number: Union[int,None]=None) -> None:
        number = self.nmonkeys if (number is None) else number
        starting_number = starting_number if starting_number else (len(self.monkey_list)+1)
        monkey_list = []
        for i in range(starting_number, starting_number+number):
            monkey = Monkey(
                name=self.monkey_basename+' '+str(i),
                predator_list=self.predator_list,
                signal_list=self.signal_list,
                state_list=self.state_list)
            monkey_list.append(monkey)
            self.add_monkey_maps(monkey)
        self.monkey_list.extend(monkey_list)

    def replication_phase(self, starting_number: Union[int,None]=None) -> None:
        t0 = time.time()
        starting_number = starting_number if starting_number else (len(self.monkey_list)+1)
        # Normal reproduction
        number__no_mutation = int(len(self.monkey_list)*(self.rep_rate-1.0)*(1.0-self.mut_prob))
        teachers  = random.choices(self.monkey_list, k=number__no_mutation)
        monkey_list__no_mutation = []
        i = starting_number
        for teacher in teachers:
            monkey = Monkey(
                name=self.monkey_basename+' '+str(i),
                wordmap=teacher.wordmap,
                actionmap=teacher.actionmap)
            monkey_list__no_mutation.append(monkey)
            self.add_monkey_maps(monkey)
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
                for monkey in self.monkey_list[:n_dead]:
                    self.delete_monkey_maps(monkey)
                self.monkey_list = self.monkey_list[n_dead:]
            else:
                random.shuffle(self.monkey_list)
                for monkey in self.monkey_list[self.nmonkeys:]:
                    self.delete_monkey_maps(monkey)
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

    def predator_phase(self) -> None:
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
            else:
                self.delete_monkey_maps(monkey)
        self.monkey_list = new_monkey_list
        t2 = time.time()
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
            if self.archive_maps:
                for pred, sigcount in self.wordmap_count.items():
                    for sig, count in sigcount.items():
                        self.archives[-1]['Wordmap {0} -> {1}'.format(pred, sig)] = count
                for sig, actcount in self.actionmap_count.items():
                    for act, count in actcount.items():
                        self.archives[-1]['Actionmap {0} -> {1}'.format(sig, act)] = count
            t3 = time.time()
            self.archives[-1]['Predator Phase Time (Witnessing)'] = t1 - t0
            self.archives[-1]['Predator Phase Time (Hunting)'] = t2 - t1
            self.archives[-1]['Predator Phase Time (Archiving)'] = t3 - t2

    def run_turn(self) -> None:
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
        print('TURNS: ', end='')
        self.create_monkeys()
        for i in range(1, nturns+1):
            (print(i, end='') if i==1 else print(', %d' % i, end=''))
            if len(self.monkey_list) < self.min_monkeys:
                print('  GAME OVER. There are less than %d monkeys' % self.min_monkeys)
                return
            self.run_turn()
        print('  GAME OVER. %d monkeys have survived.' % len(self.monkey_list))

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
            state_list[0]: 0.5,
            state_list[1]: 0.99,
            state_list[2]: 0.6
        },
        name='eagle'),
    Predator(
        menu={
            state_list[0]: 0.6,
            state_list[1]: 0.5,
            state_list[2]: 0.99
        },
        name='snake')]


game = Simulation(
    nmonkeys=100000,
    rep_rate=1.2,
    mut_prob=0.05,
    predator_dict={
        predators[0]:0.5,
        predators[1]:0.5},
    signal_list=signal_list,
    state_list=state_list,
    archive_cicle=1,
    min_monkeys=100,
    archive_maps=True)

print('')
print('RUNNING GAMES')
print('-'*30)
most_turns = 0
longest_game = None
for i in range(100):
    game.reset_game()
    game.run(1000000)
    if game.turn > most_turns:
        longest_game = copy.deepcopy(game)
        most_turns = game.turn
        print('RECORD HIGH! (%d turns)' % most_turns)
    if game.turn == 1000:
        print('MADE IT!')
        break
    print('')
print('-'*30)

print('WORDMAP CONVENTION:')
print(longest_game.get_wordmap_convention())

print('ACTIONMAP CONVENTION:')
print(longest_game.get_actionmap_convention())


df = pd.DataFrame(longest_game.archives)
df['Optimal State %'] = df['Optimal State Counter']/df['Monkey Population (Pre Predator)']
df.to_csv('archives.csv')

print('SUMMARY')
summary_list = ['Predator', 'Monkey Population (Pre Predator)', 'Message'] + [col for col in list(df.columns) if col.find('Monkey State Counter: ') != -1] + ['Average Survival Chance', 'Monkey Population (Post Predator)', 'Optimal State %']
summary = df[summary_list]
summary.to_csv('summary.csv')