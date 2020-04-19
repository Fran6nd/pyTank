import math
import pygame
from pygEngine.triangleCollider import TriangleCollider
from pygEngine.vector2D import Vector2D
from bullet import Bullet
from tankTrace import TankTrace
from tank import Tank
import pygame
from pygame.locals import *
class NetworkTankPlayer(Tank):

	def __init__(self,transform, params):
		Tank.__init__(self,transform, params)

	def getVectorInput(self, main):
		pass

	def setVectorInput(self, input):
		self.shooting = input['inputs']['shooting']
		self.keyVector = Vector2D(input['inputs']['joystick']['x'], input['inputs']['joystick']['y'])
if __name__ == "__main__":
	print('Nothing to do...')