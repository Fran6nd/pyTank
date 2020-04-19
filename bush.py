import math
import pygame
from pygEngine import *
from pygEngine.triangleCollider import TriangleCollider
from pygEngine.vector2D import Vector2D
from pygEngine.imageLoader import ImageLoader
from pygame.locals import *
from pygEngine._gameObjects.staticGameObject import StaticGameObject
class Bush(StaticGameObject):

	def setup(self):
		self.bodyTexture = ImageLoader.get('Bush')
		self.bodyTexture.convert()
		self.im, self.r = Bush.rotatePivoted(self.bodyTexture, -math.degrees(self.transform.angle) + 90, (self.transform.pos.x, self.transform.pos.y))

	def draw(self,main, offset = Vector2D.zero()):
		screen = main.screen
		screen.blit(self.im, (self.transform.pos.x + offset.x -self.r.w/2, self.transform.pos.y + offset.y - self.r.h/2))

	def rotatePivoted(im, angle, pivot):
		# rotate the leg image around the pivot.
		image = pygame.transform.rotate(im, angle)
		rect = image.get_rect()
		rect.center = pivot
		return image, rect

	def getParams(self):
		return (self.transform, self.__class__.__name__)
if __name__ == "__main__":
	print('Nothing to do...')