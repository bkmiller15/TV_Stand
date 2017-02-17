from threading import Thread
import time
import serial
from Queue import Queue


TOTAL_NODES = 2
PORT = '/dev/ttyUSB0'

TOTAL_CMD_PACKETS = 1
TOTAL_GS_CDATA_PACKETS = 15
TOTAL_DC_CDATA_PACKETS = 12
TOTAL_GS_SDATA_PACKETS = 24
TOTAL_DC_SDATA_PACKETS = 12



serialQ = Queue()

led_data = []
led_data.append('00')  # First string for cmd data
for leds in xrange(15 * TOTAL_NODES):
	color_data.append('00')

queue_data = []
for node in xrange(TOTAL_NODES):
	serial_data.append([])

serial_data = []
for node in xrange(TOTAL_NODES):
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

	if (index > 0 and index < len(led_data)):
		led_data[index] = data


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
	qdata = color_data
	serialQ.put(qdata)

	serialQ.join()  # HOLD here until all data on the queue is processed










def convGS(cdata):
	global led_data
	global queue_data


	for node in xrange(TOTAL_NODES):

		queue_data = []
		queue_data.append


		cmd_node = (node + 1) + cdata[0]
		cmd_node = str(cmd_node)
		if (len(cmd_node) < 2):            # IF value has less than 3 chars:
			cmd_node = cmd_node.zfill(2)   # Pad with zeros
		serial_data[node][0] = cmd_node

		serial_index = TOTAL_GS_SDATA_PACKETS

		for x in xrange(((node * TOTAL_GS_CDATA_PACKETS) + TOTAL_CMD_PACKETS), (((node + 1) * TOTAL_GS_CDATA_PACKETS) + TOTAL_CMD_PACKETS), 2):                  # Must be reversed to get right order

			# Takes string value [0-255] and converts it to a 12 bit value [0-4096]	
			print cdata
			rgbValue1 = cdata[x]
			if (x == ((((node + 1) * TOTAL_GS_CDATA_PACKETS) + TOTAL_CMD_PACKETS)-1) ):
				rgbValue2 = 0
			else:
				rgbValue2 = cdata[x+1]

			rgbValue1 = convColor2Hex(rgbValue1)
			rgbValue2 = convColor2Hex(rgbValue2)

			serial_data[node][serial_index] = rgbValue1[0] + rgbValue1[1]
			serial_data[node][serial_index - 1] = rgbValue1[2] + rgbValue2[0]
			serial_data[node][serial_index - 2] = rgbValue2[1] + rgbValue2[2]
			serial_index = serial_index - 3
		
		


def convColor2Hex_str(num_int):
	print num

	num = int(num**1.501)

	# Convert int to a binary stringo
	num = bin(num)
	num = num.replace("0b","")   # get rid of the 0x in string	
	num = num.zfill(12)
	num = num[::-1]
	num = hex(int(num, 2))
	num = num.replace("0x","")   # get rid of the 0x in string

	if (len(num) < 3):            # IF value has less than 3 chars:
		num = num.zfill(3)   # Pad with zeros
	elif (len(num) > 3):          # IF value has more than 3 chars:
		num = 'FFF'               # Set to Max

	return num





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
		updateSerialData_void()      # Get any new data from the queue
		sendData_void(serial_port)   # Send data for all nodes
	

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
def updateSerialData_void():
	global serial_data

	while not serialQ.empty():
	
		data = serialQ.get()

		node = getNode_int(data[0])
		
		serial_data[node] = data[:]

		serialQ.task_done()


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

		for index in xrange(len(serial_data[node]):
	
			value = serial_data[current_node][index]
			value = value.decode('hex')
	
			port.write(value)


		transmitDelay()

	
def transmitDelay():
	for x in range(2000):
		for y in range(80):
			pass
