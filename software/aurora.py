#!/usr/bin/python

import serialsnake as ss
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
		

def readMusic():

	
	Music_File = open('./music1', 'r')  # Open DC File

	bpm = Music_File.readline()      # Read first line which contains bpm

	bpm = bpm.strip()

	beat = 1

	bps = (60.0/(int(bpm)))

	Beat_Line = Music_File.readline()      # Read first line
	Beat_Line = Beat_Line.strip() 
	Beat_Line = Beat_Line.rstrip() 
	Line_Data = Beat_Line.split(":") 

	while Beat_Line: 
	
		#print beat

		musicbeat = int(Line_Data[0])  # Get the fist part

		if (musicbeat == beat):
			cleanline =  Line_Data[1].rstrip('\n')
			ss.serialQ.put(cleanline.split(" ")) # Send data part

			Beat_Line = Music_File.readline()      # Read first line
			Beat_Line = Beat_Line.strip() 
			Beat_Line = Beat_Line.rstrip() 
			Line_Data = Beat_Line.split(":") 
		else:
			time.sleep(bps)
			beat = beat + 1

	Music_File.close()
		


def main():



	# Send DC Values
	init_DC()

	#Start Thread for Serial Communication
	SCThread = Thread(target=ss.serialThread, args=())
	SCThread.daemon = True
	SCThread.start()

	#Read Music
	while 1:
		readMusic()
	
	#Delay
	time.sleep(1)
	


# Make sure script always runs main first
if __name__ == "__main__":
	main()
