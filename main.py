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
fileheader = "Time, DIN1 , DIN2, DIN3, DIN4,DIN5,DIN6,DIN7,DIN8,DOUT0,DOUT1,DOUT2,DOUT3, AIN0, AIN1,AIN2,AIN3,AOUT0,AOUT1,AOUT2,AOUT3\r"


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
    with open('filename', 'wb') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(fileheader)

#button press
def button_press(channel):
    print("button pressed on pin 4")


# file writer for data out
def fileWriter(time, dinputs, douputs, ainput, aoutputs, filename):
    #dataWrite = []
    rows = len(time)
    for i in range(rows):
        print([time[i], dinputs[i], douputs[i], ainput[i], aoutputs[i]])
    # rows = len(time)
    # col_time = 1
    # col_dinputs = 8
    # col_doutputs = 4
    # col_ainputs = 4
    # col_aouputs = 4
    # for i in range(rows):
    #     dataWrite[i][0:col_time] = time[i]
    #     dataWrite[i][col_time:col_dinputs+col_time] = din
    #     # with open(filename, wb) as csv_file:
    #     # csv.writer(csv_file).writerow([for i in range time:])


#raw data handler
def handle_data(raw_data, dataCounter):
    TIME = ""
    DINPUTS = ""
    DOUTPUTS = ""
    AINPUTS = ""
    AOUTPUTS = ""
    data = ""
    print(TIMcE)
    print(DINPUTS)
    for i in range(len(raw_data)):
        data.insert(i,raw_data[i].split('|'))
	print(data)
	print(data[0])
        TIME.insert(data[0][0].split("\t"))
        DINPUTS[i].append(data[1].split("\t"))
        DOUTPUTS[i].append(data[2].split("\t"))
        AINPUTS[i].append(data[3].split("\t"))
        AOUTPUTS[i].append(data[4].split("\t"))
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
            data = handle_data(rawData, dataCounter)
            fileWriter(data)
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
