#!/usr/bin/python

import serialsnake as ss
from threading import Thread
import time
from random import randint
import gtk, sys


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
red = 0
green = 0
blue = 0
cset = 0

#--\\ GTK Config //--#
w = gtk.Window()
c = gtk.ColorSelection()
w.add(c)
w.show_all()



#in Code //--#
def callback(*args):
	global red
	global green
	global blue
	global cset
	color=c.get_current_color()
	red = int(color.red)
	green = int(color.green)
	blue = int(color.blue)
	red = red/256
	green = green/256
	blue = blue/256
	#print red 
	#print green 
	#print blue 
	cset = 1
	green = green * 16
	blue = blue * 16
	red = red * 16
	color_data[1] = str(green)
	color_data[2] = str(blue)
	color_data[3] = str(red)
	print color_data
	ss.serialQ.put(color_data)

c.connect('color-changed', callback)
w.connect('destroy', sys.exit)


def main():
	global red
	global green
	global blue
	global cset
	
	init_DC()

	#Start Thread for Serial Communication
	SCThread = Thread(target=ss.serialThread, args=())
	SCThread.daemon = True
	SCThread.start()

	green = green * 16
	blue = blue * 16
	red = red * 16
	color_data[1] = str(green)
	color_data[2] = str(blue)
	color_data[3] = str(red)
	#print color_data
	ss.serialQ.put(color_data)
	print cset

	gtkThread = Thread(target=gtk.main(), args=())
	gtkThread.daemon = True
	gtkThread.start()
	#gtk.main()
	

	while 1:
	#	#red = int(input("Red: "))
	#	#green = int(input("Green: "))
	#	#blue = int(input("Blue: "))
	#	print cset
	#	if (cset == 1):
	#		green = green * 16
	#		blue = blue * 16
	#		red = red * 16
	#		color_data[1] = str(green)
	#		color_data[2] = str(blue)
	#		color_data[3] = str(red)
	#		print color_data
	#		ss.serialQ.put(color_data)
	#		cset = 0

		time.sleep(0.51)
	
	


# Make sure script always runs main first
if __name__ == "__main__":
	main()
