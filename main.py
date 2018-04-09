#!/usr/bin/python
import threading
import serial
import time
import RPi.GPIO as GPIO
import csv
import logging

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

# serial definitions
connected = False
port = '/dev/ttyS0'
baud = 115200

# file setup
filelocation = "/logs/"
filename = filelocation + "testfile_" + str(time.time()) + ".csv"
fileheader = "Time, DIN1 , DIN2, DIN3, DIN4,DIN5,DIN6,DIN7,DIN8,DOUT0,DOUT1,DOUT2,DOUT3, AIN0, AIN1,AIN2,AIN3,AOUT0,AOUT1,AOUT2,AOUT3"


# pin definitions
buttonPin = 4

# pin setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # button pin set as input w/ pullup resistor

#main function
#def main(port, baud, filename):


# setup serial port
def init_port(port, baud):
    return serial.Serial(port, baud, timeout=1)

# initiate file and add header
def init_logFile(filename, fileheader):
    f = open('testfile.csv', 'w')
    try:
        f.write(fileheader)
    finally:
        f.close()
    return f

#button press
def button_press(channel):
    print("button pressed on pin 4")


# file writer for data out
def fileWriter(outputData):
    file = open('testfile.csv', 'a')
    try:
        file.write(outputData)
    finally:
        file.close()


#raw data handler
def handle_data(raw_data):
    data = raw_data.split('|')
    print(data)
    TIME = (data[0].split("\t"))
    DINPUTS = data[1].split("\t")
    DOUTPUTS = data[2].split("\t")
    AINPUTS = data[3].split("\t")
    AINPUTS = AINPUTS[1].split(" ")
    AOUTPUTS = data[4].split("\t")
    print(AINPUTS)
    output = TIME[1] + "," + DINPUTS[1] + "," + DOUTPUTS[1] + "," + AINPUTS[0] + "," + AINPUTS[1] + "," + AINPUTS[2] + "," + AINPUTS[3] + ","  + AOUTPUTS[1] + "\n"
    return output


# set up thread generators
def dataCollection(ser, command):
    dataCounter = 0
    outputString = ""
    while True:
        dataDebug = serialPort(ser, command)
#       print(dataDebug)
        rawData = handle_data(dataDebug)
        outputString = outputString + rawData
        if dataCounter == 2:
            fileWriter(outputString)
            outputString = ""
            rawData = ""
        else:
            dataCounter += 1
        time.sleep(.2)

# the only access function to the serial port
def serialPort(ser, cmd):
    ser.open()
    if ser.isOpen():
        ser.flush()
        ser.write(cmd)
        rawData = ser.readline()
#            for c in ser.read():
#		        print(c)
#                if c == '*':
#                    ser.close()
#                    break
#                else:
#                    reading.append(c)
#            rawData = ''.join(reading)
        ser.close()
    else:
        rawData = "error in serial command"
        ser.close()
    return rawData



def DOUT(ser, cmd):
    rawData = serialPort(ser, cmd)
    return rawData          # add data handle for this info


def AOUT(ser, cmd):
    rawData = serialPort(ser, cmd)
    return rawData


GPIO.add_event_detect(buttonPin, GPIO.FALLING, callback=button_press, bouncetime=300)
ser = init_port(port, baud)
ser.close()
dataThread = threading.Thread(target=dataCollection, args=(ser, "DATA\r"))
dataThread.start()

while True:
    print("test in progress...")
    time.sleep(5)
