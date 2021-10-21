import pygame

class Window (object):
	def __init__(self, title: str, size: list = [500, 500], icon: pygame.Surface = None):
		# create window
		self.surface = pygame.display.set_mode(size)

		# set window title
		pygame.display.set_caption(title)

		# set icon
		if icon != None:
			pygame.display.set_icon(icon)

	def refresh(self):
		pygame.display.flip()
