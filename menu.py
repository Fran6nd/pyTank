#Add gameEngine to the python modules path.
import sys
sys.path.append("..")
#Import gameEngine's modules.
from pygEngine.scene import Scene
from pygEngine.vector2D import Vector2D
from pygEngine.transform import Transform
from pygEngine.gameObject import GameObject
from pygEngine.imageLoader import ImageLoader
from pygEngine.triangleCollider import TriangleCollider
#Import project's modules.
from bush import Bush
from crate import Crate
from bullet import Bullet
from button import Button
from localTankBot import LocalTankBot
from localTankPlayer import LocalTankPlayer
from main import Main
from client import Client
class Menu(Scene):

	def loadResources(self, loader):
		pass

	def buildMap(self):
		self.debug = True

		def load_main():
			self.loadScene(Main)
		self.instantiateUI(Button(Transform(Vector2D(self.width/2,self.height/2),0), load_main, '[Play SOLO]'))
		self.instantiateUI(Button(Transform(Vector2D(self.width/2,self.height/2 + 50),0), load_main, '[Run SERVER]'))
		self.instantiateUI(Button(Transform(Vector2D(self.width/2,self.height/2 + 100),0), load_main, '[Run CLIENT]'))
if __name__ == "__main__":
	Menu().run()