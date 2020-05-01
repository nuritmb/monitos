import time

from abstractlevel.models import Monkey, MonkeySignal, MonkeyState, MonkeyArray, Predator
from abstractlevel.simulation import Simulation

print('Creation Test')

st1 = MonkeyState(1)  # grass
st2 = MonkeyState(2)  # tree
st3 = MonkeyState(3)  # burrow

sg1 = MonkeySignal(1)
sg2 = MonkeySignal(2)
sg3 = MonkeySignal(3)

pr1 = Predator(
    id=1,  # nothing
    menu={
        st1: 0.99,
        st2: 0.97,
        st3: 0.97})
pr2 = Predator(
    id=2,  # snake
    menu={
        st1: 0.5,
        st2: 0.99,
        st3: 0.6})
pr3 = Predator(
    id=3,  # eagle
    menu={
        st1: 0.6,
        st2: 0.5,
        st3: 0.99})

state_list = [
    st1,
    st2,
    st3]

signal_list = [
    sg1,
    sg2,
    sg3]

predators = [
    pr1,
    pr2,
    pr3]

game = Simulation(
    nmonkeys=10,
    rep_rate=1.2,
    mut_prob=0.05,
    predator_dict={
        pr1: 0.5,
        pr2: 0.5},
    signal_list=signal_list,
    state_list=state_list,
    archive_cicle=1,
    min_monkeys=100,
    archive_maps=False)

game.create_monkeys(10)

ma = MonkeyArray(monkey_list=game.monkey_list)

print('old list:')
for monkey in game.monkey_list:
    monkey.display()
print('')

print('new list:')
for monkey in ma.to_monkey_list(predator_list=predators):
    monkey.display()
print('')

ma = MonkeyArray(
    npredators=len(predators),
    nsignals=len(signal_list),
    nstates=len(state_list),
    nmonkeys=10)

print('array-defined list:')
for monkey in ma.to_monkey_list(predator_list=predators):
    monkey.display()
print('')
