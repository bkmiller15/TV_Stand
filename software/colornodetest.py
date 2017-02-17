#!/usr/bin/python

import serialsnake as ss
from threading import Thread
import time
from random import randint


def init_DC():

	DC_FILE = open('./dc.conf', 'r')  # Open DC File

	dc_line = DC_FILE.readline()      # Read first line
	dc_line = dc_line.strip() 
	dc_line = dc_line.rstrip() 

	while dc_line: 

		if ( dc_line[0] != '#'
		and  dc_line != '\n' ):
			dc_data = dc_line.split(" ") 

			ss.serialQ.put(dc_data)

		dc_line = DC_FILE.readline()      # Read first line
		dc_line = dc_line.strip() 
		dc_line = dc_line.rstrip() 

	DC_FILE.close()
		
		


color_data = []
for packet in xrange(17):
	color_data.append('00')
color_data[0] = ('01')

def main():
	
	init_DC()

	#Start Thread for Serial Communication
	SCThread = Thread(target=ss.serialThread, args=())
	SCThread.daemon = True
	SCThread.start()

	switch = 0
	while 1:

		if (switch == 0):
			green = 255
			blue = 0
			red = 0
			switch = 1
		else: 
			green = 0
			blue = 0
			red = 255
			switch = 0

		green = randint(0,255)
		blue = randint(0,255)
		red = randint(0,255)
		color_data[2] = str(red)
		color_data[3] = str(green)
		color_data[4] = str(blue)
		green = randint(0,255)
		blue = randint(0,255)
		red = randint(0,255)
		color_data[4] = str(red)
		color_data[5] = str(green)
		color_data[6] = str(blue)
		green = randint(0,255)
		blue = randint(0,255)
		red = randint(0,255)
		color_data[7] = str(red)
		color_data[8] = str(green)
		color_data[9] = str(blue)
		green = randint(0,255)
		blue = randint(0,255)
		red = randint(0,255)
		color_data[10] = str(red)
		color_data[11] = str(green)
		color_data[12] = str(blue)
		green = randint(0,255)
		blue = randint(0,255)
		red = randint(0,255)
		color_data[13] = str(red)
		color_data[14] = str(green)
		color_data[15] = str(blue)


		ss.serialQ.put(color_data)
		time.sleep(0.2)
	


# Make sure script always runs main first
if __name__ == "__main__":
	main()
