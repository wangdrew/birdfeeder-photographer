import sys,os,subprocess
from parse import parse as parser


class PhotoCapture:
	def __init__(self):
		self._trigger = PhotoTrigger()
		self._exporter = PhotoExporter()

		self._photo_file_location = ''
		self._camera_brand = 'Nikon'

		if locateUsbDevice() is None:
			print 'Camera not detected'

	'''
	Determines the USB device address using camera name
	'''
	def locateUsbCamera():
		output = subprocess.Popen("lsusb | grep " + self._camera_brand, \
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

	def shouldFireShutter(data):
		pass
	
	def fireShutter():
		call(["gphoto2 --capture-image-and-download -F 1 -I 1"])

	def resetUSBDevice():
		usb_address = locateUsbCamera()
		
		if usb_address is None:
			return False
		else:
			out = subprocess.Popen("./bin/usbreset " + usb_address, shell=True, \
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
				self.resetUSBDevice()	# Reset USB to get ready for the next shot
				self._exporter.exportPhoto(self._photo_file_location)


class PhotoTrigger():
	def __init__():
		pass
	
	def getNewData():
		pass


class PhotoExporter():
	def __init__():
		pass

	def exportPhoto():
		pass

if __name__ is '__main__':
	birdcapture = PhotoCapture()
