birdfeeder-photographer
=======================

Takes pictures with a dSLR camera of birds at your feeder automatically! Requires two Raspberry PIs communicating through wifi. One is attached to the birdfeeder outside, reads the sensors, and triggers the second PI which is inside take a picture when a bird lands on the feeder. The seconds PI interfaces with the dSLR via USB.

Dependencies
============

gphoto2

python-flickrapi

flask

mimerender

parse


Installation
============

On your raspberry pi:

git clone https://github.com/wangdrew/birdfeeder-photographer.git

Ensure python-dev and pip package manager is installed:

sudo apt-get install python-dev

sudo apt-get install python-pip

Then install project python dependencies:

sudo apt-get install gphoto2

sudo pip install parse

sudo easy_install flickrapi

sudo pip install Flask

sudo pip install mimerender



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

export FLICKR_API_KEY='xyz' 

export FLICKR_API_SECRET='xyz'

export FLICKR_API_TOKEN='xyz0'


Running birdfeeder-photographer
===============

On the Raspberry PI hooked up to the camera:

Ensure Flickr environment variables are set.

sudo env FLICKR_APP_KEY=$FLICKR_APP_KEY FLICKR_APP_SECRET=$FLICKR_APP_SECRET FLICKR_APP_TOKEN=$FLICKR_APP_TOKEN python capture.py

The extra keywords in front of the python command are necessary in order to allow superuser access to the environment variables that the Flikr integration requires

On the Raspberry PI interfacing with the sensors it's much simpler:

sudo python src/sensors.py