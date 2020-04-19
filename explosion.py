import math
import pygame
from pygEngine.vector2D import Vector2D
from pygEngine.transform import Transform
from pygEngine.imageLoader import ImageLoader
from pygEngine.triangleCollider import TriangleCollider
from pygEngine._gameObjects.staticGameObject import StaticGameObject
from pygame.locals import *
class Explosion(StaticGameObject):

	def __init__(self,transform, params):
		StaticGameObject.__init__(self, transform, params)

	def setup(self):
		self.lifetime = 0.15
		self.bodyTexture = ImageLoader.get('Explosion')
		self.rotateSpeed = 1
		self.speed = 500
		self.bodyTexture.convert()
		self.params.life = 0

	def getParams(self):
		return (self.transform, self.team, self.layer, self.life, self.__class__.__name__)

	def draw(self, main, offset = Vector2D.zero()):
		screen = main.screen
		im = pygame.transform.scale(self.bodyTexture.copy(), (int(self.bodyTexture.get_width()*self.params.life/self.lifetime),int(self.bodyTexture.get_height()*self.params.life/self.lifetime)))
		im.set_colorkey((0, 0, 0))
		screen.blit(im, (self.transform.pos.x + offset.x -im.get_width()/2, self.transform.pos.y + offset.y - im.get_height()/2))

	def update(self, dt, main):
		if self.params.life > self.lifetime:
			self.removeGameObject(self, main)
		else:
			self.params.life += dt
if __name__ == "__main__":
	print('Nothing to do...')