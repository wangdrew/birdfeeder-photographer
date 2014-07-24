from parse import parse as parser
from Queue import Queue
from capture_rest_server import CaptureRestServer
import thread
import sys,os,subprocess, time

def main():
	birdcapture = PhotoCapture()
	birdcapture.run()

def startRestServerThread(sharedqueue):
		rest_server = CaptureRestServer(sharedqueue)
		rest_server.run()

class PhotoCapture:
	def __init__(self):
		self.kill_switch = False
		self.sharedqueue = Queue()
		self._exporter = PhotoExporter()
		self._photo_file_location = ''
		self._camera_brand = 'Nikon'

		if self.locateUsbCamera() is None:
			print 'Camera not detected'
		else:
			print 'Camera is good to go!'
	
	'''
	Determines the USB device address using camera name
	'''
	def locateUsbCamera(self):
		output = subprocess.Popen("lsusb | grep " + self._camera_brand, \
		 shell=True, stdout=subprocess.PIPE).stdout.read()

		print('Locate USBcamera got: %s' % str(output))

		if output == '':
			return None
		else:
			output = output.split(":")[0]
			strings = parser("Bus {} Device {}", output)
			if strings is not None:
				return '/dev/bus/usb/' + strings[0] + '/' + strings[1]
			else: 
				return None

	def shouldFireShutter(data):
		if 'confidence' in data:
			confidence = int(data['confidence'])
			if confidence > 70:
				return True
			else:
				return False
		else:
			return False
	
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
				if 'msg' in value:
					if value['msg'] == 'halt':
						if self.kill_switch == False:
							self.kill_switch = True

					elif value['msg'] == 'bird' and \
						'msg_payload' in value:
						if self.kill_switch == True:
							self.kill_switch = False
						return value['msg_payload'] 


	def run(self):

		thread.start_new_thread(startRestServerThread, (self.sharedqueue,))

		while True:
			data = self.checkQueueMessages()

			# Use data to figure out whether to fire the shutter
			if (data is not None and \
				self.kill_switch is not True and \
				self.shouldFireShutter(data) ):
				
				self.fireShutter()
				self.resetUSBDevice()	# Reset USB to get ready for the next shot
				# self._exporter.exportPhoto(self._photo_file_location)

	def run_test(self):

		thread.start_new_thread(startRestServerThread, (self.sharedqueue,))

		for x in range(0,1):
			self.fireShutter()
			self.resetUSBDevice()	# Reset USB to get ready for the next shot
			self.checkQueueMessages()


class PhotoExporter():
	def __init__(self):
		pass

	def exportPhoto(self):
		pass

if __name__ == "__main__":
	main()
