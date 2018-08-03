from library.main import *

#Define your global constants here




#  Use tbis to initilize thread and recieve serial port objects
[datathread, mbedserial, usbserial] = initTest()


# Use this to start collecting data
startCollectingData(datathread)


# Put your test code here

while(1):
	





















# Use this to stop collecting data and end test thread
stopCollectingData(datathread)
