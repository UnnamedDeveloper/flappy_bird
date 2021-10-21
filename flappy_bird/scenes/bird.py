import pygame

from .layers import *
from .. import audio
from .. import ecs
from .. import graphics as gfx

class Bird:
	def __init__(self, scene: ecs.Scene, surface: pygame.Surface, death_callback):
		self.scene = scene
		self.actor = scene.add_actor()
		self.death_callback = death_callback

		center_x = surface.get_rect().w / 2
		center_y = surface.get_rect().h / 2

		self.wing_sound = audio.load_audio("wing.wav")
		self.die_sound = audio.load_audio("die.wav")
		self.hit_sound = audio.load_audio("hit.wav")

		bird_sprite = gfx.load_image("yellowbird-midflap.png")
		self.actor.add_component(ecs.Position(x = 0, y = center_y))
		self.actor.add_component(ecs.Velocity(x = 100, y = 0))
		self.actor.add_component(ecs.Sprite(layer = LAYER_PLAYER, image = bird_sprite))
		self.actor.add_component(ecs.Camera(target = surface, offset_x = -(center_x / 2)))
		self.actor.add_component(ecs.InputMove(key = pygame.K_SPACE, move_x = 100, move_y = -250.0))
		self.actor.add_component(ecs.InputCallback(key = pygame.K_SPACE, callback = lambda delta : audio.play(self.wing_sound)))
		self.actor.add_component(ecs.BoxCollider(on_collition = self.bird_crash,
			width = bird_sprite.get_rect().w, height = bird_sprite.get_rect().h))

		self.alive = True

	def bird_crash(self):
		if self.alive:
			# removing this component crashes the game, so just disable it instead
			self.actor.get_component(ecs.InputMove).key = None

			# change sprite to dead version
			self.actor.get_component(ecs.Sprite).image = gfx.load_image("redbird-midflap.png")

			# cool velocity things
			velocity = self.actor.get_component(ecs.Velocity)
			velocity.x = 0.0
			velocity.y = -abs(velocity.y / 2.0) # bounce

			# trigger callback
			self.death_callback(self)

			# play death sound
			audio.play(self.die_sound)

			# play collition sound
			audio.play(self.hit_sound, channel = 3)

			# kill bird
			self.alive = False
