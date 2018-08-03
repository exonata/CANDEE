#  Test to see if stepper is in current position

from library.main import *

#  Define your global constants here


def isMotionComplete():
    while True:
        if getSTEP0(0) == 1:
            break
        else:
            time.sleep(0.01)


#  Use tbis to initilize thread and recieve serial port objects
datathread = initTest(False)

# Use this to start collecting data
startCollectingData(datathread)
wait(5)
print("starting test")

# Put your test code here
ABS0(0)
print("checking if motion is complete")
isMotionComplete()
print("centered at 0")
time.sleep(5)
ABS0(360)
isMotionComplete()
print("moved to 360")
time.sleep(5)
print("starting phase 2")
test = 0
while test < 3:
    INC0(180)
    isMotionComplete()
    print("Step complete")
    time.sleep(5)
    test += 1


# Use this to stop collecting data and end test thread
stopCollectingData(datathread)
