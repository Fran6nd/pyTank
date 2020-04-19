#Add gameEngine to the python modules path.
import sys
sys.path.append("..")
from pygEngine.scene import Scene
from pygEngine.params import Params
from pygEngine.vector2D import Vector2D
from pygEngine.transform import Transform
from pygEngine.gameObject import GameObject
from pygEngine.imageLoader import ImageLoader
from pygEngine.instantiator import Instantiator
from pygEngine.triangleCollider import TriangleCollider
from udpPacket import UdpPacket
import pygame
import json
import socket
import time
from threading import Thread
#Import project's modules.
from bush import Bush
from crate import Crate
from bullet import Bullet
from tankTrace import TankTrace
from explosion import Explosion
from discovery import Discovery
from localTankBot import LocalTankBot
from localTankPlayer import LocalTankPlayer
from networkTankPlayer import NetworkTankPlayer
from PIL import Image
from io import StringIO
import time
import random
import string
class Server(Scene):

	def loadResources(self, loader):
		loader('Bullet.png')
		loader('Bush.png')
		loader('Crate.bmp')
		loader('Tank.png')
		loader('Explosion.png')
		loader('TankTrace.png')

	def registerGameObjects(self, register):
		register(Bush)
		register(Bullet)
		register(LocalTankPlayer)
		register(Crate)
		register(LocalTankBot)
		register(TankTrace)
		register(Explosion)
		register(NetworkTankPlayer)

	def __init__(self, screen = None):
		Scene.__init__(self, screen)
		self.port = 9898
		self.destinationPort = 8989
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.bind(('0.0.0.0', self.port))
		#self.sock.settimeout(1)
		self.sock.setblocking(0)
		self.connected = dict()
		self.debug = True
		self.msgWaitingAck = dict()
		self.enableGameLogic = True
		self.discoveryServer = Discovery()
		t = Thread(target = self.listener)
		t.start()

	def removekey(d, key):
		r = dict(d)
		del r[key]
		return r

	def buildPlayerBulletListPos(self):
		ls = list()
		comps = self.gameComponents.copy()
		for layer in comps:
			layer = layer.copy()
			for key in layer:
				gc =  layer[key]
				if not gc.localOnly:
					ls.append(gc.getParams())
		return ls

	def sendData(self, ip, data):
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		if data['type'] == 'MSG_ACK':

			_id = ''.join(random.choice(string.ascii_letters) for x in range(10))
			data.update({'msgId' : _id})
			data.update({'ip' : ip})
			data.update({'timeWhenSent' : self.millis()})
			if not 'attempt no' in data:
				data.update({'attempt no' : 0})
			else:
				data['attempt no'] = data['attempt no'] + 1
			self.msgWaitingAck.update({_id : data})
		data = json.dumps(data).encode('utf-8')
		sock.sendto(data, (ip, self.destinationPort))

	def resendNonAcked(self):
		msgWaitingAck = self.msgWaitingAck.copy()
		keyOfPacketsToDelete = list()
		for key in msgWaitingAck:
			packet = self.msgWaitingAck[key]
			if (self.millis() - (packet['timeWhenSent'])) > 150:
				print(packet['attempt no'])
				if packet['ip'] in self.connected:
					if  packet['attempt no'] > 5:
						self.removePlayer(packet['ip'])
						keyOfPacketsToDelete.append(key)
					else:	
						self.sendData(packet['ip'], packet)
				else :
					keyOfPacketsToDelete.append(key)
		for key in keyOfPacketsToDelete:
			del self.msgWaitingAck[key]

	def buildMap(self):
		self.debug = True
		playerParams = Params('player', 10, 0, 1)
		crateParams = Params(layer = 1)
		bushParams = Params(layer = 2)
		botParams = Params(layer = 1, team = 'bot')
		t = self.instantiate(LocalTankPlayer.classId, Transform(Vector2D(300, 200), 0), playerParams)
		self.currentPlayer = t
		self.instantiate(Crate.classId, Transform(Vector2D(400,200),0), crateParams)
		self.instantiate(Crate.classId, Transform(Vector2D(200,270),0), crateParams)
		self.instantiate(Crate.classId, Transform(Vector2D(100,270),0), crateParams)
		self.instantiate(Crate.classId, Transform(Vector2D(50,150),0), crateParams)
		self.instantiate(Crate.classId, Transform(Vector2D(250,270),0), crateParams)
		self.instantiate(Crate.classId, Transform(Vector2D(750,670),0), crateParams)
		self.instantiate(Crate.classId, Transform(Vector2D(650,570),0), crateParams)
		self.instantiate(Crate.classId, Transform(Vector2D(550,470),0), crateParams)
		self.instantiate(Crate.classId, Transform(Vector2D(450,870),0), crateParams)
		self.instantiate(Crate.classId, Transform(Vector2D(350,670),0), crateParams)
		self.instantiate(Bush.classId, Transform(Vector2D(150,370),1), bushParams)
		self.instantiate(Bush.classId, Transform(Vector2D(450,670),1), bushParams)

	def removePlayer(self, ip):
		self.removeGameObject(self.connected[ip].params)
		del self.connected[ip]
		print('[Info]: Someone just left us: '+ '@' + ip)

	def listener(self):
		t1 = self.millis()
		t2 = self.millis()
		timeBeforeScanningPacketAck = 0
		while self.done == False:
			t2 = self.millis()
			if timeBeforeScanningPacketAck < 0:
				timeBeforeScanningPacketAck = 100
				self.resendNonAcked()
			timeBeforeScanningPacketAck -= (t2-t1)
			data, addr = self.recvInput()
			if data != None:
				if data['type'] == 'MSG_ACK':
					self.sendData(addr, {
						'type' : 'ACK',
						'msgId' : data['msgId']
						})
					if data['commandType'] == 'DISCONNECT':
						self.removePlayer(addr)
				if data['type'] == 'ACK':
					del self.msgWaitingAck[data['msgId']]
				elif data['type'] == 'MSG_NO_ACK':
					if data['commandType'] == 'INPUTS':
						if not addr in self.connected:
							print('[Info]: Someone just joined us: ' + data['name'] + '@' + addr)
							self.sendMap(addr)
							o = self.instantiate(NetworkTankPlayer.classId, Transform(Vector2D(100,100),0),Params('player', 10, 0, 1))
							self.sendData(addr, self.buildInstanciatePacket(o, True))
							self.connected.update({addr : o})
							o.setVectorInput(data)
						else:
							o = self.connected[addr]
							o.setVectorInput(data)
							#print(data['inputs']['shooting'])
			t1 = t2
			self.discoveryServer.listen()

	def sendInstantiationToAll(self, o):
		for ip in self.connected:
			isTheRemotePlayer = False
			if self.connected[ip] == o:
				isTheRemotePlayer = True
			data = self.buildInstanciatePacket(o, isTheRemotePlayer)
			self.sendData(ip, data)
	def sendDeletionToAll(self, o):
		#if o:
		for ip in self.connected:
			isTheRemotePlayer = False
			if self.connected[ip] == o:
				isTheRemotePlayer = True
			data = self.buildDeletePacket(o)
			self.sendData(ip, data)
	def sendUpdateToAll(self, o):
		for ip in self.connected:
			isTheRemotePlayer = False
			if self.connected[ip] == o:
				isTheRemotePlayer = True
			data = self.buildUpdatePacket(o)
			self.sendData(ip, data)
	def buildInstanciatePacket(self, o, isTheRemotePlayer = False):
		msg = {
		'type' : 'MSG_ACK',
		'commandType' : 'INSTANTIATE',
		'object' : o.toDict(),
		'isTheRemotePlayer' : isTheRemotePlayer
		}
		return msg
	def sendMap(self, ip):
		comps = self.gameComponents.copy()
		for layer in comps:
			layer = layer.copy()
			for key in layer:
				gc =  layer[key]
				if not gc.localOnly and gc.classId != -1:
					data = self.buildInstanciatePacket(gc, False)
					self.sendData(ip, data)

	def buildDeletePacket(self, o):
		msg = {
		'type' : 'MSG_ACK',
		'commandType' : 'DEL',
		'object' : o.toDict()
		}
		return msg
	def buildUpdatePacket(self, o):
		msg = {
		'type' : 'MSG_ACK',
		'commandType' : '_UPDATE',
		'object' : o.toDict()
		}
		return msg

	def onInstanciation(self, o):
		self.sendInstantiationToAll(o)

	def onDeletion(self, o):
		self.sendDeletionToAll(o)

	def onParamsOrTransformChange(self, o):
		self.sendUpdateToAll(o)

	def recvInput(self):
		data, addr = '', ''
		try:
			data, addr = self.sock.recvfrom(1024) # buffer size is 1024 bytes.
		except:
			return None, None
		data = data.decode('utf-8')
		data = json.loads(data)
		return data, addr[0]

if __name__ == "__main__":
	Server().run()