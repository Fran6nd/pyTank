import math
import pygame
from pygEngine.vector2D import Vector2D
from pygEngine.transform import Transform
from pygEngine.imageLoader import ImageLoader
from pygEngine.triangleCollider import TriangleCollider
from pygEngine._gameObjects.dynamicGameObject import DynamicGameObject
from explosion import Explosion
from pygame.locals import *
class Bullet(DynamicGameObject):

	def setup(self):
		self.collidable = True
		self.bodyTexture = ImageLoader.get('Bullet')
		self.rotateSpeed = 1
		self.speed = 500
		self.bodyTexture.convert()
		self.lifetime = 2
		self.bodyTexture, self.r = Bullet.rotatePivoted(self.bodyTexture, -math.degrees(self.transform.angle) + 90 + 180, (self.transform.pos.x, self.transform.pos.y))
		self.bodyTexture.set_colorkey((255, 255, 255))
		self.transform.velocity = self.transform.forward() * self.speed
		self.currentLifeTime = 0

	def getParams(self):
		return (self.transform, self.team, self.layer, self.__class__.__name__)

	def draw(self,main, offset = Vector2D.zero()):
		screen = main.screen
		screen.blit(self.bodyTexture, (self.transform.pos.x + offset.x -self.r.w/2, self.transform.pos.y + offset.y - self.r.h/2))

	def update(self, dt, main):
		if self.currentLifeTime > self.lifetime:
			self.removeGameObject(self, main)
		self.currentLifeTime += dt

	def onCollision(self, hit, main):
		self.explode(main, hit)

	def explode(self, main, o):
		explodeParams = self.params.copy()
		explodeParams.layer =+1
		self.instantiate(main, Explosion, self.transform, explodeParams)
		if hasattr(o, 'hurt'):
			o.hurt(main)
		self.destroy(main)
if __name__ == "__main__":
	print('Nothing to do...')