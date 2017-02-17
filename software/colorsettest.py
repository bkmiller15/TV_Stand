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

	while 1:
		green = 150
		blue = 255
		red = 50
		green = green * 16
		blue = blue * 16
		red = red * 16
		color_data[1] = str(green)
		color_data[2] = str(blue)
		color_data[3] = str(red)
		ss.serialQ.put(color_data)
		time.sleep(0.51)
	


# Make sure script always runs main first
if __name__ == "__main__":
	main()
