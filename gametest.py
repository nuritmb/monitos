import time
import numpy as np

from abstractlevel.models import Game, MonkeySignal, MonkeyState, PredArray
from abstractlevel.simulation import Simulation

# Parameters
nturns = 100
npredators = 3
nsignals = 5
nstates = 7
nmonkeys = 100000
min_monkeys = 100
rep_rate = 1.2
mut_rate = 0.2

# Simulation

monkey_signals = []
for i in range(nsignals):
    monkey_signals.append(MonkeySignal(i))

monkey_states = []
for i in range(nstates):
    monkey_states.append(MonkeyState(i))

sp = np.random.rand(npredators)
sp = sp / np.sum(sp)
predarray = PredArray(
    array=np.random.rand(npredators, nstates),
    spawn_probabilities=sp)
predators = predarray.to_predator_list(
    state_list=monkey_states)

sim = Simulation(
    nmonkeys=nmonkeys,
    rep_rate=rep_rate,
    mut_prob=mut_rate,
    predator_dict={predators[i]: sp[i] for i in range(len(predators))},
    signal_list=monkey_signals,
    state_list=monkey_states,
    min_monkeys=min_monkeys,
    delete_only_elderly=False)

# Game

game = Game(
    nmonkeys=nmonkeys,
    nsignals=nsignals,
    nstates=nstates,
    predarray=predarray,
    rep_rate=rep_rate,
    mut_rate=mut_rate,
    min_monkeys=min_monkeys)

# Game simulation
t1 = time.time()
sim.run(100)
t2 = time.time()
print('Standard: {0:.0f} μs ({1:.6f} μs per monkey*turn)'.format(
    (t2 - t1) * (10**6),
    (t2 - t1) * (10**6) / (nmonkeys * nturns)
))

t1 = time.time()
game.run(100)
t2 = time.time()
print('Standard: {0:.0f} μs ({1:.6f} μs per monkey*turn)'.format(
    (t2 - t1) * (10**6),
    (t2 - t1) * (10**6) / (nmonkeys * nturns)
))
