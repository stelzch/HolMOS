import netifaces as ni
import socket

class UdpStreamer:
	def __init__(self, port, interface='eth0'):
		# Do some magic to get the broadcast address of the ethernet
		# interfaces
		self.clientIp = str(ni.ifaddresses(interface)[ni.AF_INET][0]['addr'][:11]+'.255')
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