#!/usr/bin/python3
from picamera.array import PiRGBArray
from picamera import PiCamera
from http.server import BaseHTTPRequestHandler, HTTPServer



from UdpStreamer import UdpStreamer
from Discovery import Discovery

DISCOVERY_PORT = 13654
CONTROL_PORT = 8008
VIDEO_PORT = 8010
VERSION = '0.01'

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 20
		
class APIHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		if(len(self.path)>1):
			print(self.path)
			if(self.path == '/about'):
				self.send_response(200)
				self.wfile.write(bytes('Raspberry Cam '+VERSION+'\r\n', 'utf-8'))
				return
			if(self.path == '/brightness'):
				brightness = int(value)
				camera.brightness = brightness
				self.send_response(200)
				self.wfile.write('Brightness set\r\n')
				return
			

		self.send_response(403)
		return

discovery = Discovery(VIDEO_PORT, CONTROL_PORT)
discovery.run()


streamer = UdpStreamer(VIDEO_PORT)

camera.start_recording(streamer, 
		format='h264', quality=20)

server = HTTPServer(('', CONTROL_PORT), APIHandler)
server.serve_forever()
