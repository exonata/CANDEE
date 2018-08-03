
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Date last modified: 4/10/18                                                                                         ~~
# Original  Author: Renata Smith                                                                                      ~~
# Last Author: Renata Smith                                                                                           ~~
#                                                                                                                     ~~
# File: pinDefinitions.py                                                                                             ~~
# Description: Declare variables for sensors in an out                                                                ~~
# Parameter: None                                                                                                     ~~
# Return: None                                                                                                        ~~
#                                                                                                                     ~~
#                                                                                                                     ~~
#                                                                                                                     ~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
FILELOC = "/home/pi/SKYFLOW_TESTSTAND/logs/"
FILEHEAD = "Time,DIN1,DIN2,DIN3,DIN4,DIN5,DIN6,DIN7,DIN8,DOUT0,DOUT1,DOUT2,DOUT3, DOUT4, DOUT5, DOUT6, DOUT7, AIN0, AIN1,AIN2,AIN3,AOUT0, INPOS0, TARPOS0, CURPOS0, CURVEL0, SCALE\n"

mbedLogName = "/home/pi/SKYFLOW_TESTSTAND/logs/mbedlog.txt"
scaleLogName = "/home/pi/SKYFLOW_TESTSTAND/logs/scalelog.txt"


RELAY_0 = 0  # Add comments/change dout name to match what pin is controlling
RELAY_1 = 1
RELAY_2 = 2
RELAY_3 = 3
CHARGER = 3
AOUT_0 = 0
AIN_0 = 0
AIN_1 = 1
AIN_2 = 2
AIN_3 = 3
OFF = 0
ON = 1
TOGGLE = 2

BUTTON_1 = 0
BUTTON_2 = 1
SOLENOID = 1
PUMP = 0


STEP_COMPLETE = 0
STEP_DES = 1
STEP_CUR = 2
STEP_VEL = 4

PORT = '/dev/ttyS0'
BAUD = 38400
USBPORT = '/dev/ttyUSB0'
