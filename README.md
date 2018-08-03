


All tests should be written and saved in the /tests directory
All logs saved in /logs directory



Please review /tests/example_program.py for base test
    1. How to initialize the test
    2. What libraries to import
    3. How to close the data collection and exit your program

#EXAMPLE TEST:
i = 20 # runt he test 20 times

while (i >= 0):
	#Assumes the bottle is upright when starting test
	POS0(0) #set position to 0 degrees
	ABS0(180)
	while (not MOTION_COMPLETE): #wait for motion to on stepper to complete
	wait(3.5) #wait 3.5 seconds
	ABS0(0)  #move the motor back up
	while (not MOTION_COMPLETE): #wait for motion to on stepper to complete
	wait(1) #wait 3.5 seconds
	i = i+1 #increment tect counter








# Initalize test and set file name and setup all I/O.  Will return your data collection python thread (use this thread
#  to start and stop collection of data
        #  testThread = initTest()


#  To start data collection for the test, and to initialize the values from the device
        #  startCollectingData(testThread)


# To stop collecting data in the background, use this function with the name of your data collection thread
    # being passed to the function
        # stopCollectingData(testThread)

#  To get the values of any I/O on the system, use these functions to return their current value
#  getTime()  # return timestamp of most recent data collected
#  getDIN(channel)  #  Send the the DIN channel you want to read the value you of
#  getDOUT(channel) # Send the the DOUT channel you want to read the value you of
#  getAIN(channel) # Send the AIN channel you want to read the current value of
#  getAOUT(channel) # Send the AOUT channel you want to read the current value of
#  getSTEP0(info) #  Send what information you want to recieve from the Stepper motor
                        # 0 : Is current command completed? 1:YES, 0: NO
                        # 1: Current position of stepper motor
                        # 2: Desired position of stepper motor
                        # 3: Current velocity of stepper motor
#  getACC0(channel) #  Send what accel/gyro value you want to recieve
                        # 0 : X-Axis
                        # 1: Y-Axis
                        # 2: Z-Axis
                        # 3: Gs
#  getSCALE() # Returns current value of the scale in grams


#  Send ON, OFF, or TOGGLE command to digital out pin of your choice
#  DOUT(digitalOutput, cmd)
        #  DOUT(1, TOGGLE) #toggle output 1 (if its on, turn it off. If its off, turn it on)
        #  DOUT(0, OFF) #turn off output 0)

#  Run the pump to refill bottle with desired amount of liquid (in grams)
#  runPump(dispensed)
        #  runPump(253.6)  # Refill bottle with 253.6 grams of liquid


#  Open the Skyflow valve on command
        #  OPEN()  # Opening the skyflow valve


#  Close the Skyflow valve on command
        #  CLOSE()  #  Closing the skyflow valve

#  Send desired analog out voltage to desired analog pin.  Cand send float or ints
#  AOUT(analogOutput, cmd)
        #  AOUT(0, 2.32)  #  Set analog voltage to 2.32 V
        #  AOUT(0, 1)  #  Set analog voltage to 1.0 V

#  Set the position of the stepper motor to an absolute degree value based off of its absolute zero position from 0-360 degrees
#  ABS0(targetDegree)
        #  ABS0(350)  #  Set the position of the stepper motor to 350 degrees based off of its starting position
        #  ABS0(0)  #  Set position of the stepper motor to its zero position

#  Set the zero position of the stepper motor
#  POS0(targetDegree)
        #


#  Set an incremental position of the stepper motor based off of its current position
#  INC0(incTargetDegree)
        #  INCO(10)  #  Move the stepper motor position 10 degrees from current position
        #  INCO(-5)  #  Move the stepper motor 5 degrees ** clockwise counter clockwise?


#  Set the desired velocity of the stepper motor from ** to ** degrees/second.  Step up speed gradually, in ** increments
#  VEL0(degPerSecond, ser)
        #  VELO(500)  # Set speed to 500 deg/sec
        #  VEL0(1000)  #  Step up speed of stepper to 1000 deg/sec
