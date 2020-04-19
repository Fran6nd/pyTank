import math
import pygame
from pygEngine.inputs import Inputs
from pygEngine.triangleCollider import TriangleCollider
from pygEngine.vector2D import Vector2D
from pygEngine.imageLoader import ImageLoader
from pygEngine.gameObject import GameObject
from bullet import Bullet
from tankTrace import TankTrace
from tank import Tank
import pygame
from pygame.locals import *
class LocalTankPlayer(Tank):

	def __init__(self,transform, params):
		Tank.__init__(self, transform, params)

	def getVectorInput(self, main):
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
if __name__ == "__main__":
	print('Nothing to do...')