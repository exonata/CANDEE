from library.main import *


numCycles = 1000
fillVal = 575 # grams to fill the bottle with
dispVal = 450 # grams dispensed and replaced by pump
cycles = 0

# Initialization sequence
dataThread = initTest(False)
startCollectingData(dataThread)
wait(5)
VEL0(120)
print("STARTING TEST")
POS0(0)
ABS0(0) # send stepper motor to zero position
wait(1)
emptyBottle()
wait(1)
ABS0(0)
isMotionComplete()
wait(1)
curr = getSCALE() - fillVal
runPump(curr)
wait(2)
ABS0(0)

tare_scale = getSCALE() # Record starting scale value
init_scale = tare_scale
while cycles < numCycles:
    # get base scale val
    print("In while loop")
    current_dif = getSCALE()-tare_scale
    if current_dif < dispVal:  # if current difference between starting weight and current weight
        print("in if statement 1")                       # is less than desired amount dispensed
        ABS0(180)  # invert bottle
        isMotionComplete()  # wait for motion to complete
        print("in if statement 2")
        wait(2)
        ABS0(0)
        isMotionComplete()
        print("in if statement 3")
        wait(2)
    else:
        runPump(init_scale)
        print("in else statement 1")
        tare_scale = getSCALE()
        print("in else statement ")
        cycles += 1
        wait(1)


stopCollectingData(dataThread)

