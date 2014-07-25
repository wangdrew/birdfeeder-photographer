import os
import datetime
import time
import RPi.GPIO as GPIO

# GPIO Setup
GPIO_PIR = 11
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_PIR, GPIO.IN)

# Detects motion with the PIR sensor (this is the primary trigger)
def motionDetectedByPIR():
    if (GPIO.input(GPIO_PIR) == True):
        return True
    else:
        return False


while True:
	print motionDetectedByPIR()
	time.sleep(0.5)

