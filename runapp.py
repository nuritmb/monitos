import copy
import pandas as pd

from abstractlevel.simulation import Simulation
from abstractlevel.models import MonkeySignal, MonkeyState, Predator

signal_list = [
    MonkeySignal(1),
    MonkeySignal(2),
    MonkeySignal(3)]
state_list = [
    MonkeyState(1),  # grass
    MonkeyState(2),  # tree
    MonkeyState(3)]  # burrow
predators = [
    Predator(
        id=2,  # snake
        menu={
            state_list[0]: 0.5,
            state_list[1]: 0.99,
            state_list[2]: 0.6
        }),
    Predator(
        id=3,  # eagle
        menu={
            state_list[0]: 0.6,
            state_list[1]: 0.5,
            state_list[2]: 0.99
        })]


game = Simulation(
    nmonkeys=1000000,
    rep_rate=1.2,
    mut_prob=0.05,
    predator_dict={
        predators[0]: 0.5,
        predators[1]: 0.5},
    signal_list=signal_list,
    state_list=state_list,
    archive_cicle=1,
    min_monkeys=100,
    archive_maps=False)

print('')
print('RUNNING GAMES')
print('-' * 30)
most_turns = 0
longest_game = None
for i in range(1):
    game.reset_game()
    game.run(1000)
    if game.turn > most_turns:
        longest_game = copy.deepcopy(game)
        most_turns = game.turn
        print('RECORD HIGH! (%d turns)' % most_turns)
    if game.turn == 1000:
        print('MADE IT!')
        break
    print('')
print('-' * 30)

print('WORDMAP CONVENTION:')
print(longest_game.get_wordmap_convention())

print('ACTIONMAP CONVENTION:')
print(longest_game.get_actionmap_convention())


df = pd.DataFrame(longest_game.archives)
df['Optimal State %'] = df['Optimal State Counter'] / \
    df['Monkey Population (Pre Predator)']
df.loc['Average (ms)'] = df.mean() * 1000
df.to_csv('archives.csv')

print('Average turn time (ns) / Average monkey population')
avg = df.loc['Average (ms)', :]
avg.name = 'Average (ns)'
avg = (1000000 * avg / avg['Monkey Population (Pre Predator)'])
avg = avg[[col for col, _ in avg.items() if col.find('Time') != -1]]
avg = avg.apply(lambda x: '{:.4f} ns / monkey'.format(x))
print(avg)

print('SUMMARY')
summary_list = [
    'Predator',
    'Monkey Population (Pre Predator)',
    'Message'] + [
        col for col in list(
            df.columns) if col.find('Monkey State Counter: ') != -1] + [
                'Average Survival Chance',
                'Monkey Population (Post Predator)',
    'Optimal State %']
summary = df[summary_list]
summary.to_csv('summary.csv')
