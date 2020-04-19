import math
import pygame
from pygEngine.triangleCollider import TriangleCollider
from pygEngine.vector2D import Vector2D
from pygEngine.imageLoader import ImageLoader
from pygEngine.gameObject import GameObject
from bullet import Bullet
from tankTrace import TankTrace
from tank import Tank
import pygame
from pygame.locals import *
class LocalTankBot(Tank):

	def __init__(self,transform, params):
		Tank.__init__(self, transform, params)
		self.minRange = 400

	def getClosestEnnemy(self, main, team):
		l = main.getGameComponentsByTeam(team)
		cp = None
		mindist = -1
		for p in l:
			dist = (self.transform.pos - p.transform.pos).getModule()
			if (dist<mindist or mindist == -1) and p.killable == True:
				cp = p
				mindist = dist
		return cp, mindist

	def lookAt(self, p):
		angle = Vector2D.getArg(self.transform.pos - p.transform.pos) + math.pi
		delta = self.transform.angle - angle
		delta = delta  - 2 * math.pi if delta> math.pi else delta
		delta = delta + 2 * math.pi if delta< -math.pi else delta
		if delta == 0:
			self.keyVector.x = 0
		elif delta > 0:
			self.keyVector.x = -1
		else:
			self.keyVector.x = 1

	def getVectorInput(self, main):
		self.shooting = False
		self.keyVector = Vector2D.zero()
		e, d = self.getClosestEnnemy(main, 'player')
		if e != None:
			self.keyVector.y = 0
			if d < self.minRange:
				self.lookAt(e)
				gc, d = main.raycast(self.transform.pos + Vector2D.up().setArg(self.transform.angle)*30, Vector2D.up().setArg(self.transform.angle), 10, layer = self.layer)
				if d != None and d < self.minRange:
					if gc.team == 'player':
						self.keyVector.y = 1
						self.shooting = True
if __name__ == "__main__":
	print('Nothing to do...')