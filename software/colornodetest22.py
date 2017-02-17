#!/usr/bin/python2

import serialsnake2 as ss
from threading import Thread
import time
from random import randint


	
def main():
	
	#Start Thread for Serial Communication
	SCThread = Thread(target=ss.serialThread_void, args=())
	SCThread.daemon = True
	SCThread.start()

	ss.init_DC()

	sw = 0

	while (1):

		ss.setDataType_void(ss.GS_CMD)
		

		ss.setLEDData_void(2,50)
		ss.setLEDData_void(5,50)
		ss.setLEDData_void(8,50)
		ss.setLEDData_void(11,50)
		ss.setLEDData_void(14,50)

		ss.setLEDData_void(1,50)
		ss.setLEDData_void(4,50)
		ss.setLEDData_void(7,50)
		ss.setLEDData_void(10,50)
		ss.setLEDData_void(13,50)


		ss.loadLEDData_void()

		ss.clearLEDData_void()

		time.sleep(1)


	


# Make sure script always runs main first
if __name__ == "__main__":
	main()
