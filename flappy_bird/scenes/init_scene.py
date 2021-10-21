import pygame

from .. import ecs
from .. import graphics as gfx
from .layers import *
from .bird import Bird
from .game_scene import GameScene
from .ground import Ground
from .pipe import Pipe

class InitScene (ecs.Scene):
	def __init__(self, surface: pygame.Surface, bg: pygame.Surface):
		ecs.Scene.__init__(self, surface, name = "Init")
		self.surface = surface

		center_x = bg.get_rect().w / 2
		center_y = bg.get_rect().h / 2

		self.bg = self.add_actor()
		self.bg.add_component(ecs.Background(image = bg))
		self.bg.add_component(ecs.Position(x = center_x, y = center_y))
		self.bg.add_component(ecs.Camera(target = surface, offset_x = -center_x))

		self.overlay = self.add_actor()
		self.overlay.add_component(ecs.Position(x = center_x, y = center_y))
		self.overlay.add_component(ecs.Sprite(image = gfx.load_image("message.png")))
		self.overlay.add_component(ecs.InputCallback(key = pygame.K_SPACE, callback = self.start))

		self.ground = Ground(self, None, offset_factor = 0.5)

	def start(self, delta):
		self.load_scene(GameScene(self.surface, self.bg.get_component(ecs.Background).image))
