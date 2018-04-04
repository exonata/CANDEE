#!/usr/bin/python

import threading
import serial
import time
import RPi.GPIO as GPIO
import csv
import logging

#serial definitions
connected = False
port = '/dev/ttyS0'
baud = 115200

#pin definitions
buttonPin = 4

#pin setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP) #button pin set as input w/ pullup

#setup serial port
def init_port(port, baud):
	return serial.Serial(port, baud, timeout=1)

#raw data handleer
def handle_data(raw_data, tag):
	print(raw_data)
	data = raw_data.split('|')
	TIME  = data[0].split("\t")
	DINPUTS = data[1].split("\t")
	DOUTPUTS = data[2].split("\t")
	AINPUTS = data[3].split("\t")
	AOUTPUTS = data[4].split("\t")
	print(TIME)
	print(DINPUTS)
	print(DOUTPUTS)
	print(AINPUTS)
	print(AOUTPUTS)


	print(data)


#set up thread generators
def serialHandler(ser, command):
	while True:
		ser.flush()
		ser.write(command)
		reading = ser.readline()
		if t reading.endswith("*")
			reading2 = ser.readline()
		handle_data(reading, command)
		time.sleep(2)

def serialCommander(ser, command):
	ser.flush()
	ser.write(command)
	reading = ser.readline()
	handle_data(reading, command)




ser = init_port(port, baud)
dataThread = threading.Thread(target=serialHandler, args=(ser, "DATA\r"))
dataThread.start()

while True:
	print("test in progress...")
	time.sleep(5)
