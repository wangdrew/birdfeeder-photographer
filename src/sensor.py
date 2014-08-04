import sys,os,subprocess,time
import urllib2
import RPi.GPIO as GPIO


# GPIO Setup
GPIO_PIR = 17
GPIO_LED = 22
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_PIR, GPIO.IN)
GPIO.setup(GPIO_LED, GPIO.OUT)
pir_state = False
rest_server_ip = '0.0.0.0'
rest_server_port = '80'


class SensorMan:

	def __init__(self):
		pass

	def is_pir_true(self):
		return GPIO.input(GPIO_PIR) 

	def is_distance_true(self):
		pass

	def get_trigger_confidence():
		if self.is_pir_true() and self.is_distance_true():
			return 100
		else:
			return 0

	def trigger_shutter(self, confidence):
		urllib2.urlopen("http://" + rest_server_port + \
			":" + rest_server_port +"/bird?confidence=" + \
			confidence)

	def run(init):
		while True:
			confidence = self.get_trigger_confidence()
			self.trigger_shutter(confidence)
