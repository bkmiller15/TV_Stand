#!/usr/bin/python

import serialsnake as ss
import colorblaster as cb
from threading import Thread
import time

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
		colorblast = cb.getColor(2)
		color_data[1] = str(colorblast[1]*16) 
		color_data[2] = str(colorblast[2]*16) 
		color_data[3] = str(colorblast[0]*16) 
		color_data[4] = str(colorblast[1]*16) 
		color_data[5] = str(colorblast[2]*16) 
		color_data[6] = str(colorblast[0]*16) 
		color_data[7] = str(colorblast[1]*16) 
		color_data[8] = str(colorblast[2]*16) 
		color_data[9] = str(colorblast[0]*16) 
		ss.serialQ.put(color_data)
		time.sleep(1)
		color_data[1] = str(colorblast[4]*16) 
		color_data[2] = str(colorblast[5]*16) 
		color_data[3] = str(colorblast[3]*16) 
		color_data[4] = str(colorblast[4]*16) 
		color_data[5] = str(colorblast[5]*16) 
		color_data[6] = str(colorblast[3]*16) 
		color_data[7] = str(colorblast[4]*16) 
		color_data[8] = str(colorblast[5]*16) 
		color_data[9] = str(colorblast[3]*16) 
		ss.serialQ.put(color_data)
		time.sleep(1)
	


# Make sure script always runs main first
if __name__ == "__main__":
	main()
