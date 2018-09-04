import sys
import zmq
import Queue
import itertools
import os

port = "5563"
# Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)

socket.connect ("tcp://localhost:%s" % port)

socket.setsockopt(zmq.SUBSCRIBE, '')

gesturePoints = Queue.Queue()

for i in range(5):
	gesturePoints.put(0)

while True:
	string = socket.recv()
	x, y = string.split(',')
	gesturePoints.get()
	gesturePoints.put(x)
	gesturePointsList = list(gesturePoints.queue)
	print gesturePointsList
	if all(earlier > later for earlier, later in itertools.izip(gesturePointsList, gesturePointsList[1:])):
		print 'Descending'
		os.system('nircmd.exe changesysvolume 5000')

	if all(earlier < later for earlier, later in itertools.izip(gesturePointsList, gesturePointsList[1:])):
		print 'Ascending'
		os.system('nircmd.exe changesysvolume -5000')
	