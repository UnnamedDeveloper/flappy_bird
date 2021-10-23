import esper
import pygame

from .components import *
from ..scenes import layers
from .. import graphics as gfx

class RenderSystem (esper.Processor):
	def __init__(self, debug):
		self.debug = debug

	def percentage_between(self, value: float, a: float, b: float) -> float:
		return (a - value) / (b - value)

	def process(self, delta):
		for actor, (camera, cam_position) in self.world.get_components(Camera, Position):
			viewport = camera.target.get_rect()

			# create layers
			draw_layers = []
			for i in range(layers.LAYER_COUNT):
				# create transparent surfaces for each layer
				draw_layers.append(pygame.surface.Surface((viewport.w, viewport.h), pygame.SRCALPHA, 32))
				draw_layers[i] = draw_layers[i].convert_alpha()

			for actor, (background) in self.world.get_components(Background):
				camera.target.blit(background[0].image, (0, 0))

			# draw colliders
			if self.debug:
				# the extra padding to add to the collider boxes for visibility
				debug_width = 5
				for actor, (position, collider) in self.world.get_components(Position, BoxCollider):
					# calculate top-left of collider
					x = position.x + collider.offset_x - (collider.width / 2)
					y = position.y + collider.offset_y - (collider.height / 2)

					# apply camera offset
					x -= cam_position.x + camera.offset_x

					pygame.draw.rect(camera.target, (0, 255, 0),
						(x - debug_width,
							y - debug_width,
							collider.width + (debug_width * 2),
							collider.height + (debug_width * 2)))

			# draw sprites
			for actor, (position, sprite) in self.world.get_components(Position, Sprite):
				rotation = sprite.rotation
				if self.world.has_component(actor, Velocity):
					velocity = self.world.component_for_entity(actor, Velocity)

					# rotate with a variation of 120 degrees up or down dependent on the current y
					# velocity
					rotation = self.percentage_between(velocity.y, 0, velocity.y_speed_cap * 2)
					rotation *= 120

				# rotate sprite
				rotated_img = pygame.transform.rotate(sprite.image, rotation)

				rect = rotated_img.get_rect()

				# move sprite according to actor location
				rect.x += position.x - (rect.w / 2)
				rect.y += position.y - (rect.h / 2)

				# move sprite according to camera location
				rect.x -= cam_position.x + camera.offset_x

				# draw sprite
				draw_layers[sprite.layer - 1].blit(rotated_img, rect)

			# apply layers
			for layer in draw_layers:
				camera.target.blit(layer, (0, 0))

class MovementSystem (esper.Processor):
	def __init__(self, gravity: float = 500.0):
		self.gravity = -gravity

	def process(self, delta):
		for actor, (position, velocity) in self.world.get_components(Position, Velocity):
			velocity.x = max(-velocity.x_speed_cap, min(velocity.x_speed_cap, velocity.x))
			velocity.y = max(-velocity.y_speed_cap, min(velocity.y_speed_cap, velocity.y))
			position.x += velocity.x * delta
			position.y += velocity.y * delta

			velocity.y -= self.gravity * delta

class InputSystem (esper.Processor):
	def __init__(self):
		self.last_pressed = pygame.key.get_pressed()

	def process(self, delta):
		keys = pygame.key.get_pressed()
		for actor, (velocity, move) in self.world.get_components(Velocity, InputMove):
			# do not process a move event without a set key
			if move.key == None:
				continue

			if keys[move.key]:
				# dont trigger if it requires the button to be pressed
				if move.press and self.last_pressed[move.key]:
					continue

				velocity.x = move.move_x
				velocity.y = move.move_y

		for actor, (position, callback) in self.world.get_components(Position, InputCallback):
			if callback.key == None:
				continue

			if keys[callback.key]:
				if callback.press and self.last_pressed[callback.key]:
					continue

				if callback.callback != None:
					callback.callback(delta)

		self.last_pressed = keys

class CollitionSystem (esper.Processor):
	def aabb_overlap(self, a_pos: Position, a_col: BoxCollider, b_pos: Position, b_col: BoxCollider):
		a_x = a_pos.x + a_col.offset_x
		a_y = a_pos.y + a_col.offset_y
		b_x = b_pos.x + b_col.offset_x
		b_y = b_pos.y + b_col.offset_y

		return (abs(a_x - b_x) * 2 < (a_col.width + b_col.width)) and \
			(abs(a_y - b_y) * 2 < (a_col.height + b_col.height))

	def process(self, delta):
		for actor, (position, collider, velocity) in self.world.get_components(Position, BoxCollider, Velocity):
			for compare_actor, (comp_position, comp_collider) in self.world.get_components(Position, BoxCollider):
				if actor == compare_actor:
					continue

				if self.aabb_overlap(position, collider, comp_position, comp_collider):
					if collider.on_collition != None:
						collider.on_collition()

class ScriptSystem (esper.Processor):
	def process(self, delta):
		for actor, (script) in self.world.get_components(Script):
			for s in script:
				if s.update != None:
					s.update(delta)
