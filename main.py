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
fileheader = "Time, DIN1 , DIN2, DIN3, DIN4,DIN5,DIN6,DIN7,DIN8,DOUT0,DOUT1,DOUT2,DOUT3, AIN0, AIN0,AIN0,AIN0,AOUT0,AOUT0,AOUT0,AOUT0"


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
    TIME = []
    DINPUTS = []
    DOUTPUTS = []
    AINPUTS = []
    AOUTPUTS = []
    print(raw_data)
    for i in range(dataCounter):
        data = raw_data.split('|')
        TIME[:][i] = data[0].split("\t")
        DINPUTS[:][i] = data[1].split("\t")
        DOUTPUTS[:][i] = data[2].split("\t")
        AINPUTS[:][i] = data[3].split("\t")
        AOUTPUTS[:][i] = data[4].split("\t")
    return {TIME, DINPUTS,  DOUTPUTS, AINPUTS, AOUTPUTS}

    # set up thread generators
def serialHandler(ser, command):
    dataCounter = 0
    while True:
        rawData = serialPort(ser, command)
        if dataCounter == 1000:
            fileWriter(handle_data(rawData, dataCounter))
            dataCounter = 0
            break
        else:
            dataCounter += 1
        time.sleep(.2)


def serialPort(ser, cmd):
    if ser.isOpen():
        try:
            reading = []
            ser.flush()
            ser.write(cmd)
            for c in ser.read():
                if c == '*':
                    ser.close()
                    break
                else:
                    reading.append(c)
            rawData = ''.join(reading)
        except:
            rawData = "Error in serial command"
            print("Error in serial command")
    else:
        rawData = "error in serial command"
    return rawData



def DOUT(ser, cmd):
    rawData = serialPort(ser, cmd)
    return rawData          # add data handle for this info


def AOUT(ser, cmd):
    rawData = serialPort(ser, cmd)
    return rawData


GPIO.add_event_detect(buttonPin, GPIO.FALLING, callback=button_press, bouncetime=300)

while True:
    ser = init_port(port, baud)
    dataThread = threading.Thread(target=serialHandler, args=(ser, "DATA\r"))
    dataThread.start()
    print("test in progress...")
    time.sleep(5)