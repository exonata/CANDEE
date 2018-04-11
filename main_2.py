#!/usr/bin/python
import threading
import serial
import time
import RPi.GPIO as GPIO
from serial import SerialException
import csv
import logging


serialLock = threading.Lock()
# global commands
def global_define():
    # cmd out settings
    global cmdDATA, cmdDOUT, cmdAOUT
    cmdDATA = "DATA\r"
    cmdDOUT = "DOUT\r"
    cmdAOUT = "AOUT\r"
    # DOUT commands
    global RELAY_0, RELAY_1, RELAY_2, RELAY_3, OFF, ON, TOGGLE
    RELAY_0 = 0  # Add comments/change dout name to match what pin is controlling
    RELAY_1 = 1
    RELAY_2 = 2
    RELAY_3 = 3
    OFF = 0
    ON = 1
    TOGGLE = 2
    global CONNECTED, PORT, BAUD
    # serial definitions
    CONNECTED = False
    PORT = '/dev/ttyS0'
    BAUD = 115200
    global FILEHEAD, FILELOC, FILENAME
    # file setup
    FILELOC = "logs/"
    FILENAME = FILELOC + "testfile_" + time.strftime("%Y%m%d-%H%M%S") + ".csv"
    FILEHEAD = "Time,DIN1,DIN2,DIN3,DIN4,DIN5,DIN6,DIN7,DIN8,DOUT0,DOUT1,DOUT2,DOUT3,AIN0, AIN1,AIN2,AIN3,AOUT0,AOUT1,AOUT2,AOUT3"
    global BUTTON_0
    # pin definitions
    BUTTON_0 = 4

global_define()
# pin setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_0, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # button pin set as input w/ pullup resistor

#main function
#def main(port, baud, filename):


# setup serial port
def initPort(port, baud):
    try:
        ser = serial.Serial(port, baud, timeout=1)
        ser.close()
    except SerialException:
        print("Failed to initalize serial port: " + port)
    return ser

# initiate file and add header
def initLogFile(filename, fileheader):
    f = open(filename, 'w')
    try:
        f.write(fileheader)
	print(filename)
    except Exception as e:
        print("Could not init log file error: ")
    finally:
        f.close()
    return f


#button press
def buttonPress(channel):
    print("button pressed on pin 4")


# file writer for data out
def fileWriter(outputData):
    file = open(FILENAME, 'a')
    print(FILENAME)
    try:
	print("Writing to file")
        file.write(outputData)
    except Exception as e:
        print("Could not init log file error: ")
    finally:
        file.close()
    return file


#raw data handler
def parseData(raw_data):
    data = raw_data.split('|')
    TIME = (data[0].split("\t"))
    DINPUTS = data[1].split("\t")
    DOUTPUTS = data[2].split("\t")
    AINPUTS = data[3].split("\t")
    AINPUTS = AINPUTS[1].split(" ")
    AOUTPUTS = data[4].split("\t")
    output = TIME[1] + "," + DINPUTS[1] + "," + DOUTPUTS[1] + "," + AINPUTS[0] + "," + AINPUTS[1] + "," + AINPUTS[2] + "," + AINPUTS[3] + ","  + AOUTPUTS[1] + "\n"
    return output


# set up thread generators
def dataCollection(ser, command):
    dataCounter = 0
    outputString = ""
    while True:
        rawData = serialTransmission(ser, command)
        parsedData = parseData(rawData)
        outputString = outputString + parsedData
        if dataCounter == 100:
            fileWriter(outputString)
            outputString = ""
        else:
            dataCounter += 1
        time.sleep(.05)

# the only access function to the serial port
def serialTransmission(ser, cmd):
    serialLock.acquire()
    try:
        ser.open()
        ser.flush()
        ser.write(cmd)
        rawData = ser.readline()
	print(rawData)
    except SerialException:
        rawData = "Unable to open serial port"
        print(SerialException)
    finally:
        ser.close()
        serialLock.release()
    return rawData



def DOUT(digitalOutput, cmd):
    error_code = 1 #initial value. This will be changed if everything is alright

    #Error check inputs
    if type(digitalOutput) != int: #check input in an integer
        error_code = 2

    if type(cmd) != str: #check command is a string
        error_code = 3

    if (digitalOutput < 0) or (digitalOutput > 7):
        error_code = 4

    cmd = cmd.upper()  # make it upper case
    if not ((cmd == 'ON') or (cmd == 'OFF') or (cmd == 'TOGGLE')):
        error_code = 5
    send = "DOUT " + str(digitalOutput) + " " + cmd + "\r"
    if error_code == 1: #Send the data to the serial port function
        #returnedData = serialTransmission(ser, send)
        # we dont care about what came back so ignore it
        #if returnedData[0] != 0:
        #    error_code = 6
        error_code = 0
    #print(str(error_code) + "\t" + send)
    return error_code


def AOUT(analogOutput, cmd):
    maxVoltage = 3.3
    error_code = 1 #initial value. This will be changed if everything is alright

    #Error check inputs
    if type(analogOutput) != int: #check input in an integer
        error_code = 2

    if type(cmd) != float: #check command is a float
        error_code = 3

    if (analogOutput < 0) or (analogOutput > 0): # only 1 analog output for now
        error_code = 4

    if (cmd > maxVoltage) or (cmd < 0):
        error_code = 5

    send = "AOUT " + str(analogOutput) + " " + str(cmd) + "\r"

    if error_code == 1: #Send the data to the serial port function
        #returnedData = serialTransmission(ser, send)
        # we dont care about what came back so ignore it
        #if returnedData[0] != 0:
        #    error_code = 6
        error_code = 0

    #print(str(error_code) + "\t" + send)

    return error_code

GPIO.add_event_detect(4, GPIO.FALLING, callback=buttonPress, bouncetime=300)
ser = initPort(PORT, BAUD)
ser.close()
dataThread = threading.Thread(target=dataCollection, args=(ser, "DATA\r"))
dataThread.start()

while True:
    print("test in progress...")
    time.sleep(5)
