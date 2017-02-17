#!/usr/bin/python2

import threading 
import time


def hello():
	print "hello"
	

	
def main():

	while(1):
		t = threading.Timer(5.0, hello)
 		t.start()
		t.join()

	


# Make sure script always runs main first
if __name__ == "__main__":
	main()
