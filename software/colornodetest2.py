#!/usr/bin/python

import serialsnake as ss
from threading import Thread
import time
from random import randint


def main():
	
	#Start Thread for Serial Communication
	SCThread = Thread(target=ss.serialThread, args=())
	SCThread.daemon = True
	SCThread.start()

	ss.init_DC()
	#ss.updateSerialData()
	#ss.printSerialData()

	ss.qDelay()
	time.sleep(1)

	


	value = 0
	dire = 1


	while 1:
		value = 0

		ss.qDelay()

		ss.setDataType(ss.GS_CMD)

		for y in xrange(3,31,3):
			ss.setColorData(y,value)

		ss.drawColorData()

		if (value >= 225):
			dire = 0
		elif (value <= 0):
			dire = 1 


		if (dire == 1):
			value = value + 4
		elif (dire == 0):
			value = value - 4

		

		time.sleep(0.005)
	


# Make sure script always runs main first
if __name__ == "__main__":
	main()
