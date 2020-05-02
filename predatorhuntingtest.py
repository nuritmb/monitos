import time
import numpy as np

from abstractlevel.models import MonkeyArray, MonkeySignal, MonkeyState, PredArray
from abstractlevel.simulation import Simulation

# Parameters
npredators = 3
nsignals = 5
nstates = 7
nmonkeys = 100000
random_predator = np.random.choice(npredators)

# Simulation Initialization

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
    rep_rate=1.2,
    mut_prob=0.2,
    predator_dict={predators[i]: sp[i] for i in range(len(predators))},
    signal_list=monkey_signals,
    state_list=monkey_states)
sim.create_monkeys()

# MonkeyArray Initialization

ma = MonkeyArray(
    npredators=npredators,
    nsignals=nsignals,
    nstates=nstates,
    nmonkeys=nmonkeys)

# Hunting phase simulation

pred = sim.predator_list[random_predator]
witness = sim.get_random_monkey()
message = witness.emmit(pred)
for monkey in sim.monkey_list:
    monkey.receive(message)
t1 = time.time()
new_monkey_list = []
for monkey in sim.monkey_list:
    monkey.receive(message)
    if pred.survived(monkey.state):
        new_monkey_list.append(monkey)
t2 = time.time()
print('Standard: {0:.0f} μs ({1:.2f} μs per monkey)'.format(
    (t2 - t1) * (10**6),
    (t2 - t1) * (10**6) / nmonkeys
))

monkeystatearray = ma.witness(random_predator)
t1 = time.time()
survived = predarray.hunt(random_predator, monkeystatearray)
ma.survive(survived)
t2 = time.time()
print('Vectorized: {0:.0f} μs ({1:.2f} μs per monkey)'.format(
    (t2 - t1) * (10**6),
    (t2 - t1) * (10**6) / nmonkeys
))
