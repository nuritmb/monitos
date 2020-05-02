import time
import numpy as np

from abstractlevel.models import Predator, PredArray, MonkeyState

# Parameters
npredators = 1000
nstates = 7

# Initialization
monkey_states = []
for i in range(nstates):
    monkey_states.append(MonkeyState(i))

predator_matrix = np.random.rand(npredators, nstates)

t1 = time.time()
predator_list = []
for i, row in enumerate(predator_matrix):
    predator_list.append(Predator(
        menu={monkey_states[j]: row[j] for j in range(len(monkey_states))}
    ))
t2 = time.time()
print('Standard: {0:.0f} μs ({1:.2f} μs per predator)'.format(
    (t2 - t1) * (10**6),
    (t2 - t1) * (10**6) / npredators
))

t1 = time.time()
pa = PredArray(predator_matrix)
t2 = time.time()
print('Standard: {0:.0f} μs ({1:.2f} μs per predator)'.format(
    (t2 - t1) * (10**6),
    (t2 - t1) * (10**6) / npredators
))
