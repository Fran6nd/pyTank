#Add gameEngine to the python modules path.
import sys
sys.path.append("..")
#Import gameEngine's modules.
from pygEngine.scene import Scene
from pygEngine.params import Params
from pygEngine.vector2D import Vector2D
from pygEngine.transform import Transform
from pygEngine.gameObject import GameObject
from pygEngine.imageLoader import ImageLoader
from pygEngine.instantiator import Instantiator
from pygEngine.triangleCollider import TriangleCollider
#Import project's modules.
from bush import Bush
from crate import Crate
from bullet import Bullet
from tankTrace import TankTrace
from explosion import Explosion
from localTankBot import LocalTankBot
from localTankPlayer import LocalTankPlayer
from networkTankPlayer import NetworkTankPlayer
class Main(Scene):

	def loadResources(self, loader):
		loader('Bullet.png')
		loader('Bush.png')
		loader('Crate.bmp')
		loader('Tank.png')
		loader('Explosion.png')
		loader('TankTrace.png')

	def registerGameObjects(self, register):
		register(Bush)
		register(Bullet)
		register(LocalTankPlayer)
		register(Crate)
		register(LocalTankBot)
		register(TankTrace)
		register(Explosion)
		register(NetworkTankPlayer)

	def buildMap(self):
		self.debug = True
		playerParams = Params('player', 10, 0, 1)
		crateParams = Params(layer = 1)
		bushParams = Params(layer = 2)
		botParams = Params(layer = 1, team = 'bot')
		t = self.instantiate(LocalTankPlayer.classId, Transform(Vector2D(100, 100), 0), playerParams)
		self.currentPlayer = t
		self.instantiate(Crate.classId, Transform(Vector2D(200,200),0), crateParams)
		self.instantiate(Crate.classId, Transform(Vector2D(200,270),0), crateParams)
		self.instantiate(Crate.classId, Transform(Vector2D(100,270),0), crateParams)
		self.instantiate(Crate.classId, Transform(Vector2D(50,150),0), crateParams)
		self.instantiate(Crate.classId, Transform(Vector2D(250,270),0), crateParams)
		self.instantiate(Crate.classId, Transform(Vector2D(750,670),0), crateParams)
		self.instantiate(Crate.classId, Transform(Vector2D(650,570),0), crateParams)
		self.instantiate(Crate.classId, Transform(Vector2D(550,470),0), crateParams)
		self.instantiate(Crate.classId, Transform(Vector2D(450,870),0), crateParams)
		self.instantiate(Crate.classId, Transform(Vector2D(350,670),0), crateParams)
		self.instantiate(Bush.classId, Transform(Vector2D(150,370),0), bushParams)
		self.instantiate(Bush.classId, Transform(Vector2D(450,670),0), bushParams)
		self.instantiate(LocalTankBot.classId, Transform(Vector2D(650, 650), 0), botParams)
if __name__ == "__main__":
	Main().run()