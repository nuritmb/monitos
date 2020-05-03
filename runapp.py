import copy
import pandas as pd

from abstractlevel.models import Game, PredArray

# Parameters
numgames = 100
maxturns = 1000
nmonkeys = 1000000
minmonkeys = 100

predarray = PredArray([
    [0.5,   0.99,   0.6],   # snake
    [0.6,   0.5,    0.99]   # eagle
])

game = Game(
    nmonkeys=nmonkeys,
    nsignals=3,
    nstates=3,
    predarray=predarray,
    rep_rate=1.2,
    mut_rate=0.05,
    min_monkeys=minmonkeys)

print('RUNNING GAMES')
print('-' * 30)
mostturns = 0
longestgame = None
for _ in range(numgames):
    game.reset()
    game.run(maxturns)
    if game.turns > mostturns:
        longestgame = copy.deepcopy(game)
        mostturns = game.turns
        print('RECORD HIGH! (%d turns)' % mostturns)
    if game.turns == maxturns:
        print('MADE IT!')
        break
    print('')
print('-' * 30)

print('WORDMAP COUNT:')
print(longestgame.monkeyarray.wordcount)

print('WORDMAP CONVENTION:')
print(longestgame.monkeyarray.wordconvention)

print('ACTIONMAP COUNT:')
print(longestgame.monkeyarray.actioncount)

print('ACTIONMAP CONVENTION:')
print(longestgame.monkeyarray.actionconvention)

print('PREDATOR CONVENTION')
print(longestgame.monkeyarray.predatorconvention)

print('OPTIMAL AGAINST')
print(longestgame.monkeyarray.optimalagainst(longestgame.predarray))