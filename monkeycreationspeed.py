import time

from abstractlevel.models import Monkey, MonkeySignal, MonkeyState, MonkeyArray, Predator
from abstractlevel.simulation import Simulation

# Parameters
nmonkeys = 1000000

# Initialization

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

sim = Simulation(
    nmonkeys=nmonkeys,
    rep_rate=1.2,
    mut_prob=0.05,
    predator_dict={
        predators[0]: 0.5,
        predators[1]: 0.5},
    signal_list=signal_list,
    state_list=state_list,
    archive_cycle=1,
    min_monkeys=100,
    archive_maps=False)

# Test

t1 = time.time()
sim.create_monkeys(nmonkeys)
t2 = time.time()
print('Standard: {0:.0f} μs ({1:.2f} μs per monkey)'.format(
    (t2 - t1) * (10**6),
    (t2 - t1) * (10**6) / nmonkeys
))

t1 = time.time()
MonkeyArray(
    npredators=2,
    nsignals=3,
    nstates=3,
    nmonkeys=nmonkeys)
t2 = time.time()
print('Vectorized: {0:.0f} μs ({1:.2f} μs per monkey)'.format(
    (t2 - t1) * (10**6),
    (t2 - t1) * (10**6) / nmonkeys
))
