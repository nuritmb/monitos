import os
import copy
import pandas as pd
import numpy as np

from abstractlevel.models import Game, PredArray

# CREATE GAME
#########################

# Settings
numgames = 1000
maxturns = 10**6
nmonkeys = 1000
nsignals = 7
nstates = 3
minmonkeys = 30
immortal = True
archive_cycle = 10**4
archive_loss = True

predarray = PredArray([
    #grass  #tree   #bush
    [0.7,   0.99,   0.6],   # snake
    [0.6,   0.7,    0.99],  # eagle
    [0.99,   0.6,    0.7]   # puma
])

game = Game(
    nmonkeys=nmonkeys,
    nsignals=nsignals,
    nstates=nstates,
    predarray=predarray,
    rep_rate=1.2,
    mut_rate=0.05,
    min_monkeys=minmonkeys,
    immortal=immortal,
    archive_cycle=archive_cycle,
    archive_loss=archive_loss)

# CREATE ARCHIVE
#########################

archive = pd.DataFrame(
    columns=[
        'Developed Stategy Convention',
        'Bottleneck',
        'Bottleneck Turn',
        'Worst Overall Turn Multiplier',
        'Best Overall Turn Multiplier',
        'Optimal Response Chance',
        'Losses',
    ]
)

if os.path.exists('archive.csv') and os.path.isfile('archive.csv'):
    csv = pd.read_csv('archive.csv')
    if (len(csv.columns) != len(archive.columns)) or (csv.columns != archive.columns).any():
        os.remove('archive.csv')
        archive.to_csv(
            'archive.csv',
            header=True,
            index=False,
            encoding='utf-8')
else:
    archive.to_csv(
        'archive.csv',
        header=True,
        index=False,
        encoding='utf-8')

# RUN GAMES
#########################

print('RUNNING GAMES')
print('-' * 30)
bestgame = None
for i in range(numgames):
    game.reset()
    print('GAME %d' % (i+1), end=': ')
    game.run(maxturns)
    bestgame = copy.deepcopy(game) if not bestgame else bestgame
    bestgame.numgame = i+1
    if game.monkeyswon:
        print('MADE IT WITH %d MONKEYS!\n(bottleneck: %d monkeys in turn %d, bestmultiplier: %.4f, worstmultiplier: %.4f)' % (
            game.monkeyarray.nummonkeys,
            game.bottleneck,
            game.bottleneckturn,
            game.bestoverallturnmultiplier,
            game.worstoverallturnmultiplier))
    elif game.turns > bestgame.turns:
        print('RECORD HIGH OF %d TURNS!\n(bestmultiplier: %.4f, worstmultiplier: %.4f)' % (
            game.turns,
            game.bestoverallturnmultiplier,
            game.worstoverallturnmultiplier))
    else:
        print('%d TURNS.\n(bestmultiplier: %.4f, worstmultiplier: %.4f)' %(
            game.turns,
            game.bestoverallturnmultiplier,
            game.worstoverallturnmultiplier))
    if game.better(bestgame):
        bestgame = copy.deepcopy(game)
        bestgame.numgame = i+1
    archive = pd.DataFrame({
        'Developed Stategy Convention': [game.learned],
        'Bottleneck': [game.bottleneck],
        'Bottleneck Turn': [game.bottleneckturn],
        'Worst Overall Turn Multiplier': [game.worstoverallturnmultiplier],
        'Best Overall Turn Multiplier': [game.bestoverallturnmultiplier],
        'Optimal Response Chance': [str(game.optimalchance)],
        'Losses': [game.losses],
    })

    archive.to_csv(
        'archive.csv',
        mode='a',
        header=False,
        index=False,
        encoding='utf-8')

np.set_printoptions(precision=2, suppress=True)

print('-' * 30)
print('BEST GAME: GAME {0}'.format(bestgame.numgame))
print('-' * 30)

print('WORDMAP COUNT:')
print(bestgame.wordcount)
print('')

print('WORDMAP PROBABILITIES:')
print(bestgame.wordchances)
print('')

print('WORDMAP CONVENTION:')
print(bestgame.wordconvention)
print('')

print('ACTIONMAP COUNT:')
print(bestgame.actioncount)
print('')

print('ACTIONMAP PROBABILITIES:')
print(bestgame.actionchances)
print('')

print('ACTIONMAP CONVENTION:')
print(bestgame.actionconvention)
print('')

print('OVERALL STRATEGY PROBABILITIES:')
print(bestgame.strategychance)
print('')

print('OVERALL STRATEGY CONVENTION')
print(bestgame.strategyconvention)
print('')

print('SURVIVAL CHANCE BY PREDATOR')
print(bestgame.survivalchances)
print('')

print('OVERALL SURVIVAL CHANCE')
print(bestgame.overallsurvivalchance)
print('')

print('OPTIMAL AGAINST')
print(bestgame.optimalagainst)
print('')
