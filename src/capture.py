from parse import parse as parser
from Queue import Queue
from capture_rest_server import CaptureRestServer
import thread
import sys,os,subprocess,time
import flickrapi
from flickrapi import FlickrError

def main():
	birdcapture = PhotoCapture()
	birdcapture.run()

def startRestServerThread(sharedqueue):
		rest_server = CaptureRestServer(sharedqueue)
		rest_server.run()

class PhotoCapture:
	def __init__(self):
		self.CAMERA_BRAND = 'Nikon'
		self.CONFIDENCE_THRSHOLD = 70

		self.sharedqueue = Queue()
		self._flickr = FlickrUploader()
		self._photo_file_location = ''

		if self.locateUsbCamera() is None:
			print 'Camera not detected'
		else:
			print 'Camera is ready'
	
	'''
	Determines the USB device address using camera name
	'''
	def locateUsbCamera(self):
		output = subprocess.Popen("lsusb | grep " + self.CAMERA_BRAND, \
		 shell=True, stdout=subprocess.PIPE).stdout.read()

		if output == '':
			return None
		else:
			output = output.split(":")[0]
			strings = parser("Bus {} Device {}", output)
			if strings is not None:
				return '/dev/bus/usb/' + strings[0] + '/' + strings[1]
			else: 
				return None

	def shouldFireShutter(self, data):
		confidence = int(data)
		if confidence >= self.CONFIDENCE_THRSHOLD: return True
		else: return False
	
	def fireShutter(self):
		subprocess.call(["gphoto2 --capture-image-and-download \
			--force-overwrite -F 1 -I 1"], shell=True)

	def resetUSBDevice(self):

		usb_address = self.locateUsbCamera()
		
		print('Resetting USB Device with address : %s ' % str(usb_address))

		if usb_address is None:
			return False
		else:
			out = subprocess.Popen("../bin/usbreset " + usb_address, shell=True, \
				stdout=subprocess.PIPE).stdout.read()
			if 'successful' not in out.lower():
				print 'USB failed to reset, reason: ' + out
				return False
			else:
				print 'USB successfully reset'
				return True

	def checkQueueMessages(self):
		while True:
			if self.sharedqueue.empty():
				break
			else:
				value = self.sharedqueue.get(False)
				if 'bird' in value:
					return value['bird'] # Contains confidence level


	def run(self):

		thread.start_new_thread(startRestServerThread, (self.sharedqueue,))

		while True:
			data = self.checkQueueMessages()

			# Use data to figure out whether to fire the shutter
			if data is not None and self.shouldFireShutter(data):
				if self.resetUSBDevice() is True:
					self.fireShutter()
					self._flickr.uploadPhoto(self._photo_file_location)
					print 'upload complete'
				else:
					print 'No camera found'


	def run_test(self):

		thread.start_new_thread(startRestServerThread, (self.sharedqueue,))

		for x in range(0,1):
			self.fireShutter()
			self.resetUSBDevice()	# Reset USB to get ready for the next shot
			self.checkQueueMessages()


class FlickrUploader():
	def __init__(self):
		self.api_key = os.getenv('FLICKR_APP_KEY')
		self.api_secret = os.getenv('FLICKR_APP_SECRET')
		self.api_token = os.getenv('FLICKR_APP_TOKEN')
		if self.api_key is None or \
			self.api_secret is None or \
			self.token is None:
			self.flickr = None
		try:
			self.flickr = flickrapi.FlickrAPI(api_key = self.api_key, \
				secret = self.api_secret, token = self.api_token)
		except FlickrError as e:
			print('Could not register with Flickr services, reason: ' \
				+ str(e))
			self.flickr = None

	def uploadPhoto(self, photo_location):
		if self.flickr is not None:
			pass
			# flickr.upload()
		else: 
			pass

if __name__ == "__main__":
	main()
