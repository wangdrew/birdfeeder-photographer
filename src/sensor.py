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
MAX_DISTANCE_THRESHOLD = 14.0
MIN_DISTANCE_THRESHOLD = 2.0
pir_state = False

''' maximum photos before shutoff '''
MAX_PHOTOS = 300

''' take no more than max photos in timeperiod'''
MAX_PHOTOS_IN_TIME_PERIOD = 5
TIME_PERIOD = 90.0 	# in seconds
TIME_WAIT_BTWN_PHOTOS = 10.0
TIME_WAIT_BTWN_TIME_PERIODS = 400.0

''' REST call params '''
rest_server_ip = '192.168.1.117'	# this is the 2nd rasppi IP
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
	try:
		urllib2.urlopen("http://" + rest_server_ip + \
			":" + rest_server_port + "/bird?confidence=100")
	except:
		print "Error with REST call"


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
	
	GPIO.output(GPIO_LED, True)

	photos_taken = 0	
	timestamp_q = Queue.Queue(MAX_PHOTOS_IN_TIME_PERIOD)

	while True:

		shouldFireTrigger = pollSensors()

		if shouldFireTrigger:

			time_now = time.time()
			
			timestamp_q.put(time_now)

			triggerShutter()

			photos_taken += 1
			
			print('time: %s', str(time_now))
			
			if timestamp_q.full():
				time_first_photo = timestamp_q.get()
				print('q full')
				if time_now - time_first_photo < TIME_PERIOD:
					print('sleeping %s sec' % str(TIME_WAIT_BTWN_TIME_PERIODS))
					time.sleep(TIME_WAIT_BTWN_TIME_PERIODS)
			else:
				time.sleep(TIME_WAIT_BTWN_PHOTOS)

		if photos_taken > MAX_PHOTOS:
			break

		time.sleep(.5)

	GPIO.output(GPIO_LED, False)

if __name__ == '__main__':
	run()
