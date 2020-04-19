import math
import pygame
from pygEngine.vector2D import Vector2D
from pygEngine.imageLoader import ImageLoader
from pygEngine._gameObjects.staticGameObject import StaticGameObject
from pygEngine.triangleCollider import TriangleCollider
from pygame.locals import *
class Crate(StaticGameObject):

	def setup(self):
		self.collidable = True
		self.bodyTexture = ImageLoader.get('Crate')
		self.bodyTexture.convert()
		p1 = Vector2D(25, 25)
		p2 = Vector2D(-25, 25)
		p3 = Vector2D(25, -25)
		p4 = Vector2D(-25, -25)
		self.colliders.append(TriangleCollider(p1, p2, p3, self.transform))
		self.colliders.append(TriangleCollider(p4, p2, p3, self.transform))
		self.im, self.r = Crate.rotatePivoted(self.bodyTexture, -math.degrees(self.transform.angle) + 90, (self.transform.pos.x, self.transform.pos.y))
		for c in self.colliders:
			c.setTransform(self.transform)		

	def draw(self,main, offset = Vector2D.zero()):
		screen = main.screen
		screen.blit(self.im, (self.transform.pos.x + offset.x -self.r.w/2, self.transform.pos.y + offset.y - self.r.h/2))

	def getParams(self):
		return (self.transform, self.__class__.__name__)
if __name__ == "__main__":
	print('Nothing to do...')