#Add gameEngine to the python modules path.
import sys
sys.path.append("..")
from pygEngine.scene import Scene
from pygEngine.vector2D import Vector2D
from pygEngine.inputs import Inputs
from pygEngine.params import Params
from pygEngine.transform import Transform
import pygame
import json
import socket
from bush import Bush
from crate import Crate
from bullet import Bullet
from tankTrace import TankTrace
from explosion import Explosion
from localTankBot import LocalTankBot
from localTankPlayer import LocalTankPlayer
from networkTankPlayer import NetworkTankPlayer
from threading import Thread
class Client(Scene):

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
		self.debug = True
		#FIXME! Ask for the server address.
		self.server_ip = '192.168.1.68'
		#Uncomment for testing purpose.
		self.server_ip = '127.0.0.1'
		self.targetPort = 9898
		self.listenPort = 8989
		self.name = 'Fran6nd'
		self.enableGameLogic = False
		t = Thread(target = self.listener)
		t.start()
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.setblocking(0)
		self.sock.bind((self.server_ip, self.listenPort))

	def buildMap(self):
		pass
	def update(self, dt):
		super().update(dt)
		self.sendData(self.buildPacketInputs((self.getVectorInput())))

	def sendData(self, input):
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.sendto(input.encode('utf-8'), (self.server_ip, self.targetPort))

	def getVectorInput(self):
		keyVector = Vector2D.zero()
		keystate = pygame.key.get_pressed()
		self.keyVector = Vector2D.zero()
		if Inputs.get('space').getValue():
			self.shooting = True
		else:
			self.shooting = False
		if Inputs.get('up').getValue():
			self.keyVector += Vector2D.up()
		if Inputs.get('down').getValue():
			self.keyVector += Vector2D.down()
		if Inputs.get('right').getValue():
			self.keyVector += Vector2D.right()
		if Inputs.get('left').getValue():
			self.keyVector += Vector2D.left()
		input = list()
		input.append(self.shooting)
		input.append(keyVector)
		inputs = {
			'shooting' : self.shooting,
			'joystick' : self.keyVector.toDict()
		}
		return inputs

	def buildPacketInputs(self, inputs):
		return json.dumps({
			'type' : 'MSG_NO_ACK',
			'msgId' : '0',
			'commandType' : 'INPUTS',
			'inputs' : inputs,
			'name' : self.name
			})

	def recvInput(self):
		try:
			data, addr = self.sock.recvfrom(4096) # buffer size is 1024 bytes
			if data:
				return json.loads(data.decode('utf-8')),addr[0]
			return (data), addr[0]
		except:
			return None, None

	def listener(self):
		while self.done == False:
			data, addr = self.recvInput()
			if data:
				if addr == self.server_ip:
					if data['type'] == 'MSG_ACK':
						self.sendData(json.dumps({
							'type' : 'ACK',
							'msgId' : data['msgId']
							}))
						if data['commandType'] == 'INSTANTIATE':
							obj = data['object']
							o = self.instantiateWithForcedId(obj['classId'], Transform.fromDict(obj['transform']), Params.fromDict(obj['params']))
							if data['isTheRemotePlayer'] == True:
								self.currentPlayer = o
						if data['commandType'] == 'DEL':
							obj = data['object']
							o = self.removeGameObject(Params.fromDict(obj['params']))
						if data['commandType'] == '_UPDATE':
							obj = data['object']
							p = Params.fromDict(obj['params'])
							o = self.getGameObjectByParams(p)
							if o:
								o.params = p
								o.setTransform(Transform.fromDict(obj['transform']))
					elif data['type'] == 'MSG_NO_ACK':
						pass
	def quit(self):
		super().quit()
		self.sendData(json.dumps({
			'type' : 'MSG_ACK',
			'commandType' : 'DISCONNECT',
			'msgId' : '1234'
			}))
	def run(self):
		super().run()
		while not self.done:
			pass
if __name__ == "__main__":
	Client().run()