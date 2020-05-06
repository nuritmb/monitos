import copy
import pandas as pd

from abstractlevel.models import Game, PredArray

# Parameters
numgames = 100
maxturns = 1000
nmonkeys = 100000
nsignals = 20
nstates = 3
minmonkeys = 100

predarray = PredArray([
    #grass  #tree   #bush
    [0.7,   0.99,   0.6],   # snake
    [0.7,   0.6,    0.99]   # eagle
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
mostturns = 0
longestgame = None
for i in range(numgames):
    game.reset()
    game.run(maxturns)
    if game.turns > mostturns:
        longestgame = copy.deepcopy(game)
        mostturns = game.turns
        print('RECORD HIGH! (%d turns in game %s)' % (mostturns, i+1))
    if game.turns == maxturns:
        print('MADE IT!')
        break
print('-' * 30)
print('LONGEST GAME')
print('-' * 30)

print('WORDMAP COUNT:')
print(longestgame.monkeyarray.wordcount)
print('')

print('WORDMAP PROBABILITIES:')
print(longestgame.monkeyarray.wordchances)
print('')

print('WORDMAP CONVENTION:')
print(longestgame.monkeyarray.wordconvention)
print('')

print('ACTIONMAP COUNT:')
print(longestgame.monkeyarray.actioncount)
print('')

print('ACTIONMAP PROBABILITIES:')
print(longestgame.monkeyarray.actionchances)
print('')

print('ACTIONMAP CONVENTION:')
print(longestgame.monkeyarray.actionconvention)
print('')

print('OVERALL STRATEGY PROBABILITIES:')
print(longestgame.monkeyarray.strategychance)
print('')

print('OVERALL STRATEGY CONVENTION')
print(longestgame.monkeyarray.strategyconvention)
print('')

print('SURVIVAL CHANCE BY PREDATOR')
print(longestgame.monkeyarray.survivalchances(longestgame.predarray))
print('')

print('OVERALL SURVIVAL CHANCE')
print(longestgame.monkeyarray.overallsurvivalchance(longestgame.predarray))
print('')

print('OPTIMAL AGAINST')
print(longestgame.monkeyarray.optimalagainst(longestgame.predarray))
print('')
