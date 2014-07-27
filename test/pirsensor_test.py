import os
import datetime
import time
import RPi.GPIO as GPIO
import urllib2

# GPIO Setup
GPIO_PIR = 17
GPIO_LED = 22
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_PIR, GPIO.IN)
GPIO.setup(GPIO_LED, GPIO.OUT)
pir_state = False
# Detects motion with the PIR sensor (this is the primary trigger)

def motionDetectedByPIR(pir_state):
    if (GPIO.input(GPIO_PIR) == True):
    	if pir_state is False:
    		pir_state = True
    		urllib2.urlopen("http://0.0.0.0:80/bird?confidence=80")
    	GPIO.output(GPIO_LED, True)
    	return True
    else:
    	pir_state = False
    	GPIO.output(GPIO_LED, False)
    	return False


while True:
	pir_state = motionDetectedByPIR(pir_state)
	time.sleep(0.1)

