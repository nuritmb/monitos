#from __future__ import unicode_literals
import numpy
import random
import matplotlib.pylab as plt
#import matplotlib
from moviepy.video.io.bindings import mplfig_to_npimage
import moviepy.editor as mpy
#matplotlib.rcParams['text.usetex'] = True
#matplotlib.rcParams['text.latex.unicode'] = True


n=10 #root of maximum number of monkeys
initial_n=4 #root of initial number of monkeys
current_n=initial_n #current number of monkeys
m=n #maximum number of eagles
initial_m=4
current_m=initial_m

ini_n_events = 2
ini_n_acts = 2
ini_n_signals = 2

list_events = list(range(1,ini_n_events+1))
list_acts = list(range(1,ini_n_acts+1))
list_signals = list(range(1,ini_n_signals+1))

max_axis  = 25
longest_step= float(max_axis/4)

x_axis = numpy.zeros((n,n))
#x_axis = [x * max_axis for x in x_axis]
y_axis = numpy.zeros((n,n))
#y_axis = [x * max_axis for x in y_axis]

fitness = numpy.zeros((n,n))

emitters = numpy.zeros((n,n))
receptors = numpy.zeros((n,n))

x_eagle = numpy.random.rand(1,m) * max_axis
y_eagle = numpy.random.rand(1,m) * max_axis

eagle_detection_distance = 1

event_signal = numpy.zeros((n,n))   #matrix of tuples? or just lists of signals where position marks the event?
signal_act = numpy.zeros((n,n))

state = numpy.zeros((n,n))  #stuff like hidden or in a tree, essentially acts

def initialize_event_signal(mapping):
	for monkey in numpy.nditer(mapping[:initial_n,:initial_n],flags=['ranged'],op_flags=['readwrite']):
		monkey[...]=[choice(list_events),choice(list_signals)]
	return mapping

def initialize_signal_act(mapping):
	for monkey in numpy.nditer(mapping[:initial_n,:initial_n],flags=['ranged'],op_flags=['readwrite']):
		monkey[...]=[choice(list_signals),choice(list_acts)]
	return mapping

def move(axis):
	for monkey in numpy.nditer(axis[:current_n,:current_n],flags=['ranged'],op_flags=['readwrite']):
		if random.random()>0.5:
			monkey[...]=monkey+(random.random() * longest_step)
		else:
			monkey[...]=monkey-(random.random() * longest_step)
		if monkey>max_axis:
			monkey[...]=2*max_axis-monkey
		if monkey<-max_axis:
			monkey[...]=-2*max_axis-monkey
	return axis

def move_eagle(axis):
	for eagle in numpy.nditer(axis[:current_m],flags=['ranged'],op_flags=['readwrite']):
		if random.random()>0.5:
			eagle[...]=eagle+(random.random() * longest_step)
		else:
			eagle[...]=eagle-(random.random() * longest_step)
		if eagle>max_axis:
			eagle[...]=2*max_axis-eagle
		if eagle<-max_axis:
			eagle[...]=-2*max_axis-eagle
	return axis


def eagle_detection():
	i=0
	for eagle in x_eagle:
		temp_x=x_axis-eagle

		


		i+=1



# def signalling game:

# def purge:

# def next generation:

def finer_grain(aspect_of_world):
	aspect_of_world = aspect_of_world.append(aspect_of_world[-1]+1)
	return aspect_of_world


# animation section

duration=5

fig, ax = plt.subplots()

def make_frame(t):

	global x_axis
	global y_axis
	global x_eagle
	global y_eagle
	ax.clear()
	x_axis = move(x_axis)
	y_axis = move(y_axis)
	x_eagle = move_eagle(x_eagle)
	y_eagle = move_eagle(y_eagle) 
	ax.set_ylim(-max_axis, max_axis)
	ax.set_xlim(-max_axis, max_axis)
	ax.plot(x_axis, y_axis, 'ko')
	ax.plot(x_eagle,y_eagle, 'x')
	return mplfig_to_npimage(fig)

animation = mpy.VideoClip(make_frame, duration=duration)
#animation.ipython_display(fps=20, loop=True, autoplay=True)
animation.write_gif('matplotlib.gif', fps=10)

# for x in range(0,9):
# 	plt.plot(x_axis,y_axis)
# 	plt.show()
# 	x_axis=move(x_axis)
# 	y_axis=move(y_axis)

