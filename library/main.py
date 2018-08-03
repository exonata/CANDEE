#!/usr/bin/python
import threading
import serial
import time
import RPi.GPIO as GPIO
from serial import SerialException
from library.pinDefinitions import *


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Date last modified: 4/10/18                                                                                         ~~
# Original  Author: Renata Smith                                                                                      ~~
# Last Author: Renata Smith                                                                                           ~~
#                                                                                                                     ~~
# Function: global_define():                                                                                          ~~
# Description: Define global variables for all functions                                                              ~~
# Parameter: None                                                                                                     ~~
# Example: global_define()                                                                                            ~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def global_define():
# cmd out settings
    global cmdDATA, cmdDOUT, cmdAOUT, cmdSCALE
    cmdDATA = "DATA\r"
    cmdDOUT = "DOUT\r"
    cmdAOUT = "AOUT\r"
    cmdSCALE = "SI\r\n"
# serial definitions
    global PORT, BAUD, USBPORT, FILELOC, FILEHEAD
    PORT = '/dev/ttyS0'
    USBPORT = '/dev/ttyUSB0'
    BAUD = 38400
# pin definitions
    global r_BUTTON_0
    r_BUTTON_0 = 4
    global RUN
    RUN = True

# Global variables for
USBSERIAL = None
MBEDSERIAL = None

# Master Data lists
TIME = []
DINPUTS = []
DOUTPUTS = []
AINPUTS = []
AOUTPUTS = []
STEP0 = []
ACC0 = []
SCALE = []


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Date last modified: 4/10/18                                                                                         ~~
# Original  Author: Renata Smith                                                                                      ~~
# Last Author: Renata Smith                                                                                           ~~
#                                                                                                                     ~~
# Function: wait(seconds)                                                                                             ~~
# Description: Initiate a system sleep                                                                                ~~
# Parameter: seconds to wait (Type: Float)                                                                            ~~
# Return: None                                                                                                        ~~
#                                                                                                                     ~~
# Example 0: wait(0.1)                                                                                                ~~
#                                                                                                                     ~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def wait(secs):
    time.sleep(secs)



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Date last modified: 4/10/18                                                 ********************                                         ~~
# Original  Author: Renata Smith                                                                                      ~~
# Last Author: Renata Smith                                                                                           ~~
#                                                                                                                     ~~
# Function: checkStopButton()                                                                                             ~~
# Description: Initiate a system sleep                                                                                ~~
# Parameter: seconds to wait (Type: Float)                                                                            ~~
# Return: None                                                                                                        ~~
#                                                                                                                     ~~
# Example 0: wait(0.1)                                                                                                ~~
#                                                                                                                     ~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def checkStopButton():
    check = True
    while check:
        if getDIN(5) == 0:
            ABS0(0)




# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Date last modified: 4/10/18                                                                                         ~~
# Original  Author: Renata Smith                                                                                      ~~
# Last Author: Renata Smith                                                                                           ~~
#                                                                                                                     ~~
# Function: initTest(collectData)                                                                                     ~~
# Description: Initilize test, including opening serial port, initilizing log file, and setting up threading locks    ~~
# Parameter 0: collectData: Boolean flag from user to determine if data is written to file or not                     ~~
#                                                                                                                     ~~
# Example 0: initTest(True) # collect data during this test sequence                                                  ~~
#                                                                                                                     ~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def initTest(collectData):
    global_define()  # define global
    mbedserial = initPort(PORT, BAUD) # define mbed serial object
    usbserial = initPort(USBPORT, BAUD)  # define scale serial object
    global MBEDSERIAL, USBSERIAL # declare and set the global serial objects
    MBEDSERIAL = mbedserial[1]
    USBSERIAL = usbserial[1]
    global serialLock  # declare global serialLock object
    serialLock = threading.Lock()  # define threading lock
    datathread = threading.Thread(target=dataCollection, args=(cmdDATA, cmdSCALE, collectData))  # call data collection thread
    return datathread


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Date last modified: 4/10/18                                                                                         ~~
# Original  Author: Renata Smith                                                                                      ~~
# Last Author: Renata Smith                                                                                           ~~
#                                                                                                                     ~~
# Function: startCollectingData(threadName)                                                                           ~~
# Description: start data collection thread                                                                           ~~
# Parameter 0: threadName (Type: thread object)                                                                       ~~
# Return: errorcode (Type: int)                                                                                       ~~
# Error Codes 0: Everything OK                                                                                        ~~
#             1: Error starting thread                                                                                ~~
# Example 0: startCollectingData(dataThread)                                                                          ~~
#                                                                                                                     ~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def startCollectingData(threadName):
    errorcode = 0
    try:
        threadName.start()  # start named thread
    except:
        errorcode = 1
    finally:
        return errorcode


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Date last modified: 4/10/18                                                                                         ~~
# Original  Author: Renata Smith                                                                                      ~~
# Last Author: Renata Smith                                                                                           ~~
#                                                                                                                     ~~
# Function: stopCollectingData(threadName)                                                                            ~~
# Description: stop data collection thread and ensure that all data is written to file                                ~~
# Parameter 0: threadName (Type: thread object)                                                                       ~~
# Return: errorcode (Type: int)                                                                                       ~~
# Error Codes 0: Everything OK                                                                                        ~~
#             1: Error starting thread                                                                                ~~
# Example 0: stopCollectingData(dataThread)                                                                           ~~
#                                                                                                                     ~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def stopCollectingData(threadName):
    global RUN  #  call global variable RUN
    RUN = False  # Set RUN to false, will block data collection thread while loop
    errorcode = 0
    try:
        threadName.join()  #  Join thread with main process
    except:
        errorcode = 1
    finally:
        return errorcode


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Date last modified: 4/10/18                                                                                         ~~
# Original  Author: Renata Smith                                                                                      ~~
# Last Author: Renata Smith                                                                                           ~~
#                                                                                                                     ~~
# Function: dataCollection(ser, command, collectData)                                                                 ~~
# Description: thread generators for serial port polling and data collection                                          ~~
# Parameter 0: mbed serial port (Type: String)                                                                        ~~
#           1: usb serial port (Type: string)                                                                         ~~
#           1: boolean for collecting data (Type: bool)                                                               ~~
# Return: Nothing                                                                                                     ~~
#                                                                                                                     ~~
# Example 0: dataCollection(mbed_ser_obj,scale_ser_obj, True)                                                         ~~
#                                                                                                                     ~~
#                                                                                                                     ~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def dataCollection(cmddata, cmdusb, collectData):
    dataCounter = 0  # init counter for data
    outputString = ""  # init output string as empty
    if collectData:  # if user has flagged for data collection, init files
        filename = initLogName()
        initLogFile(filename, FILEHEAD)
    else:
        filename = ""  # make filename blank if user does not flag for data collection
    while RUN:  # while global variable RUN is still True (altered by stopDataCollection function
        raw_data = serialTransmission(cmddata)  # get raw data from serial port
        raw_scale = usbTransmission(cmdusb)
        parsedData = parseData(raw_data[1], raw_scale[1])  # have raw data parsed and assigned to global variables
        outputString = outputString + parsedData  # add parsed and formatted data added to output string
        if dataCounter == 100 & collectData == True:  # if user wants data collected & 100 points of data have been collected
            fileWriter(outputString, filename)  # write output string to file
            outputString = ""  # reset output string to blank
            dataCounter = 0  # rollback dataCounter to 0
        elif collectData == False & dataCounter == 100:  # if user does not want data to be collected, throw it away
            outputString = ""
            dataCounter = 0
        else:  # or just add to data counter
            dataCounter += 1
        time.sleep(.01)  # sleep for 10 msec inbetween each probe for data
    if collectData:  # if collecting data and thread quiting, write last data to file and close it
        fileWriter(outputString, filename)
        print("Logging test complete")
    else:
        print("Test complete")


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Date last modified: 4/10/18                                                                                         ~~
# Original  Author: Renata Smith                                                                                      ~~
# Last Author: Renata Smith                                                                                           ~~
#                                                                                                                     ~~
# Function: initPort(port, baud)                                                                                      ~~
# Description: Setup serial port                                                                                      ~~
# Parameter 0: Serial port address (Type: String)                                                                     ~~
#          1: Baud Rate (Type: int)                                                                                   ~~
# Return: [error code, serialport](see below for detail)                                                              ~~
# Error Codes 0: Everything OK                                                                                        ~~
#             1: Error opening the serial port                                                                        ~~
#                                                                                                                     ~~
# Example 0: initPort("/dev/ttyS0", 115200)                                                                           ~~
#                                                                                                                     ~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def initPort(port, baud):
    errorcode = 0
    try:
        ser = serial.Serial(port, baud, timeout=1)  # try to open serial port with defined port and baud rate
        ser.close()  # close the now open port
    except SerialException:  # if you experience a serial exception while opening the port, throw error
        print("Failed to initalize serial port: " + port)
        errorcode = 1
        ser = 1
    return [errorcode, ser]

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Date last modified: 4/10/18                                                                                         ~~
# Original  Author: Renata Smith                                                                                      ~~
# Last Author: Renata Smith                                                                                           ~~
#                                                                                                                     ~~
# Function: initLogName()                                                                                             ~~
# Description: initiate filename based off current time                                                               ~~
# Parameter None                                                                                                      ~~
# Return: filename (Type: string)                                                                                     ~~
#                                                                                                                     ~~
# Example 0: initLogFile()                                                                                           ~~
#                                                                                                                     ~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def initLogName():
    filename = FILELOC + "testfile_" + time.strftime("%Y%m%d-%H%M%S") + ".csv"  # stitch together file name
    return filename

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Date last modified: 4/10/18                                                                                         ~~
# Original  Author: Renata Smith                                                                                      ~~
# Last Author: Renata Smith                                                                                           ~~
#                                                                                                                     ~~
# Function: initLogFile(filename, fileheader)                                                                         ~~
# Description: initiate file and add header                                                                           ~~
# Parameter 0: filename (Type: String)                                                                                ~~
#          1:fileheader (Type: String)                                                                                ~~
# Return: intialize file object                                                                                       ~~
#                                                                                                                     ~~
# Example 0: initLogFile("/logs/testfile.csv", "Val1, Val2, Val3\r"                                                   ~~
#                                                                                                                     ~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def initLogFile(filename, fileheader):
    f = open(filename, 'w')  # file, set it to "write over" to clear any junk in it
    fscale = open(scaleLogName, 'w')
    fmbed = open(mbedLogName, 'w')
    try:
        f.write(fileheader)  # write file header to file
        fscale.write("")
        fmbed.write("")
        print(filename)  # print filename to file
    except Exception as e:  # if error thrown when opening print error to terminal
        print("Could not init log file error: ", e)
    finally:
        f.close()  # close file when finished
        fscale.close()
        fmbed.close()
    return f  # return file object



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Date last modified: 4/10/18                                                                                         ~~
# Original  Author: Renata Smith                                                                                      ~~
# Last Author: Renata Smith                                                                                           ~~
#                                                                                                                     ~~
# Function: fileWriter(outputData)                                                                                    ~~
# Description: append file object with data string                                                                    ~~
# Parameter 0: outputData (Type: String)                                                                              ~~
# Return: initialize file object                                                                                      ~~
# Error Codes 0: Everything OK                                                                                        ~~
#             1: Error writing to file                                                                                ~~
# Example 0: fileWriter(dataOut)                                                                                      ~~
#                                                                                                                     ~~
#                                                                                                                     ~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def fileWriter(outputData, fileName):
    errorCode = 0
    file = open(fileName, 'a')  # set file writing to "append" so that you add to current file, not erase
    try:
        print("Writing to file")  #useful to note if you are writing to file during testing
        file.write(outputData)  # write formatted data to file
    except Exception as e:
        errorCode = 1
        print("Could not init log file error: ", e)  # if error when file writing, print out
    finally:
        file.close()   # close file
    return errorCode


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Date last modified: 4/10/18                                                                                         ~~
# Original  Author: Renata Smith                                                                                      ~~
# Last Author: Renata Smith                                                                                           ~~
#                                                                                                                     ~~
# Function: parseData(raw_data, raw_scale)                                                                            ~~
# Description: Parse raw serial Data from MBed into string                                                            ~~
# Parameter 0: rawData (Type: String)                                                                                 ~~
#           1: rawData (Type: String)                                                                                 ~~
# Return: Formatted output string (Type: String)                                                                      ~~
# Error Codes 0: Everything OK                                                                                        ~~
#                                                                                                                     ~~
# Example 0: parseData("mbed data", "scale data")                                                                     ~~
#                                                                                                                     ~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def parseData(raw_data, raw_scale):
    print(raw_scale)  # debug code
    print(raw_data)  # debug code
    try:
        if raw_data != "***":  # if not throwaway data from mbed, prep for parsing
            data = raw_data.split('|')  # split data into list by |
            timestamp = parseTime(data[0])  # send data to inividual parse functions
            din = parseDinputs(data[1])
            dout = parseDouputs(data[2])
            ain = parseAinputs(data[3])
            aout = parseAoutputs(data[4])
            step0 = parseStep(data[5])
            if raw_scale != "***":  # if scale is not throwaway data
                scale = parseScale(raw_scale)  # parse scale data
            else:
                scale = ""  # set scale to blank
            output = timestamp + din + dout + ain + aout + step0 + scale
            if data[6] != "*":  # check to see if mbed data includes acceleromenter
                acc0 = parseAcc(data[6]) # parse acc data
                output = output + acc0[:-1] + "\n"  # add to output string, add carrige return
            else:
                output = output[:-1] + "\n"  # if no acc data, add newline to output data
        else:
            output = ""  # set output to blank if data is not valid
    except:
        output = ""
    return output

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Date last modified: 4/10/18                                                                                         ~~
# Original  Author: Renata Smith                                                                                      ~~
# Last Author: Renata Smith                                                                                           ~~
#                                                                                                                     ~~
# Function: parse*DATA*(raw_DATA)                                                                                     ~~
# Description: parse all data lists, set global reference val, return string for output                               ~~
# Parameter 0: raw data from serial port                                                                              ~~
# Return: DATA_string (Type: string)                                                                                  ~~
# Error Codes 0: Everything OK                                                                                        ~~
#             1: Error starting thread                                                                                ~~
# Example 0: startCollectingData(dataThread                                                                           ~~
#                                                                                                                     ~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def parseTime(raw_time):
    timestamp = raw_time.split("\t")  # split time data on \t
    time_string = timestamp[1] + ","  # add "," to end of time stamp to return
    setTime(timestamp[1])  # send timestamp val to setTime function (updates global variables)
    return time_string


def parseDinputs(raw_din):
    din = raw_din.split("\t")   # split time data on \t
    parsed_din = []  # generate empty list
    din_string = ""  # generate empty string
    for i in din[1]:  # iterate through characters in din to seperate them
        parsed_din.append(i)  # add to d input list, one character at a time
        din_string = din_string + i + ","  # generate output string, seperate each value with ","
    setDIN(parsed_din)  # send din list to set function
    return din_string


def parseDouputs(raw_dout):
    dout= raw_dout.split("\t")  # split time data on \t
    parsed_dout = []  # generate empty list
    dout_string = ""  # generate empty string
    for i in dout[1]:  # iterate through characters in din to seperate them
        parsed_dout.append(i)
        dout_string = dout_string + i + ","  # generate output string, seperate each value with ","
    setDOUT(parsed_dout)
    return dout_string


def parseAinputs(raw_ain):
    ain_string = ""
    ain = raw_ain.split("\t")
    parsed_ain = ain[1].split(" ")
    for i in parsed_ain:
        ain_string = ain_string + i + ","
    setAIN(parsed_ain)
    return ain_string


def parseAoutputs(raw_aout):
    aout_string = ""
    aout = raw_aout.split("\t")
    parsed_aout = aout[1].split(" ")
    for i in parsed_aout:
        aout_string = aout_string + i + ","
    setAOUT(parsed_aout)
    return aout_string


def parseStep(raw_step):
    step_string = ""
    step = raw_step.split("\t")
    parsed_step = step[1].split(" ")
    for i in parsed_step:
        step_string = step_string + i + ","
    setSTEP0(parsed_step)
    return step_string


def parseAcc(raw_acc):
    acc_string = ""
    acc = raw_acc.split("\t")
    parsed_acc = acc[1].split(" ")
    for i in parsed_acc:
        acc_string = acc_string + i + ","
    setACC0(parsed_acc)
    return acc_string


def parseScale(raw_scale):
    scale_string = ""
    scale = raw_scale.split(" ")
    scale = list(filter(None, scale))
    if scale:
        setSCALE(scale[0])
        scale_string = scale[0] + ","
        return scale_string
    else:
        scale_string = str(getSCALE()) + ","
        return scale_string

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Date last modified: 4/10/18                                                                                         ~~
# Original  Author: Renata Smith                                                                                      ~~
# Last Author: Renata Smith                                                                                           ~~
#                                                                                                                     ~~
# Function: setDATA(dataVal)                                                                                          ~~
# Description: Update global list containing data                                                                     ~~
# Parameter 0: threadName (Type: thread object)                                                                       ~~
# Return: errorcode (Type: int)                                                                                       ~~
# Error Codes 0: Everything OK                                                                                        ~~
#             1: Error starting thread                                                                                ~~
# Example 0: startCollectingData(dataThread                                                                           ~~
#                                                                                                                     ~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def setTime(timestamp):
    global TIME
    del TIME[:]
    TIME.append(timestamp[:])


def getTime():
    return int(TIME[0])


def setDIN(din):
    global DINPUTS
    del DINPUTS[:]
    DINPUTS = din[:]
    return 0


def getDIN(channel):
    return int(DINPUTS[channel])


def setDOUT(dout):
    global DOUTPUTS
    del DOUTPUTS[:]
    DOUTPUTS = dout[:]
    return 0


def getDOUT(channel):
    return int(DOUTPUTS[channel])


def setAIN(ain):
    global AINPUTS
    del AINPUTS[:]
    AINPUTS = ain[:]
    return 0


def getAIN(channel):
    return float(AINPUTS[channel])


def setAOUT(aout):
    global AOUTPUTS
    del AOUTPUTS[:]
    AOUTPUTS = aout[:]
    return 0


def getAOUT(channel):
    return float(AOUTPUTS[channel])


def setSTEP0(step):
    global STEP0
    del STEP0[:]
    STEP0 = step[:]
    return 0


def getSTEP0(channel):
    if channel == 0:
        return int(STEP0[channel])
    else:
        return float(STEP0[channel])


def setACC0(acc):
    global ACC0
    del ACC0[:]
    ACC0 = acc[:]
    return 0


def getACC0(channel):
    return float(ACC0[channel])


def setSCALE(scale):
    global SCALE
    if scale != "":
        SCALE = scale[:]
    return 0


def getSCALE():
    return float(SCALE)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Date last modified: 4/10/18                                                                                         ~~
# Original  Author: Renata Smith                                                                                      ~~
# Last Author: Renata Smith                                                                                           ~~
#                                                                                                                     ~~
# Function: serialTransmission(cmd)                                                                                   ~~
# Description: the only access function to the serial port                                                            ~~
# Parameter 0: desired serial port (Type: String)                                                                     ~~
#           1: serial buffer out (Type: String)                                                                       ~~
# Return: [errorcode, rawData] (Type: [int, String])                                                                  ~~
# Error Codes 0: Everything OK                                                                                        ~~
#             1: Unknown error                                                                                        ~~
# Example 0: serialTransmission("/dev/ttyS0", "AOUT 0 1\r")                                                           ~~
#                                                                                                                     ~~
#                                                                                                                     ~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def serialTransmission(cmd):
    errorCode = 0
    serialLock.acquire()  # aquire serial lock to control block access to serial port
    rawData = ""  # generate empty string from raw data
    try:  # try functions below, throw exception if not completed
        MBEDSERIAL.open()  # open serial port
        MBEDSERIAL.reset_input_buffer()  # clear input buffer
        MBEDSERIAL.reset_output_buffer() # clear output buffer
        MBEDSERIAL.write(cmd) # write desired command
        while True:          # wait for "*" to print output
            rawByte = MBEDSERIAL.read()    # pop one character off buffer at a time
            if rawByte != "*":  # check if * character
                rawData += rawByte  # if not, add to raw data, continue while loop
            else:  # if is *
                rawData += rawByte  # add to raw data
                break  # exit while loop

    except SerialException:
        errorCode = 1
        rawData = "***"  # if error when reading in serial data, make raw data *** to be easily thrown away
        print(SerialException)
    finally:
        MBEDSERIAL.reset_input_buffer()  # clear rest of in put buffer
        MBEDSERIAL.close()  # close serial port
        serialLock.release()  # release lock on serial port
        # fileWriter(rawData, mbedLogName)
    return [errorCode, rawData]


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Date last modified: 4/10/18                                                                                         ~~
# Original  Author: Renata Smith                                                                                      ~~
# Last Author: Renata Smith                                                                                           ~~
#                                                                                                                     ~~
# Function: usbTransmission(ser, cmd)                                                                                 ~~
# Description: the only access function to the serial port                                                            ~~
# Parameter 0: desired serial port (Type: String)                                                                     ~~
#           1: serial buffer out (Type: String)                                                                       ~~
# Return: rawData (Type: String)                                                                                      ~~
# Error Codes 0: Everything OK                                                                                        ~~
#             1: Unknown error                                                                                        ~~
# Example 0: serialTransmission("/dev/ttyS0", "AOUT 0 1\r")                                                           ~~
#                                                                                                                     ~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def usbTransmission(cmd):
    errorCode = 0
    try:  # try functions below, throw exception if not completed
        USBSERIAL.open()  # open usb serial port
        USBSERIAL.reset_input_buffer()  # clear input and output buffers
        USBSERIAL.reset_output_buffer()
        USBSERIAL.write(cmd)  # write command to serial port
        rawData = USBSERIAL.readline()  # read in data til \n
    except SerialException:
        errorCode = 1
        rawData = "***"  # make raw data a placeholder to throw away later
        print("SerialException")
    finally:
#        print(rawData)
        USBSERIAL.reset_input_buffer()  #clear input buffer
        USBSERIAL.close() # close serial port

    return [errorCode, rawData]

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Date last modified: 4/10/18                                                                                         ~~
# Original  Author: Cory Bowdach                                                                                      ~~
# Last Author: Cory Bowdach                                                                                           ~~
#                                                                                                                     ~~
# Function: DOUT(digitalOutput, cmd)                                                                                  ~~
# Description: Take in a command from the user application and set/reset the appropriate output                       ~~
# Parameter 0: Output number. 0-7 as integer                                                                          ~~
#          1: Desired output state. 'ON', 'OFF', or 'TOGGLE'                                                          ~~
# Return: error code (see below for detail)                                                                           ~~
# Error Codes 0: Everything OK                                                                                        ~~
#             1: Unknown error                                                                                        ~~
#             2: Invalid input type for output state                                                                  ~~
#             3: Invalid input type for digital input                                                                 ~~
#             4: Input number out of range                                                                            ~~
#             5: Invalid output state given                                                                           ~~
#             6: Serial port error (serial function did not return 0)                                                 ~~
# Example 0: DOUT(1, 'TOGGLE') #toggle output 1 (if its on, turn it off. If its off, turn it on)                      ~~
#         1: DOUT(0, 'OFF') #turn off output 0)                                                                       ~~
#                                                                                                                     ~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def DOUT(digitalOutput, cmd):
    error_code = 1  # initial value. This will be changed if everything is alright

    # Error check inputs
    if type(digitalOutput) != int:  # check input in an integer
        error_code = 2

    if type(cmd) != int:  # check command is a integer
        error_code = 3

    if (digitalOutput < 0) or (digitalOutput > 7):
        error_code = 4

    if not ((cmd == ON) or (cmd == OFF) or (cmd == TOGGLE)):
        error_code = 5

    send = "DOUT " + str(digitalOutput) + " " + str(cmd) + "\r"
    if error_code == 1:  # Send the data to the serial port function
        returnedData = serialTransmission(send)
#        print(returnedData)
        # we dont care about what came back so ignore it
        if returnedData[0] != 0:
            error_code = 6
        error_code = 0
    print(str(error_code) + "\t" + send)

    return error_code

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Date last modified: 4/10/18                                                                                         ~~
# Original  Author: Renata Smith                                                                                      ~~
# Last Author: Renata Smith                                                                                           ~~
#                                                                                                                     ~~
# Function: runPump(init_weight)                                                                                      ~~
# Description: run pump to lower level on scale to desired weight                                                     ~~
# Parameter 0: desired mass on scale (in grams) Type: float                                                           ~~
#                                                                                                                     ~~
# Return: error code (see below for detail)                                                                           ~~
# Error Codes 0: Everything OK                                                                                        ~~
#             1: Unknown error                                                                                        ~~
#             6: Serial port error (serial function did not return 0)                                                 ~~
# Example 0: runPump(252.5) # run pumps til 252.5 grams read on scale                                                 ~~
#                                                                                                                     ~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def runPump(init_weight):
    pumpRUN = True  # variable to control while loop
    DOUT(PUMP, ON)  # turn on pump
    DOUT(SOLENOID, ON)  # open solenoid
    print("PUMP ON")  # let the people know what is happening
    while pumpRUN:  # while pumpRun True
        current_weight = getSCALE()  # get the current weight of scale
        if current_weight > init_weight:  # check to see if it is below the desired weight
            pumpRUN = True  # if not, pumpRun still true
            wait(.01)  # wait for a few msec, then try again
        else:  # if current weight is lower than desired weight
            DOUT(PUMP, OFF)    # turn off pump
            DOUT(SOLENOID, OFF)  # turn off solenoid
            pumpRUN = False  # set pumpRun to false
            print("PUMP OFF")  # let the people know you are done pumping
    return 0



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Date last modified: 4/10/18                                                                                         ~~
# Original  Author: Renata Smith                                                                                      ~~
# Last Author: Renata Smith                                                                                           ~~
#                                                                                                                     ~~
# Function: isMotionComplete()                                                                                        ~~
# Description: check if stepper motion is complete                                                                    ~~
# Parameter 0: None                                                                                                   ~~
# Return: Nothing                                                                                                     ~~
# Example 0: isMotionComplete()                                                                                       ~~
#                                                                                                                     ~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def isMotionComplete():
    stepperMoving = True  # set while loop control variable
    while stepperMoving:  # while stepper is still moving
        if getSTEP0(0) == 1:  # if stepper motion complete data returns a 1 (motion complete)
            stepperMoving = False  # set while loop control varial to False
        else:
            time.sleep(0.01)  # if motion not complete, wait for data to update

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Date last modified: 4/10/18                                                                                         ~~
# Original  Author: Renata Smith                                                                                      ~~
# Last Author: Renata Smith                                                                                           ~~
#                                                                                                                     ~~
# Function: emptyBottle()                                                                                             ~~
# Description: empty bottle completely                                                                                ~~
# Parameter 0: none                                                                                                   ~~
# Return: None                                                                                                        ~~
# Example 0: emptyBottle() # empty bottle completely                                                                  ~~
#                                                                                                                     ~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def emptyBottle():
    bottleNotEmpty = True
    scale = getSCALE()  # get initial scale reading
    ABS0(180)  # invert the bottle
    isMotionComplete()  # wait for motion to complete
    wait(3)  # wait for a few seconds
    while bottleNotEmpty:
        curr = getSCALE()  # get current scale value
        if abs(scale - curr) < 2:  # if difference between previous measurement and current measurement is < 2 grams
            bottleNotEmpty = False  # bottle not empty is false (break while loop)
        else:
            scale = curr  # set current measurement as previous measurement
            wait(3)  # wait for bottle to dispense more
    print("Bottle empty")  # Let the people know what is happening


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Date last modified: 4/10/18                                                                                         ~~
# Original  Author: Renata Smith                                                                                      ~~
# Last Author: Renata Smith                                                                                           ~~
#                                                                                                                     ~~
# Function: pumpON() and pumpOFF()                                                                                    ~~
# Description: turn on  and turn off pump                                                                             ~~
# Parameter 0: none                                                                                                   ~~
# Return: None                                                                                                        ~~
# Example 0: pumpON() # turn on pump                                                                                  ~~
#            pumpOFF()  # turn off pump                                                                               ~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def pumpON():
    DOUT(PUMP, ON)  # Turn on pump
    DOUT(SOLENOID, ON)  # open solendoid valve


def pumpOFF():
    DOUT(PUMP, OFF)  # Turn off pump
    DOUT(SOLENOID, OFF)  # Close solenoid valve


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Date last modified: 4/10/18                                                                                         ~~
# Original  Author: Renata Smith                                                                                      ~~
# Last Author: Renata Smith                                                                                           ~~
#                                                                                                                     ~~
# Function: spoutOPEN()                                                                                               ~~
# Description: Open the spout valve                                                                                   ~~
# Return: error code (see below for detail)                                                                           ~~
# Error Codes 0: Everything OK                                                                                        ~~
#             1: Unknown error                                                                                        ~~
#             6: Serial port error (serial function did not return 0)                                                 ~~
# Example 0: OPEN() # open spout                                                                                      ~~
#                                                                                                                     ~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def spoutOPEN():
    error_code = 1  # initial value. This will be changed if everything is alright
    send = "OPEN\r"
    if error_code == 1:  # Send the data to the serial port function
        returnedData = serialTransmission(send)
#        print(returnedData)
        # we dont care about what came back so ignore it
        if returnedData[0] != 0:
            error_code = 6
        error_code = 0
#    print(str(error_code) + "\t" + send)
    #print("SPOUT OPEN")

    return error_code

def spoutopen():
    spoutOPEN()


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Date last modified: 4/10/18                                                                                         ~~
# Original  Author: Renata Smith                                                                                      ~~
# Last Author: Renata Smith                                                                                           ~~
#                                                                                                                     ~~
# Function: spoutCLOSE()                                                                                              ~~
# Description: Close the spout valve                                                                                  ~~
# Return: error code (see below for detail)                                                                           ~~
# Error Codes 0: Everything OK                                                                                        ~~
#             1: Unknown error                                                                                        ~~
#             6: Serial port error (serial function did not return 0)                                                 ~~
# Example 0: CLOSE('/dev/ttyS)') # close spout                                                                        ~~
#                                                                                                                     ~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def spoutCLOSE():
    error_code = 1  # initial value. This will be changed if everything is alright
    send = "CLOS\r"
    if error_code == 1:  # Send the data to the serial port function
        returnedData = serialTransmission(send)
#        print(returnedData)
        # we dont care about what came back so ignore it
        if returnedData[0] != 0:
            error_code = 6
        error_code = 0
#    print(str(error_code) + "\t" + send)
    #print("SPOUT CLOSED")

    return error_code


def spoutclose():
    spoutCLOSE()


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Date last modified: 4/10/18                                                                                         ~~
# Original  Author: Renata Smith                                                                                      ~~
# Last Author: Renata Smith                                                                                           ~~
#                                                                                                                     ~~
# Function: chargeON()/charge                                                                                                ~~
# Description: Start charging/stop charging                                                                                   ~~
# Parameter 0: none                                                                                            ~~
# Return: error code (see below for detail)                                                                           ~~
# Error Codes 0: Everything OK                                                                                        ~~
#             1: Unknown error                                                                                        ~~
#             6: Serial port error (serial function did not return 0)                                                 ~~
# Example 0: CLOSE('/dev/ttyS)') # close spout                                                                        ~~
#                                                                                                                     ~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def chargeON():
    DOUT(CHARGER, 0)

def chargeOFF():
    DOUT(CHARGER, 1)




# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Date last modified: 4/10/18                                                                                         ~~
# Original  Author: Cory Bowdach                                                                                      ~~
# Last Author: Cory Bowdach                                                                                           ~~
#                                                                                                                     ~~
# Function: AOUT(analogOutput, cmd)                                                                                   ~~
# Description: Take in a command from the user application and set/reset the appropriate output                       ~~
# Parameter 0: Output number. 0-7 as integer                                                                          ~~
#          1: Desired output state. 'ON', 'OFF', or 'TOGGLE'                                                          ~~
# Notes 0: The voltage input should be X.X even if the last X is zero                                                 ~~
# Return: error code (see below for detail)                                                                           ~~
# Error Codes 0: Everything OK                                                                                        ~~
#             1: Unknown error                                                                                        ~~
#             2: Invalid input type for output state                                                                  ~~
#             3: Invalid input type for digital input                                                                 ~~
#             4: Input number out of range                                                                            ~~
#             5: Input command out of range                                                                           ~~
#             6: Serial port error (serial function did not return 0)                                                 ~~
# Example 0: AOUT(0,2.1) #set analog output 0 to 2.1V                                                                 ~~
#         1: AOUT(0,0.0) #set analog output 0 to 0.0V                                                                 ~~
#                                                                                                                     ~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def AOUT(analogOutput, cmd):
    maxVoltage = 3.3
    error_code = 1  # initial value. This will be changed if everything is alright

    # Error check inputs
    if type(analogOutput) != int:  # check input in an integer
        error_code = 2

    if type(cmd) != float:  # check command is a float
        if type(cmd) == int:
            cmd = float(cmd)  #incase starting value is just an int
        else:
            error_code = 3

    if (analogOutput < 0) or (analogOutput > 0):  # only 1 analog output for now
        error_code = 4

    if (cmd > maxVoltage) or (cmd < 0):
        error_code = 5

    send = "AOUT " + str(analogOutput) + " " + str(cmd) + "\r"

    if error_code == 1:  # Send the data to the serial port function
        returnedData = serialTransmission(send)
        # we dont care about what came back so ignore it
        if returnedData[0] != 0:
            error_code = 6
        error_code = 0
    print(str(error_code) + "\t" + send)

    return error_code


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Date last modified: 4/13/18                                                                                         ~~
# Original  Author: Cory Bowdach                                                                                      ~~
# Last Author: Cory Bowdach                                                                                           ~~
#                                                                                                                     ~~
# Function: ABS0(targetDegree)                                                                                        ~~
# Description: Absolute position command for stepper 0      									                      ~~
# Parameter 0: Absolute position target (float)                                                                       ~~
# Return: error code (see below for detail)                                                                           ~~
# Error Codes 0: Everything OK                                                                                        ~~
#             1: Unknown error                                                                                        ~~
#             2: Invalid input type for position command                                                              ~~
#             3: Serial port error (serial function did not return 0)                                                 ~~
# Example 0: ABS0(720.5) #Go to absolute position 720.5      									                          ~~
#         1: ABS0(0)   #Go to absolute position 0																      ~~
#                                                                                                                     ~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def ABS0(targetDegree):
    error_code = 1  # initial value. This will be changed if everything is alright

    # Error check inputs
    if not ((type(targetDegree) == float) or (type(targetDegree) == int)):  # check input in an integer
        error_code = 2

    send = "ABS0 " + str(targetDegree) + "\r"

    if error_code == 1:  # Send the data to the serial port function
        returnedData = serialTransmission(send)
        # we dont care about what came back so ignore it
        if returnedData[0] != 0:
            error_code = 3
        error_code = 0

    print(str(error_code) + "\t" + send)
    while True:
        diff = abs(float(targetDegree) - getSTEP0(2))
        if getSTEP0(0) == 0 or diff < 2:
            break
        else:
            time.sleep(.01)
    return error_code


def abs0(a):  # Allow upper and lower case functions
    return ABS0(a)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Date last modified: 4/13/18                                                                                         ~~
# Original  Author: Renata Smith                                                                                      ~~
# Last Author: Renata Smith                                                                                           ~~
#                                                                                                                     ~~
# Function: POS0(targetDegree)                                                                                        ~~
# Description: Set current position as absolute value of targetDegree     						                      ~~
# Parameter 0: Desired absolute value (float)                                                                         ~~
# Return: error code (see below for detail)                                                                           ~~
# Error Codes 0: Everything OK                                                                                        ~~
#             1: Unknown error                                                                                        ~~
#             2: Invalid input type for position command                                                              ~~
#             3: Serial port error (serial function did not return 0)                                                 ~~
# Example 0: POS0(720.5) #Set current position to 720.5 absolute position    	    		                          ~~
#         1: POS0(0)   #Set current position to 0 absolute position			    								      ~~
#                                                                                                                     ~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def POS0(targetDegree):
    error_code = 1  # initial value. This will be changed if everything is alright

    # Error check inputs
    if not ((type(targetDegree) == float) or (type(targetDegree) == int)):  # check input in an integer
        error_code = 2

    send = "POS0 " + str(targetDegree) + "\r"

    if error_code == 1:  # Send the data to the serial port function
        returnedData = serialTransmission(send)
        # we dont care about what came back so ignore it
        if returnedData[0] != 0:
            error_code = 3
        error_code = 0
    print(str(error_code) + "\t" + send)
    return error_code


def pos0(a):  # Allow upper and lower case functions
    return POS0(a)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Date last modified: 4/13/18                                                                                         ~~
# Original  Author: Cory Bowdach                                                                                      ~~
# Last Author: Cory Bowdach                                                                                           ~~
#                                                                                                                     ~~
# Function: INC0(incTargetDegree)                                                                                     ~~
# Description: Incremental position command for stepper 0      									                      ~~
# Parameter 0: Incremental position target (float)                                                                    ~~
# Return: error code (see below for detail)                                                                           ~~
# Notes 1: Change the current target position to CURRENT POSITION plus parameter (not previous target)                ~~
#       2: INC0(0)  effectively stops the motor in place														      ~~
# Error Codes 0: Everything OK                                                                                        ~~
#             1: Unknown error                                                                                        ~~
#             2: Invalid input type for position command                                                              ~~
#             3: Serial port error (serial function did not return 0)                                                 ~~
# Example 0: INC0(720) #move to a position 720 degrees from the current position                                      ~~      									                          ~~
#         1: INC0(0)   #Stop motor              																      ~~
#                                                                                                                     ~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def INC0(incTargetDegree):
    error_code = 1  # initial value. This will be changed if everything is alright

    # Error check inputs
    if not ((type(incTargetDegree) == float) or (type(incTargetDegree) == int)):  # check input in an integer
        error_code = 2

    send = "INC0 " + str(incTargetDegree) + "\r"

    if error_code == 1:  # Send the data to the serial port function
        returnedData = serialTransmission(send)
        # we dont care about what came back so ignore it
        if returnedData[0] != 0:
           error_code = 3
        error_code = 0
    while True:
        diff = abs(float(incTargetDegree) - getSTEP0(2))
        if getSTEP0(0) == 0 or diff < 2:
            break
        else:
            time.sleep(.01)
    print(str(error_code) + "\t" + send)
    return error_code


def inc0(a):  # Allow upper and lower case functions
    return INC0(a)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Date last modified: 4/13/18                                                                                         ~~
# Original  Author: Cory Bowdach                                                                                      ~~
# Last Author: Cory Bowdach                                                                                           ~~
#                                                                                                                     ~~
# Function: VEL0(degPerSecond)                                                                                        ~~
# Description: Set the velocity for stepper 0													                      ~~
# Parameter 0: Degrees per second (float)                                                                             ~~
# Return: error code (see below for detail)                                                                           ~~
# Error Codes 0: Everything OK                                                                                        ~~
#            1: Unknown error                                                                                         ~~
#            2: Invalid input type for speed command                                                                  ~~
#            3: Serial port error (serial function did not return 0)                                                  ~~
# Example 0: VEL0(725.3) #set speed to 725.3 degrees per second									                      ~~
#         1: VEL0(0) 	 #set speed to 0 degrees per second. This is still 'moving' at speed of 0                     ~~
#                                                                                                                     ~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def VEL0(degPerSecond):
    error_code = 1  # initial value. This will be changed if everything is alright

    # Error check inputs
    if not ((type(degPerSecond) == float) or (type(degPerSecond) == int)):  # check input in an integer
        error_code = 2

    send = "VEL0 " + str(degPerSecond) + "\r"

    if error_code == 1:  # Send the data to the serial port function
        returnedData = serialTransmission(send)
        # we dont care about what came back so ignore it
        if returnedData[0] != 0:
           error_code = 3
        error_code = 0

    print(str(error_code) + "\t" + send)

    return error_code


def vel0(a, ser):  # Allow upper and lower case functions
    return VEL0(a)




