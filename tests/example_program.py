from library.main import *

#  Define your global constants here




#  Use tbis to initilize thread and recieve serial port objects
datathread = initTest(True)


# Use this to start collecting data
startCollectingData(datathread)


# Put your test code here


















# Use this to stop collecting data and end test thread
stopCollectingData(datathread)