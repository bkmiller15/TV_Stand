#!/usr/bin/python

import random

LMF = 0
beat = 0

def led_on():
	global beat
	on_time = random.randint(1,5)
	red = random.randint(0,255)
	green = random.randint(0,255)
	blue = random.randint(0,255)
	writeline(beat,red,green,blue)
	beat = beat + on_time

def led_off():
	global beat
	off_time = random.randint(1,4)
	red = 0
	green = 0
	blue = 0
	writeline(beat,red,green,blue)
	beat = beat + off_time

def led_fadeup():
	global beat
	fade_time = random.randint(10,100)
	red = random.randint(0,255)
	green = random.randint(0,255)
	blue = random.randint(0,255)
	writeline(beat,0,0,0)
	beat = beat + 1
	red = red/fade_time
	green = green/fade_time
	blue = blue/fade_time
	newred = 0	
	newgreen = 0	
	newblue = 0	
	for x in xrange(fade_time):
		newred = newred + red
		newgreen = newgreen + green
		newblue = newblue + blue
		writeline(beat,newred,newgreen,newblue)
		beat = beat + 1

def led_fadedown():
	global beat
	fade_time = random.randint(10,100)
	red = random.randint(0,255)
	green = random.randint(0,255)
	blue = random.randint(0,255)
	writeline(beat,red,green,blue)
	beat = beat + 1
	red = red/fade_time
	green = green/fade_time
	blue = blue/fade_time
	newred = 0	
	newgreen = 0	
	newblue = 0	
	for x in xrange(fade_time):
		newred = newred - red
		newgreen = newgreen - green
		newblue = newblue - blue
		writeline(beat,newred,newgreen,newblue)
		beat = beat + 1

	writeline(beat,0,0,0)
	beat = beat + 1


def writeline(beat,red,green,blue):
	global LMF
	LMF.write(str(beat)+":01 "+str(red)+" "+str(green)+" "+str(blue)+" 00 00 00 00 00 00 00 00 00 00 00 00 00\n")
	

def main():

	global LMF
	global beat
	file_name = raw_input("Enter a file name: ")
	bpm = raw_input("Enter bpm: ")
	length = raw_input("Enter Length: ")
	
	LMF = open(file_name, 'w')  # Open DC File
	LMF.write(bpm+"\n")

	beat = 1

	while (beat < int(length)):
		num = random.randint(0,10)
		if (num == 0):
			led_off()
		#elif (num >= 1 or num <=2 ):
		#	led_on()
		elif (num >= 3 or num <=6 ):
			led_fadeup()
		elif (num >= 7 or num <=10 ):
			led_fadedown()
			
	
	LMF.close()
	


# Make sure script always runs main first
if __name__ == "__main__":
	main()
