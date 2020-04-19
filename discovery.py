import socket
from PIL import Image
from io import StringIO
import time
import json
class Discovery():

	def __init__(self, server = True, serverName = 'Server', id = '0xABF'):
		self.ip = '0.0.0.0'
		self.serverPort = 4441
		self.clientPort = 4442
		self.sendPort = 8989
		self.server = server
		self.id = id
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		if server == True:
			self.serverName = serverName
			self.sock.setblocking(0)
			self.sock.bind(('', self.serverPort))
		else:
			self.sock.setblocking(0)
			self.sock.bind(('', self.clientPort))
	def createClient(id = '0xABF'):
		return Discovery(False, id = id)
	def createServer(serverName = 'Server', id = '0xABF'):
		return Discovery(True, serverName, id)
	def listen(self):
			data, addr = self.recvInput()
			if data:
				if self.server == True:
					if self.id == data['id']:
						self.sendDiscoveredPacket(addr)
						print(data)
				else:
					self.discovered.append({'ip' : addr, 'name' : data['name']})
	def sendData(self,msg, ip, port):
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.sendto(json.dumps(msg).encode('utf-8'), (ip, port))

	def recvInput(self):
		data, addr = '', ''
		try:
			data, addr = self.sock.recvfrom(1024) # buffer size is 1024 bytes.
		except:
			return None, None
		data = data.decode('utf-8')
		data = json.loads(data)
		if data['id'] != self.id:
			return None, None
		return data, addr[0]

	def sendBroadcast(self, msg):
		cs = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		cs.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
		cs.sendto(json.dumps(msg).encode('utf-8'), ('255.255.255.255', self.serverPort))

	def sendDiscoveryPacket(self):
		self.sendBroadcast({'type' : 'DISCOVERY', 'id' : self.id})
	def sendDiscoveredPacket(self, ip):
		self.sendData({'type' : 'DISCOVED', 'id' : self.id, 'name' : self.serverName}, ip, self.clientPort)
	def discover(self, timeout = 2):
		self.discovered = list()
		self.sendDiscoveryPacket()
		timeout = timeout * 1000
		endingTime = self.millis() + timeout
		while endingTime > self.millis():
			self.listen()
		return self.discovered
	def millis(self):
		return int(round(time.time() * 1000))
if __name__ == "__main__":
	print(Discovery.createClient().discover())