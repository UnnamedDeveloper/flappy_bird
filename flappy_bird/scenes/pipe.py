import random

import pygame

from .layers import *
from .. import ecs
from .. import graphics as gfx

class Pipe:
	def __init__(self, scene: ecs.Scene, x: float, y: float, facing_up: bool = False):
		self.scene = scene
		self.actor = scene.add_actor()

		pipe_sprite = gfx.load_image("pipe-green.png")
		self.actor.add_component(ecs.Position(x = x, y = y))
		self.actor.add_component(ecs.Sprite(layer = LAYER_PIPE, image = pipe_sprite, rotation = 0 if facing_up else 180))
		self.actor.add_component(ecs.BoxCollider(width = pipe_sprite.get_rect().w, height = pipe_sprite.get_rect().h))

class PipePair:
	def __init__(self, scene: ecs.Scene, surface: pygame.Surface, bird, x: float, callback):
		self.scene = scene
		self.bird = bird
		self.callback = callback

		self.height = -random.randint(0, 100)

		self.top = Pipe(scene, x, self.height, False)
		self.bottom = Pipe(scene, x, surface.get_rect().h - 80 + self.height, True)
		self.bottom.actor.add_component(ecs.Script(update = self.update))

	def delete(self):
		self.top.actor.delete()
		self.bottom.actor.delete()

	def update(self, delta):
		camera = self.bird.actor.get_component(ecs.Camera)
		viewport = camera.target.get_rect()
		viewport.x += self.bird.actor.get_component(ecs.Position).x + camera.offset_x

		bottom_position = self.bottom.actor.get_component(ecs.Position)
		top_position = self.top.actor.get_component(ecs.Position)
		sprite = self.bottom.actor.get_component(ecs.Sprite)
		if viewport.x > bottom_position.x + sprite.image.get_rect().w:
			self.callback(self)
