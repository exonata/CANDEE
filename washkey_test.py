from library.main import *

#  Define your global constants here




#  Use this to initialize thread and receive serial port objects
#  The background thread that will poll the mbed for data
datathread = initTest(False)

# Start collecting data
startCollectingData(datathread)


# Put your test code here
while True:
    spoutOPEN()
    wait(1)
    spoutCLOSE()
    wait(1)


# Use this to stop collecting data and end test thread
stopCollectingData(datathread)
