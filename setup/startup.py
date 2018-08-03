
# currently lives at /etc/profile

import RPi.GPIO as GPIO
import time
import os
import subprocess
import signal
import serial



#adjust for where your switch is connected
ON = False
buttonPin = 4
s = serial.Serial("/dev/ttyS0", 38400, timeout=1)
rpistr = " python /home/pi/SKYFLOW_TESTSTAND/simple_test.py"


def getButtonVal(ser):
    ser.reset_input_buffer()  # clear input buffer
    ser.reset_output_buffer()  # clear output buffer
    ser.write("DATA\r")  # write desired command
    raw_data = ser.readline()
    data = raw_data.split("|")
    din = data[1].split("\t")  # split time data on \t
    parsed_din = din[1]  # generate empty list
    button = parsed_din[5]
    return button


def toggleSolenoid(ser):
    ser.write("DOUT 1 1\r")
    ser.write("DOUT 1 0\r")


def isButtonOn(ser):
    button = getButtonVal(ser)
    if button == 0:
        return True
    else:
        return False


while True:
    #assuming the script to call is long enough we can ignore bouncing

    if isButtonOn(s):
        time.sleep(.05)
        if isButtonOn(s):
            if not ON:
                #this is the script that will be called (as root)
                toggleSolenoid(s)
                s.close()
                p = subprocess.Popen(rpistr, shell=True, preexec_fn=os.setsid)
                ON = True
                print("On value", ON)
                time.sleep(1)
            else:
                os.killpg(p.pid, signal.SIGTERM)
                ON = False
                s.write("DOUT 0 0\r")
                s.write("DOUT 1 0\r")
                s.write("ABS0 0\r")
                s.close()
                print("On value", ON)
                time.sleep(1)
