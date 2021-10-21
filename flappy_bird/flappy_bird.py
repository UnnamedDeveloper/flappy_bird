from .application import Application
from . import scenes
from . import graphics as gfx

class FlappyBird (Application):
	def __init__(self):
		bg = gfx.load_image("background-day.png")
		Application.__init__(self, 
			name = "Flappy bird",
			size = [bg.get_rect().w, bg.get_rect().h],
			icon = gfx.load_image("yellowbird-midflap.png"))
		self.scene = scenes.InitScene(self.window.surface, bg)
		# self.scene = scenes.GameScene(self.window.surface, bg)
