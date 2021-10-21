import pygame

from . import graphics as gfx

class Application (object):
	def __init__(self, name: str, size: list = [500, 500], icon = None):
		pygame.init()
		pygame.font.init()
		pygame.mixer.init()

		self.window = gfx.Window(name, size = size, icon = icon)
		self.scene = None

	def run(self) -> bool:
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.scene.stop()
					return True
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						return True

			if self.scene != None:
				try:
					self.scene = self.scene.update()
				except Exception as e:
					print("A fatal error occured in the scene. Aborting")
					print(e)
					self.scene.stop()
					return False
			else:
				return True

			self.window.refresh()
