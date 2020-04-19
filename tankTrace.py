import math
import pygame
from pygEngine.triangleCollider import TriangleCollider
from pygEngine.vector2D import Vector2D
from pygEngine.imageLoader import ImageLoader
from pygEngine.gameObject import GameObject
from pygame.locals import *
class TankTrace(GameObject):

	def setup(self):
		self.bodyTexture = ImageLoader.get('TankTrace')
		self.id = -1
		self.bodyTexture.convert()
		self.im, self.r = TankTrace.rotatePivoted(self.bodyTexture, -math.degrees(self.transform.angle) + 90, (self.transform.pos.x, self.transform.pos.y))
		self.im.set_colorkey((255, 255, 255))
		self.drawn = False
		self.updated = False

	def draw(self,main, offset = Vector2D.zero()):
		if not self.drawn:
			main.backGround.blit(self.im, (self.transform.pos.x -self.r.w/2, self.transform.pos.y - self.r.h/2))
		self.drawn = True
		if self.drawn and self.updated:
			main.removeGameObject(self.params)

	def update(self, dt, main):
		self.updated = True
		if self.drawn and self.updated:
			main.removeGameObject(self.params)
if __name__ == "__main__":
	print('Nothing to do...')