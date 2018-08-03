#!/usr/bin/python3
import RPi.GPIO as GPIO
import time


#put this at the end of: sudo nano /etc/profile
#sudo python /home/pi/rasp-pi/shutdown.py &

 
#this method will be invoked when the event occurs
def restart(channel):
    command = "/usr/bin/sudo /sbin/shutdown now"
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print(output)

 
swtch = 7
GPIO.setmode(GPIO.BOARD)
GPIO.setup(swtch,GPIO.IN)
# adding event detect to the switch pin
GPIO.add_event_detect(swtch, GPIO.BOTH, restart, 600)
#print("Event armed\r\n")
try:
	while(True):
		#to avoid 100% CPU usage	
		time.sleep(1)
except KeyboardInterrupt:
	#cleanup GPIO settings before exiting
	GPIO.cleanup()


