import netifaces as ni
import socket
import threading
import time

TIMEOUT = 5.0 # Timeout in seconds

class UdpStreamer:
	def __init__(self, port, interface='eth0'):
		# Do some magic to get the broadcast address of the ethernet
		# interfaces
		#self.clientIp = str(ni.ifaddresses(interface)[ni.AF_INET][1]['addr'][:11]+'.255')
		self.clientIp = "192.168.178.255"
		self.clientPort = port
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

	def write(self, s):
		if len(s) > 65500:
			# Split package to multiple packets
			numPackages = len(s) // 65500
			remainingBytes = len(s) % 65500

			# Send the first packages
			for i in range(0,numPackages):
				#print('Sent package %d' % (i*65500))
				self.send(s[i*65500:(i+1)*65500])

			# Pack the remaining bytes into another package
			if remainingBytes > 0:
				self.send(s[numPackages*65500:])
				#print('Sent package %d' % (numPackages*65500))
		else:
			#print(len(s))
			self.send(s)

	def send(self, d):
		self.sock.sendto(d, (self.clientIp, self.clientPort))

class UdpPoller:
	def __init__(self, port, callback, interface='eth0'):
		#self.ip = str(ni.ifaddresses(interface)[ni.AF_INET][0]['addr'])
		self.ip = "192.168.178.255"
		self.port = port
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.bind((self.ip, self.port))
		self.sock.settimeout(TIMEOUT)

		self.callback = callback
		self.receiveThread = threading.Thread(target=self.__recv_message__)

	def __recv_message__(self):
		t = threading.currentThread()
		while getattr(t, 'shouldRun', True) == True:
			try:
				data, address = self.sock.recvfrom(1024)
			except socket.timeout:
				print("Timed out")
				continue

			# Parse the message
			if(data[:10] == b'RASPBERRY '):
				message = data[10:].decode('utf-8')
				message = message.split('=')
				if(len(message) == 2):
					self.callback(message[0], message[1])
					print('Received to set', message[0], 'to', message[1])
				else:
					print('Received malformed message: ', data, address)
			else:
				print('Received malformed message: ', data, address)
		print("Terminating")
		return

	def run(self):
		self.receiveThread.start()

	def stop(self):
		print("Stop called")
		self.receiveThread.shouldRun = False
		self.receiveThread.join()
		print("REcv joined")
		