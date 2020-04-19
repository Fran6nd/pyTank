#Standards imports.
import math
import pygame
from pygame.locals import *
#pygEngine imports.
from pygEngine.inputs import Inputs
from pygEngine.vector2D import Vector2D
from pygEngine.transform import Transform
from pygEngine.imageLoader import ImageLoader
from pygEngine.triangleCollider import TriangleCollider
from pygEngine._gameObjects.uiGameObject import UiGameObject
class Button(UiGameObject):

	def __init__(self, transform, cb, caption = 'BUTTON'):
		super().__init__(transform)
		self.cb = cb
		self.caption = caption
		self.clickable = True
		font=pygame.font.Font(None,30)
		self.text=font.render(self.caption,1,(255,0,0))
		self.text_rect = self.text.get_rect(center=(self.transform.pos.x, self.transform.pos.y))
		self.colliders = TriangleCollider.makeFromPygameRect(self.text_rect)
		self.collidable = True
		self.localOnly = True
		for c in self.colliders:
			c.setTransform(self.transform)

	def draw(self,main, offset = Vector2D.zero()):
		main.screen.blit(self.text, self.text_rect)

	def onClick(self):
		self.cb()

	def update(self, dt, main):
		if Inputs.get('LeftMouseButton').getValue() == True and Inputs.get('LeftMouseButton').justChanged() == True:
			mp = Inputs.get('MousePos').getValue()
			for c in self.colliders:
				if c.isPointInTriangle(mp) == True:
					self.onClick()
					
if __name__ == "__main__":
	print('Nothing to do...')