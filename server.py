#!/usr/bin/python3

'''




'''
import picamera
import socket

from UdpStreamer import UdpStreamer, UdpPoller
from Discovery import Discovery

DISCOVERY_PORT = 13654
CONTROL_PORT = 8008
VIDEO_PORT = 8010
VERSION = '0.01'

camera = picamera.PiCamera()
camera.resolution = (640, 480)
camera.framerate = 20

discovery = Discovery(VIDEO_PORT, CONTROL_PORT)
discovery.run()

streamer = UdpStreamer(VIDEO_PORT)


def set_parameter(parameter, value):
	if(parameter == 'brightness'):
		value = int(value)
		print('Setting ', parameter, 'to', value)
		camera.brightness = value
	elif(parameter == 'contrast'):
		value = int(value)
		if(value > -100 and value < 100):
			camera.contrast = value
	elif(parameter == 'awb_mode'):
		if(value in list(picamera.PiCamera.AWB_MODES.keys())):
			camera.awb_mode = value
	elif(parameter == 'drc_strength'):
		if(value in ['off', 'low', 'medium', 'high']):
			camera.drc_strength = value
	elif(parameter == 'exposure_compensation'):
		value = int(value)
		if(value > -25 and value < 25):
			camera.exposure_compensation = value
	elif(parameter == 'exposure_mode'):
		if(value in list(picamera.PiCamera.EXPOSURE_MODES.keys())):
			camera.exposure_mode = value
	elif(parameter == 'flash_mode'):
		if(value in list(picamera.PiCamera.FLASH_MODES.keys())):
			camera.flash_mode = value
	elif(parameter == 'hflip'):
		if(value == 'true'):
			camera.hflip = True
		elif(value == 'false'):
			camera.hflip = False
	elif(parameter == 'image_denoise'):
		if(value == 'true'):
			camera.image_denoise = True
		elif(value == 'false'):
			camera.image_denoise = False
	elif(parameter == 'image_effect'):
		if(value in list(picamera.PiCamera.IMAGE_EFFECTS.keys())):
			camera.image_effect = value
	elif(parameter == 'iso'):
		if(value in list('100', '200', '320', '400', '500', '640', '800')):
			camera.iso = int(value)
	elif(parameter == 'led'):
		if(value == 'true'):
			camera.led = True
		elif(value == 'false'):
			camera.led = False

camera.start_recording(streamer, 
		format='h264', quality=20)

control = UdpPoller(CONTROL_PORT, set_parameter)
control.run()

camera.wait_recording(10)
#set_brightness(camera)
print("Set brightness")
camera.wait_recording(200)
