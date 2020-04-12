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
    MonkeySignal(1),
    MonkeySignal(2),
    MonkeySignal(3)
]

monkeystates = [
    MonkeyState(1),
    MonkeyState(2),
    MonkeyState(3)
]

# PREDATORS

nothing = Predator(
    menu={
        monkeystates[0]: 1.0,
        monkeystates[1]: 0.9,
        monkeystates[2]: 0.9 
    },
    id=1 #nothing
)

eagle = Predator(
    menu={
        monkeystates[0]: 0.3,
        monkeystates[1]: 0.9,
        monkeystates[2]: 0.1
    },
    id=2 #eagle
)

snake = Predator(
    menu={
        monkeystates[0]: 0.3,
        monkeystates[1]: 0.1,
        monkeystates[2]: 0.9
    },
    id=3 #snake
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
            id=i+1,
            predator_list=predators,
            signal_list=monkeyvocab,
            state_list=monkeystates))


# COUNTER CREATION

wordmapCountDict=dict()

for i in range(len(predators)):
    for j in range(len(monkeyvocab)):
        wordmapCountDict[str(predators[i].id)+'->'+str(monkeyvocab[j])]=0 

actionmapCountDict=dict()

for i in range(len(monkeyvocab)):
    for j in range(len(monkeystates)):
        actionmapCountDict[str(monkeyvocab[i])+'->'+str(monkeystates[j])]=0 

turnwordmapCountDict=dict()

for i in range(len(predators)):
    for j in range(len(monkeyvocab)):
        turnwordmapCountDict[str(predators[i].id)+'->'+str(monkeyvocab[j])]=[0]*nturns 

turnactionmapCountDict=dict()

for i in range(len(monkeyvocab)):
    for j in range(len(monkeystates)):
        turnactionmapCountDict[str(monkeyvocab[i])+'->'+str(monkeystates[j])]=[0]*nturns 




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
                turnwordmapCountDict[str(animal.id)+'->'+str(monkey.wordmap[animal])][turn]+=1
            for vocab in monkeyvocab:
                actionmapCountDict[str(vocab)+'->'+str(monkey.actionmap[vocab])]+=1
            # turnwordmapCountDict[eagle.id+'->'+str(monkey.wordmap[eagle])][turn]+=1
            # turnwordmapCountDict[nothing.id+'->'+str(monkey.wordmap[nothing])][turn]+=1
            # turnwordmapCountDict[snake.id+'->'+str(monkey.wordmap[snake])][turn]+=1
            newmonkeylist.append(monkey)
    #print('state count:')
#    for state, count in monkeystatecounter.items():
#        print('    %d %s monkeys'%(count, state))
    #print('%d monkeys killed' % (len(monkeylist)-len(newmonkeylist)))
    #print('%d monkeys left' % len(newmonkeylist))
    monkeylist = newmonkeylist

    # REPRODUCTIVE PHASE
    babymonkeys = []
    nbabymonkeys = int(len(newmonkeylist)*(reproduction_rate-1.0)) ### por qué length de newmonkeylist, good practice??? f u
    for babymoney_i in range(nbabymonkeys):
        teacher = random.choice(monkeylist)
        baby = Monkey(
            id=babymoney_i+1+len(monkeylist),
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
    #         turnwordmapCountDict[str(predator.id)+'->'+str(monkey.wordmap[predator])][turn]+=1
    #     for vocab in monkeyvocab:
    #         turnactionmapCountDict[str(vocab)+'->'+str(monkey.actionmap[vocab])][turn]+=1




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
#             wordmapCountDict[str(predator.id)+'->'+str(monkey.wordmap[predator])]+=1
#         for vocab in monkeyvocab:
#             actionmapCountDict[str(vocab)+'->'+str(monkey.actionmap[vocab])]+=1
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




