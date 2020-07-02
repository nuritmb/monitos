import copy
import pandas as pd
import numpy as np

from abstractlevel.models import Game, PredArray

# Parameters
numgames = 100
maxturns = 1000
nmonkeys = 100000
nsignals = 7
nstates = 3
minmonkeys = 100

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
    min_monkeys=minmonkeys)

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
        print('MADE IT WITH %d MONKEYS! (bottleneck: %d monkeys in turn %d, bestmultiplier: %.4f, worstmultiplier: %.4f)' % (
            game.monkeyarray.nummonkeys,
            game.bottleneck,
            game.bottleneckturn,
            game.bestoverallturnmultiplier,
            game.worstoverallturnmultiplier))
    elif game.turns > bestgame.turns:
        print('RECORD HIGH OF %d TURNS! (bestmultiplier: %.4f, worstmultiplier: %.4f)' % (
            game.turns,
            game.bestoverallturnmultiplier,
            game.worstoverallturnmultiplier))
    else:
        print('%d TURNS. (bestmultiplier: %.4f, worstmultiplier: %.4f)' %(
            game.turns,
            game.bestoverallturnmultiplier,
            game.worstoverallturnmultiplier))
    if game.better(bestgame):
        bestgame = copy.deepcopy(game)
        bestgame.numgame = i+1

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
