import sys,os,subprocess,time
import RPi.GPIO as GPIO

GPIO_PIR = 17
GPIO_PING_TRIGGER = 23
GPIO_PING_ECHO = 18
PING_MAX_TRIES = 50
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_PIR, GPIO.IN)
GPIO.setup(GPIO_PING_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_PING_ECHO, GPIO.IN)

def calculateDistanceToWall():

    # Send 10us pulse to trigger
    GPIO.output(GPIO_PING_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_PING_TRIGGER, False)
    start = time.time()
    stop = time.time()
    
    current_try=0
    while GPIO.input(GPIO_PING_ECHO)==0 and (current_try<PING_MAX_TRIES):
        current_try = current_try + 1
        start = time.time()

    while GPIO.input(GPIO_PING_ECHO)==1:
      stop = time.time()

    elapsed = stop-start		# Pulse length
    distance = elapsed * 34000	# speed of sound (cm/s)
    distance = distance / 2 	# Distance there and back
    
    return distance

def pirDetected():
	return GPIO.input(GPIO_PIR) 

def main():
	while True:
		print (str(calculateDistanceToWall()) + ' ' + str(pirDetected()))
		time.sleep(0.5)

if __name__ == '__main__':
	main()