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
    f = open('testfile.csv', 'wt')
    try:
        writer = csv.writer(f)
        writer.writerow( ('Time','DIN1','DIN2','DIN3','DIN4','DIN5','DIN6','DIN7','DIN8','DOUT0','DOUT1','DOUT2') )
    finally:
        f.close()
    return f

#button press
def button_press(channel):
    print("button pressed on pin 4")


# file writer for data out
def fileWriter(time, dinputs, douputs, ainput, aoutputs, filename):
    rows = len(time)
    file = open('testfile.csv', 'wt')
    writer = csv.writer(file, quoting=csv.QUOTE_ALL)
    outputData = list(zip(time, dinputs, douputs, ainput, aoutputs))
    print(outputData)

    try:
        # for i in range(rows):
        writer.writerows(outputData)
        # print([time[i], dinputs[i], douputs[i], ainput[i], aoutputs[i]])
    finally:
        file.close()


#raw data handler
def handle_data(raw_data):
    TIME = []
    DINPUTS = []
    DOUTPUTS = []
    AINPUTS = []
    AOUTPUTS = []

    for i in range(len(raw_data)):
        data = raw_data[i].split('|')
        TIME.append(data[0].split("\t"))
        DINPUTS.append(data[1].split("\t"))
        DOUTPUTS.append(data[2].split("\t"))
        AINPUTS.append(data[3].split("\t"))
        AOUTPUTS.append(data[4].split("\t"))
    return TIME, DINPUTS,  DOUTPUTS, AINPUTS, AOUTPUTS

    # set up thread generators
def serialHandler(ser, command):
    dataCounter = 0
    rawData = []
    data = {}
    while True:
	print("data counter %d", dataCounter)
	dataDebug = serialPort(ser, command)
	print(dataDebug)
        rawData.append(dataDebug)
        if dataCounter == 2:
            fileWriter(handle_data(rawData))
            dataCounter = 0
            break
        else:
            dataCounter += 1
            print("data counter = %s" % dataCounter)
        time.sleep(.2)


def serialPort(ser, cmd):
    ser.open()
    if ser.isOpen():
        print("in the reading of serial")
        reading = []
        ser.flush()
        ser.write(cmd)
        print("wrote to serial")
        rawData = ser.readline()
        print(rawData)
#            for c in ser.read():
#		print(c)
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
dataThread = threading.Thread(target=serialHandler, args=(ser, "DATA\r"))
dataThread.start()

while True:
    print("test in progress...")
    time.sleep(5)
