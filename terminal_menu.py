import sys, os
import termios, fcntl
import select
import serial



fd = sys.stdin.fileno()
newattr = termios.tcgetattr(fd)
newattr[3] = newattr[3] & ~termios.ICANON
newattr[3] = newattr[3] & ~termios.ECHO
termios.tcsetattr(fd, termios.TCSANOW, newattr)

oldterm = termios.tcgetattr(fd)
oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

ser = serial.Serial("/dev/ttyS0", 115200, timeout=1)
usb = serial.Serial("/dev/USB0", 115200, timeout=1)

print("Menu options")
print("1 - Turn on pump")
print("2 - turn off pump")
print("3 - Send stepper to 0 position")
print("4 - Set current position as 0 position")
print("5 - set position to 180")
print("6 - open spout")
print("7 - close spout")
#print("8 - run pump to fill bottle")
#print("9 - Empty bottle")
print("q - Quit this program")
print("Type some stuff")
while True:
    inp, outp, err = select.select([sys.stdin], [], [])
    c = sys.stdin.read()
    if c == '1':
        ser.write("DOUT 0 1\r")
        ser.write("DOUT 1 1\r")
    if c == '2':
        ser.write("DOUT 0 1\r")
        ser.write("DOUT 1 1\r")
    if c == '3':
        ser.write("ABS0 0\r")
    if c == '4':
        ser.write("POS0 0\r")
    if c == '5':
        ser.write("ABS0 180\r")
    if c == '6':
        ser.write("OPEN\r")
    if c == '7':
        ser.write("CLOS\r")
#    if c == '8':
#        runPumpDispense(575)
#    if c == '9':
#        emptyBottle()
    if c == 'q':
        break
    else:
        print("Not a valid input, try again loser")

# Reset the terminal:
termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)