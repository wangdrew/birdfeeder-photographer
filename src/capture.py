import sys,os,subprocess, time
from parse import parse as parser

def main():
	birdcapture = PhotoCapture()
	birdcapture.run_test()

class PhotoCapture:
	def __init__(self):
		self._trigger = PhotoTrigger()
		self._exporter = PhotoExporter()

		self._photo_file_location = ''
		self._camera_brand = 'Nikon'

		if self.locateUsbCamera() is None:
			print 'Camera not detected'
		else:
			print 'We are good to go!'
	'''
	Determines the USB device address using camera name
	'''
	def locateUsbCamera(self):
		print "here4"
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
		pass
	
	def fireShutter(self):
		subprocess.Popen(["gphoto2 --capture-image-and-download \
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
				return True
		
	def run(self):

		while True:
			data = self._trigger.getNewData()

			# Use data to figure out whether to fire the shutter
			if self.shouldFireShutter(data):
				self.fireShutter()
				print 'Resetting USB Device'
				self.resetUSBDevice()	# Reset USB to get ready for the next shot
				self._exporter.exportPhoto(self._photo_file_location)

	def run_test(self):

		for x in range(0,3):
			# TODO: Make this a blocking call
			self.fireShutter()
			time.sleep(9)
			# TODO: Make this a blocking call.
			self.resetUSBDevice()	# Reset USB to get ready for the next shot
			time.sleep(3)

class PhotoTrigger():
	def __init__(self):
		pass
	
	def getNewData(self):
		pass


class PhotoExporter():
	def __init__(self):
		pass

	def exportPhoto(self):
		pass

if __name__ == "__main__":
	main()
