from threading import Thread
import time
import serial
from Queue import Queue


TOTAL_NODES = 2
PORT = '/dev/ttyUSB0'

TOTAL_CMD_PACKETS = 1
TOTAL_GS_VALUES = 15
TOTAL_DC_VALUES = 12


GS_CMD = 00 
DC_CMD = 10

serialQ = Queue()

led_data = []
led_data.append(0)  # First string for cmd data
for leds in xrange(TOTAL_NODES * TOTAL_GS_VALUES):
	led_data.append(0)

queue_data = []
for node in xrange(TOTAL_NODES + 1):
	queue_data.append([])

serial_data = []
for node in xrange(TOTAL_NODES + 1):
	serial_data.append([])


#############################################################################
##############################################################################
#
# LED_DATA SPECIFIC FUNCTIONS
#
##############################################################################
#############################################################################

##############################################################################
# Title:     	 setLEDData_void(index_int,data_int)
#
# Description:   This is the main function for inserting color values and dc
#                values into the led_data list.  
#
# Inputs:     	 index_int - index of data to be stored
#                data_int - data to be stored in that location
# Outputs:    	 none
# Variables:     none
#
# Author:        Brandon Miller
# Last Revised:  1/1/2015
##############################################################################
def setLEDData_void(index_int,data_int):
	global led_data

	if (index_int > 0 and index_int < len(led_data)):
		led_data[index_int] = data_int


##############################################################################
# Title:     	 setDataType_void(dtype)
#
# Description:   This function sets the type of data in the first index of 
#                led_data.   
#
#                led_data = [ GS_CMD/DC_CMD, .....] 
#
# Inputs:     	 dtype - GS_CMD or DC_CMD
# Outputs:    	 none
# Variables:     none
#
# Author:        Brandon Miller
# Last Revised:  1/1/2015
##############################################################################
def setDataType_void(dtype):
	global led_data

	if (dtype == GS_CMD or dtype == DC_CMD):
		led_data[0] = dtype


##############################################################################
# Title:     	 printLEDData_void()
#
# Description:   Prints led_data in a readable format
#
# Inputs:     	 none
# Outputs:    	 none
# Variables:     none
#
# Author:        Brandon Miller
# Last Revised:  1/1/2015
##############################################################################
def printLEDData_void():
	print ""
	print " Data Type: " + str(led_data[0])
	values = ""
	for data in xrange(TOTAL_CMD_PACKETS,(15 * TOTAL_NODES)+TOTAL_CMD_PACKETS):
		values += " " + str(led_data[data])
		if ((data)%15 == 0):
			print values
			values = ""

	print ""
	print " Raw:"
	print " " + str(led_data)
	print ""


##############################################################################
# Title:     	 loadLEDData_void()
#
# Description:   Converts the led_data to the correct formate to be sent 
#                serially, places that data on the queue, and holds until 
#                the date is processed
#
# Inputs:     	 none
# Outputs:    	 none
# Variables:     none
#
# Author:        Brandon Miller
# Last Revised:  1/1/2015
##############################################################################
def loadLEDData_void():
	global led_data
	global serialQ

	if (led_data[0] == GS_CMD): 
		#print "GS"
		convGS_void()
	elif (led_data[0] == DC_CMD):
		#print "DC"
		convDC_void()

	

	serialQ.join()  # HOLD here until all data on the queue is processed
		


def clearLEDData_void():
	global led_data
	led_data = []
	led_data.append(0)  # First string for cmd data
	for leds in xrange(TOTAL_NODES * TOTAL_GS_VALUES):
		led_data.append(0)




def convGS_void():
	global led_data
	global queue_data
	global serialQ

	for node in xrange(TOTAL_NODES, 0, -1):

		#print node
		queue_data[node] = []                # Clear node data

		cmd_node = str(node + led_data[0])   # Get CMD and Node and conv to string
		cmd_node = cmd_node.zfill(2)         # Pad with zeros
		queue_data[node].append(cmd_node)    # Save in first index of node


		for x in xrange( ((node * TOTAL_GS_VALUES)+1), (((node - 1) * TOTAL_GS_VALUES) + 1), -2):         # Must be reversed to get right order


			# Takes string value [0-255] and converts it to a 12 bit value [0-4096]	
			
			if (x == ((node * TOTAL_GS_VALUES)+1)):
				rgbValue1 = 0
			else:
				rgbValue1 = led_data[x]

			rgbValue2 = led_data[x-1]

			rgbValue1 = convColor2Hex_str(rgbValue1)
			rgbValue2 = convColor2Hex_str(rgbValue2)


			queue_data[node].append(rgbValue1[1] + rgbValue1[2])
			queue_data[node].append(rgbValue2[2] + rgbValue1[0])
			queue_data[node].append(rgbValue2[0] + rgbValue2[1])
	

		serialQ.put(queue_data[node])


def convColor2Hex_str(num_int):

	num_int = int(num_int**1.501)

	# Convert int to a binary stringo
	num_int = bin(num_int)
	num_int = num_int.replace("0b","")   # get rid of the 0x in string	
	num_int = num_int.zfill(12)
	num_int = num_int[::-1]
	num_int = hex(int(num_int, 2))
	num_int = num_int.replace("0x","")   # get rid of the 0x in string

	num_int = num_int.zfill(3)   # Pad with zeros
	

	return num_int


def convDC_void():
	global led_data
	global queue_data
	global serialQ

	for node in xrange(1, TOTAL_NODES + 1):

		queue_data[node] = []                # Clear node data

		cmd_node = str(node + led_data[0])   # Get CMD and Node and conv to string
		cmd_node = cmd_node.zfill(2)         # Pad with zeros
		queue_data[node].append(cmd_node)    # Save in first index of node


		for x in xrange( (((node-1)*TOTAL_DC_VALUES)+1), (node*TOTAL_DC_VALUES) ):         # Must be reversed to get right order

			# Takes string value [0-255] and converts it to a 12 bit value [0-4096]	
			
			rgbValue = led_data[x]

			queue_data[node].append(led_data[x])
	
		
		serialQ.put(queue_data[node])



#############################################################################
##############################################################################
#
# SERIAL THREAD SPECIFIC FUNCTIONS
#
##############################################################################
#############################################################################

##############################################################################
# Title:     	 serialThread_void()
#
# Description:   This function pulls node lists off the queue, if any, and      	
#                then loads them into the apropriate list in serial_data
#
# Inputs:     	 none
# Outputs:    	 none
# Variables:     serial_port - the serial port to use
#
# Author:        Brandon Miller
# Last Revised:  1/1/2015
##############################################################################
def serialThread_void():
	#serial_port = serial.Serial(port, 115200, parity=serial.PARITY_ODD, timeout=0)
	serial_port = serial.Serial(PORT, 115200, timeout=0)
	
	while 1:
		update = updateSerialData_int()      # Get any new data from the queue
		

		#ttime = ttime + update

		#if (ttime >00 ):
		sendData_void(serial_port)   # Send data for all nodes
		#	ttime = ttime - 1
	

##############################################################################
# Title:     	 updateSerialData_void()
#
# Description:   This function pulls node lists off the queue, if any, and      	
#                then loads them into the apropriate list in serial_data
#
# Inputs:     	 none
# Outputs:    	 none
# Variables:     serial_data - (global) multi-list of all node data
#
# Author:        Brandon Miller
# Last Revised:  1/1/2015
##############################################################################
def updateSerialData_int():
	global serial_data

	update = 0

	while not serialQ.empty():
	
		update = 3

		data = serialQ.get()

		node = getNode_int(data[0])
		
		serial_data[node] = data[:]

		serialQ.task_done()

	return update


##############################################################################
# Title:     	 getNode_int(cmd_str)
#
# Description:   This function extracts the node out of a cmd/node string
#
# Inputs:     	 cmd_str - a sting containing both the CMD and node data
# Outputs:       node - a single digit int of the node from the 
# Variables:     none
#
# Author:        Brandon Miller
# Last Revised:  1/1/2015
##############################################################################
def getNode_int(cmd_str):
	node = int(cmd_str[1])
	return node


##############################################################################
# Title:     	 sendData_void(port)
#
# Description:   This function 
#
# Inputs:     	 port - the serial port to send data out
# Outputs:       node 
# Variables:     none
#
# Author:        Brandon Miller
# Last Revised:  1/1/2015
##############################################################################
def sendData_void(port):

	

	for node in xrange(1, (TOTAL_NODES + 1)):
	#for node in xrange(1, (TOTAL_NODES)):

		#print serial_data[node]

		for index in xrange(len(serial_data[node])):
	
			value = serial_data[node][index]
			value = value.decode('hex')
	
			

			port.write(value)


		transmitDelay()

	
def transmitDelay():
	for x in range(2000):
		for y in range(80):
			pass



#############################################################################
##############################################################################
#
# DC FUNCTIONS
#
##############################################################################
#############################################################################

def init_DC():

	DC_FILE = open('./dc.conf', 'r')  # Open DC File

	dc_line = DC_FILE.readline()      # Read first line
	dc_line = dc_line.strip() 
	dc_line = dc_line.rstrip() 

	setDataType_void(DC_CMD)

	index = 1

	while dc_line: 

		if ( dc_line[0] != '#'
		and  dc_line != '\n' ):
			dc_data = dc_line.split(" ") 

			for x in xrange(0,TOTAL_DC_VALUES):
				setLEDData_void(index, dc_data[x])
				index = index + 1


		

		dc_line = DC_FILE.readline()      # Read first line
		dc_line = dc_line.strip() 
		dc_line = dc_line.rstrip() 

	DC_FILE.close()	
	loadLEDData_void()
	clearLEDData_void()









