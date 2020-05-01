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
    rep_rate=1.2,
    mut_prob=0.2,
    predator_dict={predators[i]: sp[i] for i in range(len(predators))},
    signal_list=monkey_signals,
    state_list=monkey_states)
sim.create_monkeys()

# MonkeyArray

ma = MonkeyArray(
    npredators=npredators,
    nsignals=nsignals,
    nstates=nstates,
    nmonkeys=nmonkeys)

# Witnessing phase simulation
pred = sim.predator_list[random_predator]
t1 = time.time()
witness = sim.get_random_monkey()
message = witness.emmit(pred)
for monkey in sim.monkey_list:
    monkey.receive(message)
t2 = time.time()
print('Standard: {0:.0f} ms'.format((t2 - t1) * 1000000))

t1 = time.time()
ma.witness(random_predator)
t2 = time.time()
print('Vectorized: {0:.0f} ms'.format((t2 - t1) * 1000000))
