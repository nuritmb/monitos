import time

from abstractlevel.models import Predator, PredArray, MonkeyState

print('Speed Test: Normal')
t1 = time.time()
for _ in range(1000):
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
t2 = time.time()
print('1000 Laps Time (s): ', t2 - t1)
print('')

print('Speed Test: Vectorized')
t1 = time.time()
for _ in range(1000):
    pa = PredArray(
        [
            [0.9900, 0.2000, 0.3000],
            [0.9900, 0.2000, 0.3000],
            [0.8000, 0.7000, 0.9900],
            [0.2000, 0.8000, 0.3000],
        ])
t2 = time.time()
print('1000 Laps Time (s): ', t2 - t1)
print('')
