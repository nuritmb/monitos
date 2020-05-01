from abstractlevel.models import Predator, PredArray, MonkeyState

print('Creation Test')

st1 = MonkeyState(1)
st2 = MonkeyState(2)
st3 = MonkeyState(3)

pr1 = Predator({
    st1: 0.99,
    st2: 0.2,
    st3: 0.3},
    id=1)
pr2 = Predator({
    st1: 0.99,
    st2: 0.2,
    st3: 0.3},
    id=2)
pr3 = Predator({
    st1: 0.8,
    st2: 0.7,
    st3: 0.99},
    id=3)
pr4 = Predator({
    st1: 0.2,
    st2: 0.80,
    st3: 0.3},
    id=4)

state_list = [
    st1,
    st2,
    st3]

predator_list = [
    pr1,
    pr2,
    pr3,
    pr4]

pa = PredArray(
    predator_list=predator_list,
    state_list=state_list)

print('old list:')
for pred in predator_list:
    print(pred.__repr__())
print('')

print('new list:')
for pred in pa.to_predator_list(state_list=state_list):
    print(pred.__repr__())
print('')

pa = PredArray([
    [0.9900, 0.2000, 0.3000],
    [0.9900, 0.2000, 0.3000],
    [0.8000, 0.7000, 0.9900],
    [0.2000, 0.8000, 0.3000]])

print('array-defined list')
for pred in pa.to_predator_list(state_list=state_list):
    print(pred.__repr__())
print('')

pa = PredArray([
    [0.9900, 0.2000, 0.3000],
    [0.9900, 0.2000, 0.3000],
    [0.8000, 0.7000, 0.9900],
    [0.2000, 0.8000, 0.3000]],
    spawn_probabilities=[0.1, 0.1, 0.1, 0.7])

print('array-defined list with spawn chances')
for i, pred in enumerate(pa.to_predator_list(state_list=state_list)):
    print(pred.__repr__(), 'chance:', pa.spawn_probabilities[i])
print('')

print('')