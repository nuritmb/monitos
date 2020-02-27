#from __future__ import unicode_literals
import numpy as np
import random
import math
import itertools
import matplotlib.pylab as plt
#import matplotlib
from moviepy.video.io.bindings import mplfig_to_npimage
import moviepy.editor as mpy
#matplotlib.rcParams['text.usetex'] = True
#matplotlib.rcParams['text.latex.unicode'] = True


n=400 #maximum number of monkeys
initial_n=100 # initial number of monkeys
current_n=initial_n #current number of monkeys

m=n #maximum number of eagles
initial_m=16
current_m=initial_m

ini_n_events = 2    # numero de eventos iniciales
ini_n_acts = 2 		# numero de actos iniciales
ini_n_signals = 2   # numero de señales iniciales

list_events = list(range(ini_n_events))      # [0,1] 
list_acts = list(range(ini_n_acts))
list_signals = list(range(ini_n_signals))

max_axis  = 100
longest_step= float(max_axis/15)


x_axis = np.ones(n) #* -max_axis
#x_axis = [x * max_axis for x in x_axis]
y_axis = np.ones(n) #* -max_axis
#y_axis = [x * max_axis for x in y_axis]

fitness = np.zeros(n)


emitters = np.zeros(n)
#1 if they see an eagle
#2 if they see a snake


receptors = np.zeros(n)


x_eagle = np.random.rand(m) * max_axis
y_eagle = np.random.rand(m) * max_axis

eagle_detection_distance = 1
monkey_detection_distance = 10

#monkeys_hidden = []
rounds_hidden = np.zeros(n)
max_rounds_hidden = 2



dead_monkeys = np.zeros(n)

event_signal = np.zeros((n,), dtype='i,i')   #matrix of tuples? or just lists of signals where position marks the event?
signal_act = np.zeros((n,), dtype='i,i')

state = np.array([1]*initial_n + [0]*(n-initial_n)) #stuff like hidden or in a tree, essentially acts

moving = np.array([1]*initial_n + [0]*(n-initial_n))

# -2 vio al aguila??
# -1 vio a la serpiente??
# 0 muerto
muerto=0
# 1 vivo chilleando
vivo=1
# 2 escondido en arbusto
arbusto=2
# 3 trepado en arbol
arbol=3




#comparar los dos 

def functions_list_sender(list_signals,list_events):
	return (list(itertools.product(*([list_signals]*len(list_events))))[random.randint(0,len(list_signals)^len(list_events)-1)])

def functions_list_receiver(list_signals,list_acts):
	return (list(itertools.product(*([list_signals]*len(list_acts))))[random.randint(0,len(list_signals)^len(list_acts)-1)])


#initialize_event_signal():     #sender strategy   []

for i in range(initial_n):
 	event_signal[i]=functions_list_sender(list_signals,list_events)
 	
# #initialize_signal_act():    #receiver strategy
for i in range(initial_n):
	signal_act[i]=functions_list_sender(list_signals,list_acts)

 

def move():
	global x_axis
	global y_axis
	global state
	global monkeys_hidden
	global moving

	# for monkey in monkeys_hidden:   ##change to array substraction

	# 	if state[monkey]!=0 and state[monkey]!=1 and rounds_hidden[monkey]>max_rounds_hidden:  #shall the monkey move again?
	# 			rounds_hidden[monkey]=0
	# 			moving[monkey]=1
	# 			state[monkey]=1

	temp=rounds_hidden
	temp[temp<max_rounds_hidden]=0          #change to 1 only those who have stayed put more than the max rounds
	temp[temp>max_rounds_hidden]=1

	print(temp)

	moving = moving + temp                                  # change from 0 to 1 those who can move again

	state = state + temp*5                                  # change from 2 and 3 to 1 the state of those that can move again

	state[state > 5]=1

	


	if random.random()>0.5:

		x_axis = x_axis + ((np.random.uniform(low=-1.0, high=1.0, size=(n,)) * longest_step) * moving)

		y_axis = y_axis + ((np.random.uniform(low=-1.0, high=1.0, size=(n,)) * longest_step) * moving)

	else:

		x_axis = x_axis - ((np.random.uniform(low=-1.0, high=1.0, size=(n,)) * longest_step) * moving)

		y_axis = y_axis - ((np.random.uniform(low=-1.0, high=1.0, size=(n,)) * longest_step) * moving)


	while np.amax(x_axis)>max_axis:

		x_axis[np.argmax(x_axis)] = 2*max_axis - x_axis[np.argmax(x_axis)]


	while np.amax(x_axis)<-max_axis:

		x_axis[np.argmax(x_axis)] = -2*max_axis - x_axis[np.argmax(x_axis)]


	while np.amax(y_axis)>max_axis:

		y_axis[np.argmax(y_axis)] = 2*max_axis - y_axis[np.argmax(y_axis)]


	while np.amax(y_axis)<-max_axis:

		y_axis[np.argmax(y_axis)] = -2*max_axis - y_axis[np.argmax(y_axis)]
				


# def move(axis):
# 	global rounds_hidden
# 	global state

# 	for monkey in range(current_n):

# 		if state[monkey]!=0 and state[monkey]!=1 and rounds_hidden[monkey]>max_rounds_hidden:  #shall the monkey move again?
# 				rounds_hidden[monkey]=0
# 				state[monkey]=1



# 		if state[monkey]==1:

# 			if random.random()>0.5:
# 				axis[monkey]=axis[monkey]+(random.random() * longest_step)
# 			else:
# 				axis[monkey]=axis[monkey]-(random.random() * longest_step)
# 			if axis[monkey]>max_axis:
# 				axis[monkey]=2*max_axis-axis[monkey]
# 			if axis[monkey]<-max_axis:
# 				axis[monkey]=-2*max_axis-axis[monkey]

				
# 	return axis

# def move_eagle(axis):

# 	for eagle in range(current_m):


# 		if random.random()>0.5:
# 			axis[eagle]=axis[eagle]+(random.random() * float(longest_step/2))
# 		else:
# 			axis[eagle]=axis[eagle]-(random.random() * float(longest_step/2))

# 		#print(eagle)
# 		#print(axis[eagle])
# 		if axis[eagle]>max_axis:
# 			axis[eagle]=2*max_axis-axis[eagle]
# 		if axis[eagle]<-max_axis:
# 			axis[eagle]=-2*max_axis-axis[eagle]



def move_eagle():

	global x_eagle
	global y_eagle

	if random.random()>0.5:

		x_eagle = x_eagle + ((np.random.uniform(low=-1.0, high=1.0, size=(n,)) * longest_step) * moving)

		y_eagle = y_eagle + ((np.random.uniform(low=-1.0, high=1.0, size=(n,)) * longest_step) * moving)

	else:

		x_eagle = x_eagle - ((np.random.uniform(low=-1.0, high=1.0, size=(n,)) * longest_step) * moving)

		y_eagle = y_eagle - ((np.random.uniform(low=-1.0, high=1.0, size=(n,)) * longest_step) * moving)


	while np.amax(x_eagle)>max_axis:

		x_eagle[np.argmax(x_eagle)] = 2*max_axis - x_eagle[np.argmax(x_eagle)]


	while np.amax(x_eagle)<-max_axis:

		x_eagle[np.argmax(x_eagle)] = -2*max_axis - x_eagle[np.argmax(x_eagle)]


	while np.amax(y_eagle)>max_axis:

		y_eagle[np.argmax(y_eagle)] = 2*max_axis - y_eagle[np.argmax(y_eagle)]


	while np.amax(y_eagle)<-max_axis:

		y_eagle[np.argmax(y_eagle)] = -2*max_axis - y_eagle[np.argmax(y_eagle)]

def eagle_detection():

	list_of_emitters=[]

	for i in range(current_m):
		
		eagle_loc=[x_eagle[i],y_eagle[i]]

		for j in range(current_n):
		
			monkey_loc=[x_axis[j],y_axis[j]]
		
			if math.sqrt((eagle_loc[0]-monkey_loc[0])**2 + (eagle_loc[1]-monkey_loc[1])**2)<eagle_detection_distance:
				#print('detection!')
				list_of_emitters.append(j)



	return list_of_emitters


def game_round(list_of_emitters):
	
	global moving
	global rounds_hidden
	#global monkeys_hidden

	#print(list_of_emitters)

	if len(list_of_emitters)>0:

		for i in list_of_emitters:
			number_alerted=0
			emitter_loc=[x_axis[i],y_axis[i]]

			for j in range(current_n):

				if state[j]!=0:
					
					receiver_loc=[x_axis[j],y_axis[j]]

					if math.sqrt((emitter_loc[0]-receiver_loc[0])**2 + (emitter_loc[1]-receiver_loc[1])**2)<monkey_detection_distance:

						 
						number_alerted+=1
						state[j]=(signal_act[j][event_signal[i][0]])+2
						moving[j] = 0
						#monkeys_hidden.append(j)
						rounds_hidden[j]+=1

			#print(str(i)+' alerted '+str(number_alerted)+' other monkeys')





dead_monkeys = []

def hunt():
	
	global state
	global dead_monkeys
	global rounds_hidden
	global moving

	exposed_monkeys=[]

	for i in range(current_n):

		if state[i]!=0 and state[i]!=arbusto :
			exposed_monkeys.append(i)

	for i in range(current_m):
		
		eagle_loc=[x_eagle[i],y_eagle[i]]

		for j in exposed_monkeys:
		
			monkey_loc=[x_axis[j],y_axis[j]]
		
			if math.sqrt((eagle_loc[0]-monkey_loc[0])**2 + (eagle_loc[1]-monkey_loc[1])**2)<eagle_detection_distance:
				#print('murder!')
				dead_monkeys.append(j)
				moving[j]=0
				state[j]=0
				rounds_hidden[j]=0




# def signalling game:

# def purge:

# def next generation:

def finer_grain(aspect_of_world):
	aspect_of_world = aspect_of_world.append(aspect_of_world[-1]+1)
	return aspect_of_world




# animation section

duration=10

fig, ax = plt.subplots()



def make_frame(t):

	global x_axis
	global y_axis
	global x_eagle
	global y_eagle
	
	ax.clear()
	ax.set_ylim(-max_axis, max_axis)
	ax.set_xlim(-max_axis, max_axis)

	move()
	# x_axis = move(x_axis)
	# y_axis = move(y_axis)

	move_eagle()
	# x_eagle = move_eagle(x_eagle)
	# y_eagle = move_eagle(y_eagle) 
	
	
	em = eagle_detection()

	em_x=[]
	em_y=[]

	for i in em:
		em_x.append(x_axis[i])
		em_y.append(y_axis[i])


	game_round(em)

	hunt()

	# death_x = []
	# death_y = []

	# for i in dead_monkeys:
	# 	death_x.append(x_axis[i])
	# 	death_y.append(y_axis[i])

	

	#ax.plot(x_axis[:current_n], y_axis[:current_n], 'ko')

	for i in range(current_n):

		if state[i]==1:
			ax.plot(x_axis[i], y_axis[i], 'ko')

		elif state[i]==2:

			ax.plot(x_axis[i], y_axis[i], 'g*',markersize=5)

		elif state[i]==3:

			ax.plot(x_axis[i], y_axis[i], 's' , markersize=5, color='#8B4513')

		elif state[i]==0:

			ax.plot(x_axis[i], y_axis[i], 'r8')


	
	
	ax.plot(x_eagle[:current_m],y_eagle[:current_m], 'rx')

	# for i in dead_monkeys:
	# 	ax.annotate('murder',
	#             xy=(x_axis[i], y_axis[i]),  # theta, radius
	#             xytext=(-80, -80),    # fraction, fraction
	#             arrowprops=dict(facecolor='red', shrink=0.05),
	#             horizontalalignment='left',
	#             verticalalignment='bottom',
	#             )

	ax.plot(em_x,em_y, 'yo',markersize=10)
	# for i in em:
	# 	ax.annotate('detection',
	#             xy=(x_axis[i], x_axis[i]),  # theta, radius
	#             xytext=(-50, 50),    # fraction, fraction
	#             arrowprops=dict(facecolor='yellow', shrink=0.05),
	#             horizontalalignment='left',
	#             verticalalignment='bottom',
	#             )


	return mplfig_to_npimage(fig)

animation = mpy.VideoClip(make_frame, duration=duration)
animation.preview(fps=24)
#  animation.write_gif('matplotlib.gif', fps=9)

# for x in range(0,9):
# 	plt.plot(x_axis,y_axis)
# 	plt.show()
# 	x_axis=move(x_axis)
# 	y_axis=move(y_axis)

