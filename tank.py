import math
import pygame
from bullet import Bullet
from tankTrace import TankTrace
from pygame.locals import *
from pygEngine.vector2D import Vector2D
from pygEngine.transform import Transform
from pygEngine.imageLoader import ImageLoader
from pygEngine.triangleCollider import TriangleCollider
from pygEngine._gameObjects.dynamicGameObject import DynamicGameObject

class Tank(DynamicGameObject):

	def setup(self):
		self.spawnable = True
		self.killable = True
		self.collidable = True
		self.bodyTexture = ImageLoader.get('Tank')
		self.rotateSpeed = 1
		self.speed = 100
		self.bodyTexture.convert()
		
		p1 = Vector2D(25, 16)
		p2 = Vector2D(-25, 16)
		p3 = Vector2D(25, -18)
		p4 = Vector2D(-25, -18)
		self.colliders.append(TriangleCollider(p1, p2, p3, self.transform))
		self.colliders.append(TriangleCollider(p4, p2, p3, self.transform))
		self.lastShot = 0
		self.delayBetweenShots = 0.2
		self.keyVector = Vector2D.zero()
		self.shooting = False

	def getVectorInput(self):
		self.keyVector = Vector2D.zero()
		self.shooting = False

	def shoot(self, dt, main):
		if self.shooting and self.lastShot > self.delayBetweenShots:
			bulletTransform = Transform(self.transform.pos, self.transform.angle)
			bulletTransform.pos += Vector2D(0,30).setArg(self.transform.angle)
			bulletParams = self.params.copy()
			bulletParams.life = 0
			main.instantiate(Bullet.classId, bulletTransform, bulletParams)
			self.lastShot =0
		else:
			self.lastShot += dt

	def draw(self, main, offset = Vector2D.zero()):
		screen = main.screen
		im, r = Tank.rotatePivoted(self.bodyTexture, -math.degrees(self.transform.angle) + 90, (self.transform.pos.x, self.transform.pos.y))
		im.set_colorkey((255, 0, 0))
		screen.blit(im, (self.transform.pos.x + offset.x -r.w/2, self.transform.pos.y + offset.y - r.h/2))

	def update(self, dt, main):
		self.getVectorInput(main)
		if self.keyVector.y < 0:
			self.keyVector.x = self.keyVector.x * -1
		self.shoot(dt, main)
		self.transform.velocity =  Vector2D.up() * self.keyVector.y * self.speed
		self.transform.angularVelocity = self.rotateSpeed * self.keyVector.x
		if self.transform.velocity != Vector2D.zero() or self.transform.angularVelocity != 0:
			pass#main.instantiate(TankTrace.classId, self.transform, self.params)

if __name__ == "__main__":
	print('Nothing to do...')