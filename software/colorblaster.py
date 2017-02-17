from random import randint
import colorsys
import math


SMIN = 60  # Saturation value min
LMIN = 25  # Light value min
LMAX = 55  # Light value max

CCMAX = 2  # Color count max


def getColor(colorcount):
	
	rgb_array = []  # Array of color data to return

	h_random = randint(0,359)	
	l_random = randint(LMIN,LMAX)	
	s_random = randint(SMIN,100)	

	if (colorcount == 1) or (colorcount > CCMAX):
		for x in xrange(colorcount):
			rgb_array = addDataToArray(h_random,l_random,s_random,rgb_array)
			#rgb_array = addDataToArray(310,55,100,rgb_array)
	elif (colorcount == 2):
			rgb_array = getAnalogous(h_random,l_random,s_random,rgb_array,colorcount)
		
			

	return rgb_array
		
		
def addDataToArray(h,l,s,array):
	h = (h/360.0)
	l = (l/100.0)
	s = (s/100.0)
	r,g,b = colorsys.hls_to_rgb(h,l,s)
	r = r * 255
	g = g * 255
	b = b * 255
	r = math.ceil(r)	 
	g = math.ceil(g)
	b = math.ceil(b)
	array.append(int(r))
	array.append(int(g))
	array.append(int(b))

	return array
	
	
def getAnalogous(h,l,s,array,colorcount):
	angle = randint(30,75)
	
	print h
	print angle
	array = addDataToArray(h,l,s,array)

	if (colorcount == 2):
		addsub = randint(0,1)
		print addsub
		if (addsub == 0):
			h = h + angle
			if (h > 359):
				h = h - 360
		else:
			h = h - angle
			if (h < 0):
				h = 360 + h
			
		array = addDataToArray(h,l,s,array)

	print h
	print "---"
	return array
		
		
