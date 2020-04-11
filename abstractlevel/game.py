from typing import Dict
from models import MonkeySignal, MonkeyState, Monkey, Predator # if it doesn't run, add '.' right before models
from enum import Enum
import random
import matplotlib.pyplot as plt
from time import process_time

# GAME CONSTANTS

nmonkeys = 10000
nturns = 1000
lastTurn = 0 ###to record LAST TURN to print the EVOLUTION DICTS
reproduction_rate = 1.7
mutation_probability = 0.1

# MONKEY VOCABULARY AND STATES

monkeyvocab = [
    MonkeySignal('we'),
    MonkeySignal('love'),
    MonkeySignal('jeffking')
]

monkeystates = [
    MonkeyState('grass'),
    MonkeyState('burrow'),
    MonkeyState('tree')
]

# PREDATORS

nothing = Predator(
    menu={
        monkeystates[0]: 1.0,
        monkeystates[1]: 0.9,
        monkeystates[2]: 0.9 
    },
    name='nothing'
)

eagle = Predator(
    menu={
        monkeystates[0]: 0.3,
        monkeystates[1]: 0.9,
        monkeystates[2]: 0.1
    },
    name='eagle'
)

snake = Predator(
    menu={
        monkeystates[0]: 0.3,
        monkeystates[1]: 0.1,
        monkeystates[2]: 0.9
    },
    name='snake'
)

predators = [
    nothing,
    eagle,
    snake
]

eagle_prob = 0.2
snake_prob = 0.2

# MONKEY CREATION

monkeylist = []
for i in range(nmonkeys):
    monkeylist.append(
        Monkey(
            name='Jeff King %d'%(i+1),
            predator_list=predators,
            signal_list=monkeyvocab,
            state_list=monkeystates))


# COUNTER CREATION

wordmapCountDict=dict()

for i in range(len(predators)):
    for j in range(len(monkeyvocab)):
        wordmapCountDict[str(predators[i].name)+'->'+str(monkeyvocab[j].value)]=0 

actionmapCountDict=dict()

for i in range(len(monkeyvocab)):
    for j in range(len(monkeystates)):
        actionmapCountDict[str(monkeyvocab[i].value)+'->'+str(monkeystates[j].value)]=0 

turnwordmapCountDict=dict()

for i in range(len(predators)):
    for j in range(len(monkeyvocab)):
        turnwordmapCountDict[str(predators[i].name)+'->'+str(monkeyvocab[j].value)]=[0]*nturns 

turnactionmapCountDict=dict()

for i in range(len(monkeyvocab)):
    for j in range(len(monkeystates)):
        turnactionmapCountDict[str(monkeyvocab[i].value)+'->'+str(monkeystates[j].value)]=[0]*nturns 




#############
# GAME START
#############

##### to measure how long a game is taking
t = process_time()

for turn in range(nturns):
#    print('TURN %d' % turn)
#    print('--------------')
    # PREDATOR APPEARS
    p = random.random()
    pred = nothing
    if p > 1.0 - eagle_prob:
        pred = eagle
    elif p < snake_prob:
        pred = snake
    #print('predator:', pred)

    # WITNESS SEES
    witness = random.choice(monkeylist)
    # WITNESS EMMITS SIGNAL
    msg = witness.emmit(pred)
    #print('witness:')
    #witness.display(indentlevel=1)
    #print('message:', msg)

    # EATING PHASE
    monkeystatecounter = {}
    newmonkeylist = []
    for monkey in monkeylist:
        # TODO: witness state change
        monkey.receive(msg)
        currentState=monkey.state
        if currentState in monkeystatecounter:
            monkeystatecounter[currentState] += 1
        else:
            monkeystatecounter[currentState] = 0
        if pred.survived(currentState):
            for animal in predators:
                turnwordmapCountDict[str(animal.name)+'->'+str(monkey.wordmap[animal].value)][turn]+=1
            for vocab in monkeyvocab:
                actionmapCountDict[str(vocab.value)+'->'+str(monkey.actionmap[vocab].value)]+=1
            # turnwordmapCountDict[eagle.name+'->'+str(monkey.wordmap[eagle].value)][turn]+=1
            # turnwordmapCountDict[nothing.name+'->'+str(monkey.wordmap[nothing].value)][turn]+=1
            # turnwordmapCountDict[snake.name+'->'+str(monkey.wordmap[snake].value)][turn]+=1
            newmonkeylist.append(monkey)
    #print('state count:')
#    for state, count in monkeystatecounter.items():
#        print('    %d %s monkeys'%(count, state.value))
    #print('%d monkeys killed' % (len(monkeylist)-len(newmonkeylist)))
    #print('%d monkeys left' % len(newmonkeylist))
    monkeylist = newmonkeylist

    # REPRODUCTIVE PHASE
    babymonkeys = []
    nbabymonkeys = int(len(newmonkeylist)*(reproduction_rate-1.0)) ### por qué length de newmonkeylist, good practice??? f u
    for babymoney_i in range(nbabymonkeys):
        teacher = random.choice(monkeylist)
        baby = Monkey(
            name='Jeff King %d'%(babymoney_i+1+len(monkeylist)),
            wordmap=teacher.wordmap,
            actionmap=teacher.actionmap)
        if random.random() < mutation_probability:
            baby.random_wordmap(predator_list=predators, signal_list=monkeyvocab)
            baby.random_actionmap(signal_list=monkeyvocab, state_list=monkeystates)
        babymonkeys.append(baby)
    #print('reproduction phase: %d monkeys created' % len(babymonkeys))
    monkeylist.extend(babymonkeys)
    #print('new population: %d monkeys' % len(newmonkeylist))

    if len(monkeylist) > nmonkeys:
        exceed = len(monkeylist) - nmonkeys
    #    print('the monkey population has exceeded capacity')
        random.shuffle(monkeylist)
        monkeylist = monkeylist[:nmonkeys]
    #    print('%d monkeys have been eliminated by God.'%exceed)

#    print('--------------')
#    print('')

    ################ MONKEY STORAGE ##################
    ### THIS ADDS TO THE LIST'S SLOT FOR THE TURN THE NUMBER OF MONKEYS THAT HAVE THE STRATEGY 

    # for i,monkey in enumerate(monkeylist):
    #     for predator in predators:
    #         turnwordmapCountDict[str(predator.name)+'->'+str(monkey.wordmap[predator].value)][turn]+=1
    #     for vocab in monkeyvocab:
    #         turnactionmapCountDict[str(vocab.value)+'->'+str(monkey.actionmap[vocab].value)][turn]+=1




    ################ GAME END ########################

    if len(monkeylist) < 100:
 #       print('GAME OVER.')
        lastTurn=turn
        break

print('This game took %s seconds for %d turns, that is %f s per turn' % (process_time()-t,lastTurn,(process_time()-t)/lastTurn))
print(' ')
# input('press ENTER to print survivor maps')



# # print("")
# # print("################")
# # print("SURVIVORS")
# # print("################")
# for i, monkey in enumerate(monkeylist):  #deleted monkeylist[:100] 
#         for predator in predators:
#             wordmapCountDict[str(predator.name)+'->'+str(monkey.wordmap[predator].value)]+=1
#         for vocab in monkeyvocab:
#             actionmapCountDict[str(vocab.value)+'->'+str(monkey.actionmap[vocab].value)]+=1
# #    printmonkey(monkey, i)
# #    print("")

# print("################")
# print("Wordmap totals:")
# print("################")
# print(' ')

# for key in wordmapCountDict:
#     print("%s : %d" % (key,wordmapCountDict[key]))

# print(' ')
# print("################")
# print("Actionmap totals:")
# print("################")
# print(' ')

# for key in actionmapCountDict:
#     print("%s : %d" % (key,actionmapCountDict[key]))    

# print(' ')
# input('press ENTER to print evolution wordmaps')

# for key in turnwordmapCountDict:
#     #print(key+" : "+str(turnwordmapCountDict[key][:lastTurn]))
#     plt.plot(turnwordmapCountDict[key][:lastTurn],label=key)

# plt.legend(loc="upper left")
# plt.title('wordmaps')
# plt.show()
# print(' ')


# input('press ENTER to print evolution actionmaps')
# for key in actionmapCountDict:
#     #print(key+" : "+str(turnactionmapCountDict[key][:lastTurn]))
#     plt.plot(turnactionmapCountDict[key][:lastTurn],label=key)    

# plt.legend(loc="upper left")
# plt.title('actionmaps')
# plt.show()
# print(' ')




