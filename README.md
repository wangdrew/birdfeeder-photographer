birdfeeder-photographer
=======================

Takes pictures with a dSLR camera of birds at your feeder automatically! Requires two Raspberry PIs communicating through wifi. One is attached to the birdfeeder outside, reads the sensors, and triggers the second PI which is inside take a picture when a bird lands on the feeder. The seconds PI interfaces with the dSLR via USB.

Dependencies
============

gphoto2

python-flickrapi

flask


Installation
============

On your raspberry pi:

git clone https://github.com/wangdrew/birdfeeder-photographer.git

sudo apt-get install gphoto2

sudo pip install parse

sudo easy_install flickrapi



Getting a flickr API key
=============

Register a developer app on flickr's website. Obtain an API key and secret

In an environment with a web browser installed, open a python shell and run the following commands:

import flickrapi

api_key = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

api_secret = 'YYYYYYYYYYYYYYYY'

flickr = flickrapi.FlickrAPI(api_key, api_secret)

(token, frob) = flickr.get_token_part_one(perms='write')

This will open a webpage where you will allow your app to access and write to your account. Click accept and run the last command:

token = flickr.get_token_part_two((token, frob))

Copy the token.

On the Raspberry PI which is hooked up to the dSLR, set the following environvment variables:

FLICKR_API_KEY 

FLICKR_API_SECRET

FLICKR_API_TOKEN


Running birdfeeder-photographer
===============

On the Raspberry PI hooked up to the camera:

sudo python src/capture.py

On the Raspberry PI interfacing with the sensors:

sudo python src/sensors.py