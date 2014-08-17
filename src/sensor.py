import sys,os,subprocess,time
import urllib2
import Queue
import RPi.GPIO as GPIO

''' GPIO Setup '''
GPIO_PIR = 17
GPIO_LED = 22
GPIO_PING_TRIGGER = 23
GPIO_PING_ECHO = 18
PING_MAX_TRIES = 50
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_PIR, GPIO.IN)
GPIO.setup(GPIO_LED, GPIO.OUT)
GPIO.setup(GPIO_PING_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_PING_ECHO, GPIO.IN)

''' sensor constants'''
MAX_DISTANCE_THRESHOLD = 13.0
MIN_DISTANCE_THRESHOLD = 2.0
pir_state = False

''' how often to take photos '''
TIME_WAIT_BTWN_PHOTOS = 2 #10.0
TIME_WAIT_BTWN_PHOTO_SETS = 5 # 300.0
MAX_PHOTO_SET_SIZE = 5
MAX_PHOTOS = 350
# MAX_PHOTOS_IN_TIME_PERIOD = 5
# TIME_PERIOD = 60	# in seconds

''' REST call params '''
rest_server_ip = '0.0.0.0'	# this is the 2nd rasppi IP
rest_server_port = '80'


def pollSensors():
	if pirDetected():
		distance = calculateDistanceToWall()
		if distance < MAX_DISTANCE_THRESHOLD and \
			distance > MIN_DISTANCE_THRESHOLD:
			return True
	else:
		return False


def triggerShutter():

	print 'I FIRED!'

	# Make REST call to 2nd RaspPi
	# urllib2.urlopen("http://" + rest_server_port + \
	# 	":" + rest_server_port + "/bird?confidence=100")


'''
Used to measure the distance to our primary target using the 
PING ultradistance sensor.

Credit: Matt Hawkins - http://goo.gl/nZUiYg
'''
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


def run():
	
	photo_just_taken = False
	photos_taken = 0	
	photos_in_curr_set = 0
	# timestamp_q = Queue.queue()

	while True:

		shouldFireTrigger = pollSensors()

		if shouldFireTrigger:

			photos_taken += 1

			triggerShutter()

			if photo_just_taken:
				photos_in_curr_set += 1
				print('# curr set: %s' % str(photos_in_curr_set))
				
				if photos_in_curr_set > MAX_PHOTO_SET_SIZE:
					time.sleep(TIME_WAIT_BTWN_PHOTO_SETS)
					photos_in_curr_set = 0

				else:
					time.sleep(TIME_WAIT_BTWN_PHOTOS)
			
			else:
				photos_in_curr_set = 1
				time.sleep(TIME_WAIT_BTWN_PHOTOS)
				print('# curr set reset')

			photo_just_taken = True	

		else:
			photo_just_taken = False

		if photos_taken > MAX_PHOTOS:
			break

		time.sleep(.5)

if __name__ == '__main__':
	run()
