import pygame

from .bird import Bird
from .layers import *
from .. import ecs
from .. import graphics as gfx

class Ground:
	def __init__(self, scene: ecs.Scene, bird: Bird, offset_factor: float = 0.0):
		self.scene = scene
		self.bird = bird
		self.actor = scene.add_actor()

		if bird != None:
			viewport = bird.actor.get_component(ecs.Camera).target.get_rect()
		else:
			viewport = scene.surface.get_rect()
		ground_sprite = gfx.load_image("base.png")
		self.actor.add_component(ecs.Position(x = 0 + (ground_sprite.get_rect().w * offset_factor), y = viewport.h - (ground_sprite.get_rect().h / 4)))
		self.actor.add_component(ecs.Sprite(layer = LAYER_GROUND, image = ground_sprite))
		self.actor.add_component(ecs.BoxCollider(width = ground_sprite.get_rect().w, height = ground_sprite.get_rect().h))
		self.actor.add_component(ecs.Script(update = self.update))

	def update(self, delta):
		if self.bird != None:
			camera = self.bird.actor.get_component(ecs.Camera)
			viewport = camera.target.get_rect()
			viewport.x += self.bird.actor.get_component(ecs.Position).x - camera.offset_x

			position = self.actor.get_component(ecs.Position)
			sprite = self.actor.get_component(ecs.Sprite)
			if viewport.x > position.x + sprite.image.get_rect().w:
				position.x += sprite.image.get_rect().w * 2
