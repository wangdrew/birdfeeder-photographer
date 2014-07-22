import sys,os
from subprocess import call

class PhotoCapture:
	def __init__(self):
		self.__trigger = PhotoTrigger()
		self.__exporter = PhotoExporter()

		self.__photo_file_location = ''

	def shouldFireShutter(data):
		pass
	
	def fireShutter():
		call(["gphoto2 --capture-image-and-download -F 3 -I 1"])

	def resetUSBDevice():
		pass
		
	def run(self):

		while True:
			data = self.__trigger.getNewData()

			# Use data to figure out whether to fire the shutter
			if self.shouldFireShutter(data):
				fireShutter()
				self.__exporter.exportPhoto(self.__photo_file_location)

	def test_run(self):
		fireShutter()


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
