#!/usr/bin/python2

import threading 
import time


def hello():
	print "hello"
	global t 
	t = threading.Timer(0.001, hello)
	t.start()

	
def main():
	t = threading.Timer(0.001, hello)
	t.start()

	while(1):
		v = 0
	


# Make sure script always runs main first
if __name__ == "__main__":
	main()
