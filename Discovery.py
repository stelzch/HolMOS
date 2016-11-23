# DISCOVERY PROCESS
import time
import threading

from UdpStreamer import UdpStreamer


class Discovery:
	def __init__(self, videoPort, controlPort, updatePeriod=10, discoveryPort=13654):
		self.message = 'RASPBERRY DISCOVERY:'+str(videoPort)+','+str(controlPort)
		self.discoveryStreamer = UdpStreamer(discoveryPort)
		self.discoveryThread = threading.Thread(target=self.__discovery_function__)

		self.updatePeriod = updatePeriod

	def __discovery_function__(self):
		while True:
			self.discoveryStreamer.write(bytes(self.message, 'utf-8'))
			time.sleep(self.updatePeriod)		

	def run(self):
		self.discoveryThread.start()